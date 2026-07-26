# yukino-coding-company

[中文说明](README.md) · [Installation](docs/INSTALLATION.md) · [Interaction design](docs/INTERACTION_DESIGN.md)

An unofficial, non-commercial Yukinoshita Yukino-inspired animated pet for Codex. It uses the Codex v2 8×11 sprite contract and normal anime proportions, with large pose-hold event silhouettes readable at native size: raised-hand greeting, bent-knee refusal, head-down failure, crouched open-palm waiting, waist-bent inspection, and an arms-crossed peace-sign finish.

## Install with a coding agent

Send the following instruction to Codex, Claude Code, Cursor Agent, or another terminal-capable coding agent:

```text
Install the Codex custom pet from git@github.com:lu-xury/yukino-coding-company.git.
Clone or safely update the repository, create a Python virtual environment, install requirements-dev.txt, and run python scripts/validate_pet.py. Only if validation passes, copy pet/pet.json and pet/spritesheet.webp into ~/.codex/pets/yukino-yukinoshita/. Verify spriteVersionNumber is 2, the atlas is 1536x2288, and source/install SHA-256 hashes match. Do not modify other pets. Ask before requesting permissions to write under ~/.codex. Finally tell me to open Settings > Pets, click Refresh, select Yukinoshita Yukino, and use /pet or Wake Pet.
```

## Manual installation

On macOS, double-click `Install Yukino Pet.command`, or install only the pet
files from Terminal with:

```bash
./install-to-codex.sh
```

The double-click entry asks whether to apply the version-locked runtime patch;
the shell installer itself only copies and verifies the pet package.

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

## Patched Runtime Showcase

![Single-play slow interaction showcase](previews/runtime-patched-showcase.gif)

This combined animation is generated directly from the final
`pet/spritesheet.webp`. Each event row plays once at twice the stock frame
duration and then returns to idle. Every character area remains at the native
`192x208` pet size.

Codex controls the fixed row timing and repeat count. The pet cannot change those values through its manifest, so the artwork uses large full-body silhouettes reinforced by high-contrast eyes, brows, ribbons, white piping, hands, and shoes at the native `192x208` size. For macOS Codex `26.721.41059`, this repository also includes a version-locked, restorable runtime patch that plays one action cycle at twice the stock frame duration.

## Operation-to-animation map

| Operation or task status | State | Yukino action |
| --- | --- | --- |
| First wake | `waving` | Holds a raised-hand greeting pose. |
| Pointer enters the pet | `jumping / hover` | Holds a wide-arm refusal pose. |
| Drag right / left | `running-right` / `running-left` | Runs in the drag direction. |
| Pointer moves around the pet | look rows | Eyes, head, neck, and hair follow sixteen directions. |
| Task is actively working | `running` | Holds a deep waist-bent inspection pose. |
| Codex needs input | `waiting` | Holds a compact crouch wait/thinking pose. |
| Task is blocked or fails | `failed` | Holds a head-down, drooped-shoulder failure pose. |
| Completed work has unread output | `review` | Holds an arms-crossed stance with a foreground victory/peace hand. |
| No event is active | `idle` | Breathes, blinks, and observes quietly. |

Stock Codex desktop builds play every non-idle row three times and then fall back to the slow idle loop. This repeat count and the per-frame durations are renderer-owned; `pet.json` has no supported override. The optional macOS patch changes the renderer to one cycle at `2x` frame duration. See [installation](docs/INSTALLATION.md), [interaction design](docs/INTERACTION_DESIGN.md), and the [sprite contract](docs/SPRITE_CONTRACT.md).

| Greeting | Grounded hover | Failed / blocked |
| --- | --- | --- |
| ![Greeting](previews/waving.gif) | ![Grounded hover](previews/hover.gif) | ![Failure](previews/failed.gif) |

| Waiting | Working | Review / approval |
| --- | --- | --- |
| ![Waiting](previews/waiting.gif) | ![Working](previews/working.gif) | ![Review](previews/review.gif) |

The preview GIFs show one atlas-row cycle for frame inspection. Stock Codex repeats it three times; the optional supported-build patch plays it once.

Regenerate the combined runtime showcase with:

```bash
python scripts/generate_runtime_showcase.py
```

## License boundary

Original scripts and documentation are MIT-licensed. Character-derived artwork is excluded from the MIT grant and is provided only as an unofficial, non-commercial fan work. See [ASSET_NOTICE.md](ASSET_NOTICE.md) and [LICENSE](LICENSE).
