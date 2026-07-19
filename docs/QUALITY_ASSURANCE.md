# Quality assurance

## Release gates

A release is acceptable only when:

- `pet.json` parses and declares sprite version 2;
- the atlas is exactly `1536x2288` RGBA;
- all required cells are non-empty;
- every unused standard-row cell is transparent;
- no material opaque pure-cyan background panel or key-color cluster remains;
- transparent pixels do not retain hidden RGB residue;
- standard-row state semantics remain correct;
- motion previews have no clipping, scale popping, reversed gait, or inert
  loops;
- four look cardinals are unmistakable;
- the sixteen-direction loop has no visible reversal or registration jump;
- independent visual review passes.

## Portable validator

Run:

```bash
python scripts/validate_pet.py
```

The script validates the distributable repository without depending on the
local pet-generation skill installation.

## Included evidence

| File | Evidence |
| --- | --- |
| `qa/validation.json` | Final v2 dimensions, alpha and atlas validation. |
| `qa/chroma-despill.json` | Deterministic edge-local chroma cleanup. |
| `qa/direction-blind-validation.json` | Three-reviewer blind axis consensus and hard cardinal gates. |
| `qa/direction-semantics.json` | Labeled verdict for every look direction. |
| `qa/look-continuity.json` | Adjacent direction metrics and reviewed warnings. |
| `qa/hover-final-visual-qa.json` | Independent approval of the repaired hover animation and clarity. |
| `qa/stable-slots-resolution.json` | Explanation and approval of stable-slot extraction. |

## Current accepted warnings

Some intermediate mouse directions close to a principal axis are visually
subtle. Blind reviewers may classify an individual horizontal or vertical
component as ambiguous. These are accepted only because:

- all four cardinals passed hard gates;
- labeled normal-size review confirms the intended quadrant;
- the ordered loop remains clockwise;
- there is no visible reversal, snap, identity change, or baseline jump.

Metrics are review evidence, not automatic failures. A numerical outlier is a
failure only when normal-size playback shows a conspicuous defect.

## Visual review checklist

### Identity

- normal 6.5–7-head proportions;
- consistent face, blue-gray eyes, long dark hair, red ribbons;
- consistent black blazer, white piping, red bow, plaid skirt, socks, shoes;
- no chibi or mascot-doll drift.

### Hover row

- five frames, not eight;
- no airborne feet;
- no celebratory smile or exaggerated excitement;
- subtle notice, recoil, side-eye/blush, and recovery;
- stable-slot motion is smooth and unclipped;
- facial and uniform details remain readable at `192x208`.

### Directions

- 000 up;
- 090 screen-right;
- 180 down;
- 270 screen-left;
- diagonals advance smoothly between cardinals;
- `337.5 → 000` closes the loop without a visible snap.

## Regression policy

For a targeted row repair, compare the old and new atlases row by row. Rows
outside the requested change should be pixel-identical whenever possible.
The hover repair release changed only row 4; rows 0–3 and 5–10 remained
unchanged.
