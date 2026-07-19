# yukino-coding-company

[中文说明](README.md) · [Installation](docs/INSTALLATION.md) · [Interaction design](docs/INTERACTION_DESIGN.md)

An unofficial, non-commercial Yukinoshita Yukino-inspired animated pet for Codex. It uses the Codex v2 8×11 sprite contract, normal anime proportions, restrained galgame-style acting, and grounded pointer-hover behavior. Event actions hold their key pose across adjacent frames so reproach, waiting, focused work, and approval remain readable instead of flashing by.

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

Codex controls the fixed row timing. Perceived speed is improved by holding the same key pose across adjacent frames, not by adding unsupported timing fields. The artwork also emphasizes high-contrast eyes, brows, ribbons, white piping, hands, and shoes at the native `192x208` size.

| Greeting | Grounded hover | Failed / reproach |
| --- | --- | --- |
| ![Greeting](previews/waving.gif) | ![Grounded hover](previews/hover.gif) | ![Reproach](previews/failed.gif) |

| Waiting | Working | Review / approval |
| --- | --- | --- |
| ![Waiting](previews/waiting.gif) | ![Working](previews/working.gif) | ![Review](previews/review.gif) |

## License boundary

Original scripts and documentation are MIT-licensed. Character-derived artwork is excluded from the MIT grant and is provided only as an unofficial, non-commercial fan work. See [ASSET_NOTICE.md](ASSET_NOTICE.md) and [LICENSE](LICENSE).
