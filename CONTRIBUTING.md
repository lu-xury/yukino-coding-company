# Contributing

Thank you for helping improve the project. Contributions should preserve the
pet's identity, Codex v2 compatibility, restrained character acting, and the
repository's licensing boundary.

## Before opening a change

1. Read [ASSET_NOTICE.md](ASSET_NOTICE.md).
2. Read [docs/SPRITE_CONTRACT.md](docs/SPRITE_CONTRACT.md).
3. Read [docs/INTERACTION_DESIGN.md](docs/INTERACTION_DESIGN.md).
4. Do not add official screenshots, scans, logos, subtitles, or copied source
   artwork.
5. Do not claim that a character-derived contribution is MIT-licensed.

## Development setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/validate_pet.py
```

## Pull request expectations

- Explain the user-facing behavior being changed.
- Identify affected atlas rows and frame counts.
- Preserve `spriteVersionNumber: 2` and the exact `1536x2288` dimensions.
- Include an updated contact sheet or focused preview for visual changes.
- Run `python scripts/validate_pet.py`.
- Keep unused cells fully transparent.
- Avoid unrelated formatting or generated-file churn.
- Update `CHANGELOG.md` for user-visible changes.

## Interaction changes

The character should remain composed, intelligent, cool, and restrained.
Prefer eye, eyebrow, eyelid, head, hair, shoulder, and small posture changes
over exaggerated body motion. The fixed five-frame hover row must not become
an airborne celebratory jump.

## Commit style

Short imperative subjects are preferred:

```text
docs: clarify manual installation
fix: preserve hover baseline
qa: tighten unused-cell validation
```
