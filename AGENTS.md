# Repository guidance for coding agents

## Scope

This repository packages one Codex v2 custom pet. Preserve the installable
files under `pet/` and keep documentation consistent with the current package.

## Required checks

Before finishing any change, run:

```bash
python scripts/validate_pet.py
```

For visual changes, also review `previews/contact-sheet.png` and the affected
GIF at native pet size.

## Hard constraints

- Atlas: 1536x2288, 8 columns, 11 rows, 192x208 cells.
- `spriteVersionNumber`: 2.
- Used cells by row: 7 (six idle plus neutral), 8, 8, 4, 5, 8, 6, 6, 6, 8, 8.
- Unused cells in standard rows must be transparent.
- Do not modify unrelated rows during a targeted animation repair.
- Do not add official copyrighted reference images.
- Do not describe character-derived art as MIT-licensed.
- Do not push, release, or modify external systems unless the user explicitly
  authorizes it.

## Documentation

Keep installation instructions in `README.md` and
`docs/INSTALLATION.md`. Keep interaction rationale in
`docs/INTERACTION_DESIGN.md`, and technical atlas details in
`docs/SPRITE_CONTRACT.md`.
