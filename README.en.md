# yukino-coding-company

[中文说明](README.md) · [Installation](docs/INSTALLATION.md) · [Interaction design](docs/INTERACTION_DESIGN.md)

An unofficial, non-commercial Yukinoshita Yukino-inspired animated pet for Codex. It uses the Codex v2 8×11 sprite contract and normal anime proportions, with event silhouettes that remain readable at native size: blushing head-shake refusal, hands-on-hips reprimand, crouched waiting, waist-bent inspection, and confident nodding approval.

## Install with a coding agent

Send the following instruction to Codex, Claude Code, Cursor Agent, or another terminal-capable coding agent:

```text
Install the Codex custom pet from git@github.com:lu-xury/yukino-coding-company.git.
Clone or safely update the repository, create a Python virtual environment, install requirements-dev.txt, and run python scripts/validate_pet.py. Only if validation passes, copy pet/pet.json and pet/spritesheet.webp into ~/.codex/pets/yukino-yukinoshita/. Verify spriteVersionNumber is 2, the atlas is 1536x2288, and source/install SHA-256 hashes match. Do not modify other pets. Ask before requesting permissions to write under ~/.codex. Finally tell me to open Settings > Pets, click Refresh, select Yukinoshita Yukino, and use /pet or Wake Pet.
```

## Manual installation

```bash
git clone git@github.com:lu-xury/yukino-coding-company.git
cd yukino-coding-company
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/validate_pet.py
mkdir -p ~/.codex/pets/yukino-yukinoshita
cp pet/pet.json pet/spritesheet.webp ~/.codex/pets/yukino-yukinoshita/
```

Then open **Settings > Pets**, click **Refresh**, select **Yukinoshita Yukino**, and enter `/pet` or choose **Wake Pet**. In Codex CLI, enter `/pets` or `/pet` to open the picker.

See [docs/INSTALLATION.md](docs/INSTALLATION.md) for Windows, updates, uninstall, and troubleshooting.

## Preview

![Contact sheet](previews/contact-sheet.png)

Codex controls the fixed row timing and repeat count. The pet cannot slow those values through its manifest, so the artwork uses large full-body silhouettes and repeat-friendly loops, reinforced by high-contrast eyes, brows, ribbons, white piping, hands, and shoes at the native `192x208` size.

## Operation-to-animation map

| Operation or task status | State | Yukino action |
| --- | --- | --- |
| First wake | `waving` | Raises an open hand and makes a small formal bow. |
| Pointer enters the pet | `jumping / hover` | Blushes, raises a stop palm, and shakes her head left–center–right. |
| Drag right / left | `running-right` / `running-left` | Runs in the drag direction. |
| Pointer moves around the pet | look rows | Eyes, head, neck, and hair follow sixteen directions. |
| Task is actively working | `running` | Bends from the waist to inspect work below and in front. |
| Codex needs input | `waiting` | Crouches and waits with one hand supporting her cheek. |
| Task is blocked or fails | `failed` | Plants both hands on her hips and leans forward to reprimand. |
| Completed work has unread output | `review` | Straightens with one hand on her hip and gives a deliberate nod. |
| No event is active | `idle` | Breathes, blinks, and observes quietly. |

Current Codex desktop builds play every non-idle row three times and then fall back to the slow idle loop. This repeat count and the per-frame durations are renderer-owned; `pet.json` has no supported override. See [interaction design](docs/INTERACTION_DESIGN.md) and the [sprite contract](docs/SPRITE_CONTRACT.md) for the exact mapping and timings.

| Greeting | Grounded hover | Failed / reproach |
| --- | --- | --- |
| ![Greeting](previews/waving.gif) | ![Grounded hover](previews/hover.gif) | ![Reproach](previews/failed.gif) |

| Waiting | Working | Review / approval |
| --- | --- | --- |
| ![Waiting](previews/waiting.gif) | ![Working](previews/working.gif) | ![Review](previews/review.gif) |

The preview GIFs show one atlas-row cycle for frame inspection. Codex desktop repeats that cycle three times at runtime.

## License boundary

Original scripts and documentation are MIT-licensed. Character-derived artwork is excluded from the MIT grant and is provided only as an unofficial, non-commercial fan work. See [ASSET_NOTICE.md](ASSET_NOTICE.md) and [LICENSE](LICENSE).
