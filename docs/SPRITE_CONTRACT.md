# Codex v2 sprite contract

## Atlas geometry

| Property | Value |
| --- | ---: |
| Columns | 8 |
| Rows | 11 |
| Cell width | 192 px |
| Cell height | 208 px |
| Atlas width | 1536 px |
| Atlas height | 2288 px |
| Sprite version | 2 |
| Format | Lossless RGBA WebP |

The runtime manifest is `pet/pet.json`:

```json
{
  "id": "yukino-yukinoshita",
  "displayName": "雪之下雪乃",
  "description": "...",
  "spriteVersionNumber": 2,
  "spritesheetPath": "spritesheet.webp"
}
```

Omitting `spriteVersionNumber: 2` causes a v2 atlas to be interpreted using the
older nine-row contract.

## Standard rows

| Row | State | Used columns | Default timing |
| ---: | --- | --- | --- |
| 0 | idle | 0–5, plus neutral cell 6 | 280, 110, 110, 140, 140, 320 ms |
| 1 | running-right | 0–7 | 120 ms each, final 220 ms |
| 2 | running-left | 0–7 | 120 ms each, final 220 ms |
| 3 | waving | 0–3 | 140 ms each, final 280 ms |
| 4 | jumping / hover | 0–4 | 140 ms each, final 280 ms |
| 5 | failed | 0–7 | 140 ms each, final 240 ms |
| 6 | waiting | 0–5 | 150 ms each, final 260 ms |
| 7 | running | 0–5 | 120 ms each, final 220 ms |
| 8 | review | 0–5 | 150 ms each, final 280 ms |

The extended v2 atlas uses row 0, column 6 as the neutral/deadzone fallback;
row 0, column 7 remains unused. Every other unused cell after a standard row's
final used column must have zero visible alpha. Row 4 cannot be expanded to
eight visible cells without changing the application contract.

These timings are runtime/preview contract values, not package-level options.
`pet.json` does not provide a supported action-speed field. To slow the
perceived action while staying compatible, consecutive used cells may hold the
same key pose with small secondary changes such as a blink or hair settle.

## Runtime repeat behavior

In stock Codex desktop build `26.721.41059`, every non-idle state is played as three
complete copies of its row and then falls back to the slow idle loop while the
state remains unchanged:

```text
frames = row + row + row + slowIdle
loopStart = start of slowIdle
```

This explains why pointer hover appears to play three times. The repeat count
is owned by the renderer and cannot be changed through `pet.json` or atlas
metadata. Approximate time spent in the three action copies is:

| State | One row cycle | Three runtime copies |
| --- | ---: | ---: |
| waving | 700 ms | 2.10 s |
| jumping / hover | 840 ms | 2.52 s |
| failed | 1.22 s | 3.66 s |
| waiting | 1.01 s | 3.03 s |
| running | 820 ms | 2.46 s |
| review | 1.03 s | 3.09 s |
| running-left / running-right | 1.06 s | 3.18 s |

The optional macOS runtime patch in `scripts/patch_codex_pet_runtime.py` changes
this specific build to one row cycle with all non-idle frame durations doubled,
then enters the same slow idle loop. The atlas dimensions, used cells, and
manifest remain unchanged.

`scripts/generate_runtime_showcase.py` renders these patched timings directly
from the final atlas into `previews/runtime-patched-showcase.gif`; each panel's
character area remains the native `192x208` cell size.

## Look rows

Row 9:

```text
000, 022.5, 045, 067.5, 090, 112.5, 135, 157.5
```

Row 10:

```text
180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5
```

Degrees advance clockwise in viewer/screen coordinates:

- `000` = up;
- `090` = screen-right;
- `180` = down;
- `270` = screen-left.

Neutral/front is not a direction cell. It falls back to the normal idle frame
inside the pointer deadzone.

## Transparency rules

- Used cells must contain a connected, readable sprite.
- Unused cells must be fully transparent.
- Hidden RGB under alpha zero should be cleared.
- Opaque chroma-key background panels or material key-color clusters are invalid;
  a few isolated edge-color coincidences are reviewed against the production
  validator rather than treated as an automatic failure.
- No cast shadows, floor patches, glow, scenery, labels, grids, or detached
  effects.
- Hair, ribbons, tears, and other small details must remain attached to the
  main sprite or be intentionally connected effects.

## Resolution and clarity

The runtime cell is fixed at `192x208`; a doubled atlas is not a compatible
clarity upgrade. Improve readability at source level:

- generate at high resolution;
- downsample once;
- keep crisp cel edges;
- simplify tiny hair, plaid, and fabric noise;
- strengthen eye, eyebrow, eyelid, mouth, ribbon, piping, hand, and shoe
  landmarks;
- save WebP losslessly.
