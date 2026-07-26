# Project overview

## Purpose

`yukino-coding-company` packages a validated Codex v2 animated pet inspired
by Yukinoshita Yukino. The project prioritizes:

- faithful normal-proportioned anime presentation;
- restrained galgame-style acting;
- readable behavior at the native `192x208` cell size;
- deterministic atlas structure and transparency;
- reproducible installation and validation;
- explicit separation between open-source tooling and character-derived art.

## Non-goals

- Reproducing or redistributing official artwork.
- Claiming official endorsement or ownership of the character.
- Creating a chibi, mascot-doll, or exaggerated comedy interpretation.
- Changing Codex behavior or task execution; a pet changes appearance only.
- Supporting arbitrary atlas sizes outside the Codex v2 contract.

## Runtime package

Only two files are required at runtime:

```text
pet/pet.json
pet/spritesheet.webp
```

They are installed together under:

```text
~/.codex/pets/yukino-yukinoshita/
```

`pet.json` identifies the pet, declares sprite version 2, and points to the
sprite sheet. `spritesheet.webp` is a lossless RGBA atlas containing standard
state animations and mouse-look directions.

## Repository layers

| Layer | Purpose | Runtime required |
| --- | --- | --- |
| `pet/` | Installable manifest and atlas | Yes |
| `previews/` | Human visual review | No |
| `qa/` | Machine and independent QA evidence | No |
| `scripts/` | Portable release validation | No |
| `docs/` | Design and maintenance knowledge | No |
| `.github/` | CI and contribution workflow | No |

## Data flow

```text
pet.json + spritesheet.webp
          │
          ├── scripts/validate_pet.py
          │     ├── manifest checks
          │     ├── atlas geometry checks
          │     ├── used/unused cell checks
          │     └── transparency/chroma checks
          │
          └── ~/.codex/pets/yukino-yukinoshita/
                    │
                    ├── Settings > Pets > Refresh
                    ├── select 雪之下雪乃
                    └── /pet or Wake Pet
```

## Quality status

The current release has:

- an exact `1536x2288` RGBA WebP atlas;
- `spriteVersionNumber: 2`;
- no structural validation errors or warnings;
- no opaque chroma-key panels;
- required standard-row frame counts;
- passing hard cardinal direction blind tests;
- reviewed intermediate direction warnings;
- independent approval of all six repaired event-action rows at native size;
- raised-hand, bent-knee refusal, head-down failure, open-palm crouch,
  waist-bend, and foreground peace-sign silhouettes
  that remain readable under the fixed runtime timing;
- documented renderer behavior showing three copies of every non-idle action
  before the slow idle loop;
- pixel regression evidence showing that only rows 3–8 changed;
- pixel-identical PNG and lossless WebP outputs during production QA.

See [QUALITY_ASSURANCE.md](QUALITY_ASSURANCE.md) for evidence and acceptance
policy.
