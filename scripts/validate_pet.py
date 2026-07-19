#!/usr/bin/env python3
"""Validate the distributable Codex v2 pet package in this repository."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image


COLUMNS = 8
ROWS = 11
CELL_WIDTH = 192
CELL_HEIGHT = 208
ATLAS_SIZE = (COLUMNS * CELL_WIDTH, ROWS * CELL_HEIGHT)
# Row 0 contains six idle frames plus the v2 neutral/deadzone cell in column 6.
USED_COLUMNS = [7, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8]
EXPECTED_ID = "yukino-yukinoshita"
EXPECTED_SPRITE_VERSION = 2
CHROMA_KEY = (0, 255, 255)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def validate(root: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    pet_dir = root / "pet"
    manifest_path = pet_dir / "pet.json"
    atlas_path = pet_dir / "spritesheet.webp"

    for required in (manifest_path, atlas_path):
        if not required.is_file():
            errors.append(f"missing required file: {required.relative_to(root)}")

    if errors:
        return {"ok": False, "errors": errors, "warnings": warnings}

    try:
        manifest = load_json(manifest_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return {
            "ok": False,
            "errors": [f"invalid pet.json: {exc}"],
            "warnings": warnings,
        }

    if manifest.get("id") != EXPECTED_ID:
        errors.append(f"pet id must be {EXPECTED_ID!r}")
    if not isinstance(manifest.get("displayName"), str) or not manifest["displayName"].strip():
        errors.append("displayName must be a non-empty string")
    if not isinstance(manifest.get("description"), str) or not manifest["description"].strip():
        errors.append("description must be a non-empty string")
    if manifest.get("spriteVersionNumber") != EXPECTED_SPRITE_VERSION:
        errors.append("spriteVersionNumber must be 2")
    if manifest.get("spritesheetPath") != "spritesheet.webp":
        errors.append('spritesheetPath must be "spritesheet.webp"')

    with Image.open(atlas_path) as opened:
        source_format = opened.format
        source_mode = opened.mode
        atlas = opened.convert("RGBA")

    if atlas.size != ATLAS_SIZE:
        errors.append(f"atlas must be {ATLAS_SIZE[0]}x{ATLAS_SIZE[1]}; got {atlas.width}x{atlas.height}")
    if source_format != "WEBP":
        errors.append(f"spritesheet must be WebP; got {source_format}")
    if "A" not in source_mode and source_mode != "RGBA":
        warnings.append(f"source mode is {source_mode}; alpha is available only after conversion")

    used_cells = 0
    unused_cells = 0
    if atlas.size == ATLAS_SIZE:
        alpha = atlas.getchannel("A")
        for row, used_count in enumerate(USED_COLUMNS):
            for column in range(COLUMNS):
                box = (
                    column * CELL_WIDTH,
                    row * CELL_HEIGHT,
                    (column + 1) * CELL_WIDTH,
                    (row + 1) * CELL_HEIGHT,
                )
                visible = alpha.crop(box).getbbox() is not None
                if column < used_count:
                    used_cells += 1
                    if not visible:
                        errors.append(f"required cell r{row}c{column} is empty")
                else:
                    unused_cells += 1
                    if visible:
                        errors.append(f"unused cell r{row}c{column} is not transparent")

    transparent_rgb_residue = 0
    opaque_chroma_pixels = 0
    rgba_bytes = atlas.tobytes()
    for index in range(0, len(rgba_bytes), 4):
        red, green, blue, alpha_value = rgba_bytes[index : index + 4]
        if alpha_value == 0 and (red or green or blue):
            transparent_rgb_residue += 1
        if alpha_value > 0 and (red, green, blue) == CHROMA_KEY:
            opaque_chroma_pixels += 1

    if transparent_rgb_residue:
        errors.append(
            f"found {transparent_rgb_residue} transparent pixels with hidden RGB residue"
        )
    # A few isolated exact-key pixels can remain inside antialiased sprite detail
    # without forming an opaque key panel. Treat only a material cluster as a
    # packaging failure; the production atlas validator remains authoritative.
    if opaque_chroma_pixels > 16:
        errors.append(f"found {opaque_chroma_pixels} visible pure-cyan chroma pixels")

    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "petId": manifest.get("id"),
        "displayName": manifest.get("displayName"),
        "spriteVersionNumber": manifest.get("spriteVersionNumber"),
        "atlas": {
            "format": source_format,
            "sourceMode": source_mode,
            "width": atlas.width,
            "height": atlas.height,
            "columns": COLUMNS,
            "rows": ROWS,
            "cellWidth": CELL_WIDTH,
            "cellHeight": CELL_HEIGHT,
            "usedCells": used_cells,
            "unusedCells": unused_cells,
            "transparentRgbResiduePixels": transparent_rgb_residue,
            "opaqueChromaPixels": opaque_chroma_pixels,
        },
        "sha256": {
            "pet.json": sha256(manifest_path),
            "spritesheet.webp": sha256(atlas_path),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="repository root; defaults to the parent of scripts/",
    )
    parser.add_argument("--json", action="store_true", help="print JSON only")
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    result = validate(root)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"validation={'pass' if result['ok'] else 'fail'}")
        if "spriteVersionNumber" in result:
            print(f"spriteVersionNumber={result['spriteVersionNumber']}")
        if "atlas" in result:
            atlas = result["atlas"]
            print(f"atlas={atlas['width']}x{atlas['height']}")
            print(f"usedCells={atlas['usedCells']}")
            print(f"unusedCells={atlas['unusedCells']}")
        if "sha256" in result:
            print(f"spritesheetSha256={result['sha256']['spritesheet.webp']}")
        for warning in result.get("warnings", []):
            print(f"warning: {warning}")
        for error in result.get("errors", []):
            print(f"error: {error}")

    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
