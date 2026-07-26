#!/usr/bin/env python3
"""Patch one supported Codex desktop build for slower, single-play pet actions."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import plistlib
import shutil
import struct
import sys
from pathlib import Path


SUPPORTED_VERSION = "26.721.41059"
SUPPORTED_BUILD = "5848"
TARGET_ASAR_PATH = "webview/assets/codex-avatar-rFd6-NsG.js"
ASAR_INTEGRITY_KEY = "Resources/app.asar"


def padded_replacement(original: bytes, replacement: bytes) -> bytes:
    if len(replacement) > len(original):
        raise ValueError("replacement is longer than original")
    return replacement + b" " * (len(original) - len(replacement))


PATCHES = (
    (
        b"let r=[...n,...n,...n];",
        padded_replacement(b"let r=[...n,...n,...n];", b"let r=[...n];"),
    ),
    (b"failed:j(5,8,140,240)", b"failed:j(5,8,280,480)"),
    (b"jumping:j(4,5,140,280)", b"jumping:j(4,5,280,560)"),
    (b"review:j(8,6,150,280)", b"review:j(8,6,300,560)"),
    (b"running:j(7,6,120,220)", b"running:j(7,6,240,440)"),
    (
        b'"running-left":j(2,8,120,220)',
        b'"running-left":j(2,8,240,440)',
    ),
    (
        b'"running-right":j(1,8,120,220)',
        b'"running-right":j(1,8,240,440)',
    ),
    (b"waving:j(3,4,140,280)", b"waving:j(3,4,280,560)"),
    (b"waiting:j(6,6,150,260)", b"waiting:j(6,6,300,520)"),
)


class PatchError(RuntimeError):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_plist(path: Path) -> dict:
    try:
        return plistlib.loads(path.read_bytes())
    except (OSError, plistlib.InvalidFileException) as error:
        raise PatchError(f"cannot read plist: {path}: {error}") from error


def read_asar(asar_path: Path) -> tuple[bytes, dict, int]:
    try:
        with asar_path.open("rb") as archive:
            prefix = archive.read(16)
            if len(prefix) != 16:
                raise PatchError("ASAR header is truncated")
            pickle_payload_size, header_size, inner_payload_size, json_size = (
                struct.unpack("<IIII", prefix)
            )
            if pickle_payload_size != 4:
                raise PatchError("unsupported ASAR pickle prefix")
            if inner_payload_size + 4 != header_size:
                raise PatchError("unexpected ASAR inner header size")
            header_json = archive.read(json_size)
    except OSError as error:
        raise PatchError(f"cannot read ASAR: {asar_path}: {error}") from error

    try:
        header = json.loads(header_json)
    except json.JSONDecodeError as error:
        raise PatchError(f"invalid ASAR JSON header: {error}") from error
    return header_json, header, 8 + header_size


def find_entry(header: dict, relative_path: str) -> dict:
    entry = header
    for part in relative_path.split("/"):
        files = entry.get("files")
        if not isinstance(files, dict) or part not in files:
            raise PatchError(f"ASAR entry not found: {relative_path}")
        entry = files[part]
    return entry


def read_target(
    asar_path: Path, header: dict, data_offset: int
) -> tuple[bytes, dict, int]:
    entry = find_entry(header, TARGET_ASAR_PATH)
    try:
        size = int(entry["size"])
        target_offset = data_offset + int(entry["offset"])
    except (KeyError, TypeError, ValueError) as error:
        raise PatchError("target ASAR entry has invalid size or offset") from error
    try:
        with asar_path.open("rb") as archive:
            archive.seek(target_offset)
            target = archive.read(size)
    except OSError as error:
        raise PatchError(f"cannot read renderer chunk: {error}") from error
    if len(target) != size:
        raise PatchError("renderer chunk is truncated")
    return target, entry, target_offset


def runtime_state(target: bytes) -> str:
    stock_counts = [target.count(stock) for stock, _ in PATCHES]
    patched_counts = [target.count(patched) for _, patched in PATCHES]
    if all(count == 1 for count in stock_counts) and all(
        count == 0 for count in patched_counts
    ):
        return "stock"
    if all(count == 0 for count in stock_counts) and all(
        count == 1 for count in patched_counts
    ):
        return "patched"
    raise PatchError(
        "renderer chunk is neither the supported stock nor patched version: "
        f"stock_counts={stock_counts}, patched_counts={patched_counts}"
    )


def plist_integrity_hash(plist: dict) -> str:
    try:
        integrity = plist["ElectronAsarIntegrity"][ASAR_INTEGRITY_KEY]
        if integrity["algorithm"] != "SHA256":
            raise PatchError("unsupported Electron ASAR integrity algorithm")
        return integrity["hash"]
    except (KeyError, TypeError) as error:
        raise PatchError("ElectronAsarIntegrity metadata is missing") from error


def verify_integrity(
    plist: dict, header_json: bytes, entry: dict, target: bytes
) -> None:
    expected_header_hash = plist_integrity_hash(plist)
    actual_header_hash = sha256(header_json)
    if actual_header_hash != expected_header_hash:
        raise PatchError(
            "top-level ASAR integrity mismatch: "
            f"plist={expected_header_hash}, actual={actual_header_hash}"
        )

    try:
        integrity = entry["integrity"]
        expected_target_hash = integrity["hash"]
        blocks = integrity["blocks"]
        block_size = int(integrity["blockSize"])
    except (KeyError, TypeError, ValueError) as error:
        raise PatchError("renderer chunk integrity metadata is missing") from error
    actual_target_hash = sha256(target)
    if actual_target_hash != expected_target_hash:
        raise PatchError(
            "renderer chunk integrity mismatch: "
            f"header={expected_target_hash}, actual={actual_target_hash}"
        )
    actual_blocks = [
        sha256(target[offset : offset + block_size])
        for offset in range(0, len(target), block_size)
    ]
    if actual_blocks != blocks:
        raise PatchError("renderer chunk block hashes do not match")


def app_paths(app_path: Path) -> tuple[Path, Path]:
    return (
        app_path / "Contents" / "Info.plist",
        app_path / "Contents" / "Resources" / "app.asar",
    )


def inspect_app(app_path: Path) -> dict:
    plist_path, asar_path = app_paths(app_path)
    plist = read_plist(plist_path)
    version = str(plist.get("CFBundleShortVersionString", ""))
    build = str(plist.get("CFBundleVersion", ""))
    header_json, header, data_offset = read_asar(asar_path)
    target, entry, target_offset = read_target(asar_path, header, data_offset)
    state = runtime_state(target)
    verify_integrity(plist, header_json, entry, target)
    return {
        "plist_path": plist_path,
        "asar_path": asar_path,
        "plist": plist,
        "version": version,
        "build": build,
        "header_json": header_json,
        "header": header,
        "entry": entry,
        "target": target,
        "target_offset": target_offset,
        "state": state,
    }


def require_supported_build(info: dict) -> None:
    if (info["version"], info["build"]) != (SUPPORTED_VERSION, SUPPORTED_BUILD):
        raise PatchError(
            "unsupported Codex build: "
            f"{info['version']} ({info['build']}); expected "
            f"{SUPPORTED_VERSION} ({SUPPORTED_BUILD})"
        )


def backup_paths(backup_root: Path, info: dict) -> tuple[Path, Path]:
    backup_dir = backup_root / f"{info['version']}-{info['build']}"
    return backup_dir / "Info.plist", backup_dir / "app.asar"


def create_backup(backup_root: Path, info: dict) -> tuple[Path, Path]:
    backup_plist, backup_asar = backup_paths(backup_root, info)
    backup_plist.parent.mkdir(parents=True, exist_ok=True)
    if backup_plist.exists() or backup_asar.exists():
        if not backup_plist.is_file() or not backup_asar.is_file():
            raise PatchError(f"incomplete backup exists: {backup_plist.parent}")
        backup_info = inspect_app_from_files(backup_plist, backup_asar)
        if backup_info["state"] != "stock":
            raise PatchError("existing backup is not the stock runtime")
        return backup_plist, backup_asar
    shutil.copy2(info["plist_path"], backup_plist)
    shutil.copy2(info["asar_path"], backup_asar)
    backup_info = inspect_app_from_files(backup_plist, backup_asar)
    if backup_info["state"] != "stock":
        raise PatchError("new backup verification failed")
    return backup_plist, backup_asar


def inspect_app_from_files(plist_path: Path, asar_path: Path) -> dict:
    plist = read_plist(plist_path)
    header_json, header, data_offset = read_asar(asar_path)
    target, entry, target_offset = read_target(asar_path, header, data_offset)
    state = runtime_state(target)
    verify_integrity(plist, header_json, entry, target)
    return {
        "plist_path": plist_path,
        "asar_path": asar_path,
        "plist": plist,
        "version": str(plist.get("CFBundleShortVersionString", "")),
        "build": str(plist.get("CFBundleVersion", "")),
        "header_json": header_json,
        "header": header,
        "entry": entry,
        "target": target,
        "target_offset": target_offset,
        "state": state,
    }


def patch_target(target: bytes) -> bytes:
    patched = target
    for stock, replacement in PATCHES:
        if patched.count(stock) != 1:
            raise PatchError(f"expected one renderer pattern: {stock!r}")
        patched = patched.replace(stock, replacement, 1)
    if len(patched) != len(target):
        raise PatchError("renderer patch changed the ASAR entry size")
    return patched


def apply_patch(info: dict, backup_root: Path) -> None:
    require_supported_build(info)
    if info["state"] == "patched":
        print("runtime_patch=already_applied")
        return
    backup_plist, backup_asar = create_backup(backup_root, info)

    patched_target = patch_target(info["target"])
    old_target_hash = info["entry"]["integrity"]["hash"]
    new_target_hash = sha256(patched_target)
    old_hash_bytes = old_target_hash.encode("ascii")
    new_hash_bytes = new_target_hash.encode("ascii")
    expected_hash_occurrences = 1 + len(info["entry"]["integrity"]["blocks"])
    if info["header_json"].count(old_hash_bytes) != expected_hash_occurrences:
        raise PatchError("renderer integrity hashes are not unique in the ASAR header")
    patched_header = info["header_json"].replace(old_hash_bytes, new_hash_bytes)
    if len(patched_header) != len(info["header_json"]):
        raise PatchError("ASAR header size changed")
    old_header_hash = sha256(info["header_json"])
    new_header_hash = sha256(patched_header)

    try:
        with info["asar_path"].open("r+b") as archive:
            archive.seek(16)
            archive.write(patched_header)
            archive.seek(info["target_offset"])
            archive.write(patched_target)
            archive.flush()
            os.fsync(archive.fileno())
        plist_bytes = info["plist_path"].read_bytes()
        old_header_hash_bytes = old_header_hash.encode("ascii")
        if plist_bytes.count(old_header_hash_bytes) != 1:
            raise PatchError("expected one ASAR hash in Info.plist")
        patched_plist = plist_bytes.replace(
            old_header_hash_bytes, new_header_hash.encode("ascii"), 1
        )
        info["plist_path"].write_bytes(patched_plist)
    except OSError as error:
        raise PatchError(f"cannot write Codex application files: {error}") from error

    verified = inspect_app_from_files(info["plist_path"], info["asar_path"])
    if verified["state"] != "patched":
        raise PatchError("runtime patch verification failed")
    print("runtime_patch=applied")
    print("interaction_repeats=1")
    print("interaction_frame_duration=2x")
    print("restart_required=true")
    print("privacy_permissions_may_need_reapproval=true")
    print(f"backup_plist={backup_plist}")
    print(f"backup_asar={backup_asar}")


def restore_patch(info: dict, backup_root: Path) -> None:
    require_supported_build(info)
    if info["state"] == "stock":
        print("runtime_patch=already_restored")
        return
    backup_plist, backup_asar = backup_paths(backup_root, info)
    if not backup_plist.is_file() or not backup_asar.is_file():
        raise PatchError(f"backup is missing: {backup_plist.parent}")
    backup_info = inspect_app_from_files(backup_plist, backup_asar)
    require_supported_build(backup_info)
    if backup_info["state"] != "stock":
        raise PatchError("backup is not the stock runtime")
    try:
        shutil.copy2(backup_asar, info["asar_path"])
        shutil.copy2(backup_plist, info["plist_path"])
    except OSError as error:
        raise PatchError(f"cannot restore Codex application files: {error}") from error
    verified = inspect_app(info["plist_path"].parents[1])
    if verified["state"] != "stock":
        raise PatchError("runtime restore verification failed")
    print("runtime_patch=restored")
    print("restart_required=true")


def print_status(info: dict) -> None:
    print(f"codex_version={info['version']}")
    print(f"codex_build={info['build']}")
    print(f"runtime_patch={info['state']}")
    print(f"renderer_chunk={TARGET_ASAR_PATH}")
    print(f"renderer_sha256={sha256(info['target'])}")
    print(f"asar_header_sha256={sha256(info['header_json'])}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("check", "apply", "restore"))
    parser.add_argument(
        "--app",
        type=Path,
        default=Path("/Applications/ChatGPT.app"),
        help="Codex / ChatGPT application bundle",
    )
    parser.add_argument(
        "--backup-root",
        type=Path,
        default=Path.home() / ".codex" / "backups" / "yukino-pet-runtime",
        help="directory for original runtime backups",
    )
    parser.add_argument(
        "--acknowledge-signature-change",
        action="store_true",
        help="confirm that patching the application changes its vendor signature",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        info = inspect_app(args.app)
        if args.action == "check":
            print_status(info)
        elif args.action == "apply":
            if not args.acknowledge_signature_change:
                raise PatchError(
                    "apply requires --acknowledge-signature-change because the "
                    "installed application bundle is modified"
                )
            apply_patch(info, args.backup_root)
        else:
            restore_patch(info, args.backup_root)
    except PatchError as error:
        print(f"error={error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
