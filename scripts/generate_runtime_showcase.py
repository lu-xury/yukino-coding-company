#!/usr/bin/env python3
"""Generate the patched single-play runtime showcase from the final atlas."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


CELL_WIDTH = 192
CELL_HEIGHT = 208
ATLAS_COLUMNS = 8
LABEL_HEIGHT = 30
GRID_COLUMNS = 3
IDLE_HOLD_MS = 1400
FRAME_DURATION_MULTIPLIER = 2


@dataclass(frozen=True)
class Animation:
    label: str
    row: int
    frame_durations_ms: tuple[int, ...]

    @property
    def patched_durations_ms(self) -> tuple[int, ...]:
        return tuple(
            duration * FRAME_DURATION_MULTIPLIER
            for duration in self.frame_durations_ms
        )


ANIMATIONS = (
    Animation("招手  Waving", 3, (140, 140, 140, 280)),
    Animation("拒触  Hover", 4, (140, 140, 140, 140, 280)),
    Animation("失败  Failed", 5, (140, 140, 140, 140, 140, 140, 140, 240)),
    Animation("等待  Waiting", 6, (150, 150, 150, 150, 150, 260)),
    Animation("检查  Working", 7, (120, 120, 120, 120, 120, 220)),
    Animation("完成  Review", 8, (150, 150, 150, 150, 150, 280)),
)


def load_font(size: int) -> ImageFont.ImageFont:
    candidates = (
        Path("/System/Library/Fonts/PingFang.ttc"),
        Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    )
    for path in candidates:
        if path.is_file():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def checkerboard() -> Image.Image:
    image = Image.new("RGBA", (CELL_WIDTH, CELL_HEIGHT), (248, 248, 248, 255))
    draw = ImageDraw.Draw(image)
    square = 16
    for y in range(0, CELL_HEIGHT, square):
        for x in range(0, CELL_WIDTH, square):
            if (x // square + y // square) % 2:
                draw.rectangle(
                    (x, y, x + square - 1, y + square - 1),
                    fill=(232, 232, 232, 255),
                )
    return image


def atlas_cell(atlas: Image.Image, row: int, column: int) -> Image.Image:
    left = column * CELL_WIDTH
    top = row * CELL_HEIGHT
    return atlas.crop((left, top, left + CELL_WIDTH, top + CELL_HEIGHT))


def frame_at(
    frames: tuple[Image.Image, ...], durations: tuple[int, ...], time_ms: int
) -> Image.Image | None:
    elapsed = 0
    for frame, duration in zip(frames, durations, strict=True):
        elapsed += duration
        if time_ms < elapsed:
            return frame
    return None


def event_times() -> list[int]:
    times = {0}
    maximum_duration = 0
    for animation in ANIMATIONS:
        elapsed = 0
        for duration in animation.patched_durations_ms:
            elapsed += duration
            times.add(elapsed)
        maximum_duration = max(maximum_duration, elapsed)
    times.add(maximum_duration + IDLE_HOLD_MS)
    return sorted(times)


def render_panel(
    label: str,
    character: Image.Image,
    is_idle: bool,
    font: ImageFont.ImageFont,
    checker: Image.Image,
) -> Image.Image:
    panel = Image.new(
        "RGBA", (CELL_WIDTH, LABEL_HEIGHT + CELL_HEIGHT), (27, 30, 36, 255)
    )
    draw = ImageDraw.Draw(panel)
    draw.text((8, 5), label, font=font, fill=(255, 255, 255, 255))
    badge = "IDLE" if is_idle else "1× / 2×"
    badge_box = draw.textbbox((0, 0), badge, font=font)
    badge_width = badge_box[2] - badge_box[0]
    draw.text(
        (CELL_WIDTH - badge_width - 8, 5),
        badge,
        font=font,
        fill=(124, 220, 177, 255) if is_idle else (255, 196, 92, 255),
    )
    panel.alpha_composite(checker, (0, LABEL_HEIGHT))
    panel.alpha_composite(character, (0, LABEL_HEIGHT))
    return panel


def generate(atlas_path: Path, output_path: Path) -> None:
    with Image.open(atlas_path) as source:
        atlas = source.convert("RGBA")
    expected_size = (ATLAS_COLUMNS * CELL_WIDTH, 11 * CELL_HEIGHT)
    if atlas.size != expected_size:
        raise ValueError(f"unexpected atlas size: {atlas.size}, expected {expected_size}")

    idle_frame = atlas_cell(atlas, 0, 0)
    animation_frames = {
        animation.label: tuple(
            atlas_cell(atlas, animation.row, column)
            for column in range(len(animation.frame_durations_ms))
        )
        for animation in ANIMATIONS
    }
    times = event_times()
    frame_durations = [end - start for start, end in zip(times, times[1:])]
    rows = (len(ANIMATIONS) + GRID_COLUMNS - 1) // GRID_COLUMNS
    canvas_size = (
        GRID_COLUMNS * CELL_WIDTH,
        rows * (LABEL_HEIGHT + CELL_HEIGHT),
    )
    font = load_font(13)
    checker = checkerboard()
    rendered_frames: list[Image.Image] = []

    for time_ms in times[:-1]:
        canvas = Image.new("RGBA", canvas_size, (18, 20, 24, 255))
        for index, animation in enumerate(ANIMATIONS):
            character = frame_at(
                animation_frames[animation.label],
                animation.patched_durations_ms,
                time_ms,
            )
            is_idle = character is None
            panel = render_panel(
                animation.label,
                idle_frame if is_idle else character,
                is_idle,
                font,
                checker,
            )
            x = index % GRID_COLUMNS * CELL_WIDTH
            y = index // GRID_COLUMNS * (LABEL_HEIGHT + CELL_HEIGHT)
            canvas.alpha_composite(panel, (x, y))
        rendered_frames.append(
            canvas.convert(
                "P",
                palette=Image.Palette.ADAPTIVE,
                colors=160,
                dither=Image.Dither.NONE,
            )
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    rendered_frames[0].save(
        output_path,
        save_all=True,
        append_images=rendered_frames[1:],
        duration=frame_durations,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(f"showcase={output_path}")
    print(f"size={canvas_size[0]}x{canvas_size[1]}")
    print(f"frames={len(rendered_frames)}")
    print(f"duration_ms={sum(frame_durations)}")


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--atlas", type=Path, default=root / "pet" / "spritesheet.webp"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=root / "previews" / "runtime-patched-showcase.gif",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    generate(args.atlas, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
