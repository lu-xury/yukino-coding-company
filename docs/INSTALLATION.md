# Installation guide

This guide covers coding-agent installation, manual installation, selecting
the pet in the desktop app or CLI, upgrades, uninstall, and common failures.

## Recommended: ask a coding agent

Copy the complete prompt below into a coding agent that can run terminal
commands:

```text
Please install this Codex custom pet for me.

Repository: git@github.com:lu-xury/yukino-coding-company.git
HTTPS fallback: https://github.com/lu-xury/yukino-coding-company.git

Requirements:
1. Clone the repository into an appropriate local directory. If it already exists, safely update it with git pull --ff-only and do not overwrite uncommitted changes.
2. Create a temporary Python 3 virtual environment, install requirements-dev.txt, and run python scripts/validate_pet.py.
3. Continue only if validation passes.
4. Create ~/.codex/pets/yukino-yukinoshita.
5. Copy only pet/pet.json and pet/spritesheet.webp into that directory.
6. Verify spriteVersionNumber is 2, the atlas is 1536x2288, and source/install SHA-256 hashes match.
7. Do not modify or delete any other installed pet.
8. Ask for approval if writing under ~/.codex requires permission.
9. When finished, tell me to open Settings > Pets, click Refresh, select Yukinoshita Yukino, and use /pet or Wake Pet. For Codex CLI, tell me to use /pets or /pet.
```

## Requirements

- A Codex / ChatGPT desktop build with the Pets feature enabled, or an
  interactive Codex CLI with supported terminal graphics.
- Git.
- Python 3.10+ for local validation.
- Pillow, installed through `requirements-dev.txt`.

The pet itself does not execute Python. Python is only used to validate the
repository before installation.

## Clone

SSH:

```bash
git clone git@github.com:lu-xury/yukino-coding-company.git
cd yukino-coding-company
```

HTTPS:

```bash
git clone https://github.com/lu-xury/yukino-coding-company.git
cd yukino-coding-company
```

## Validate

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python scripts/validate_pet.py
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python scripts/validate_pet.py
```

Do not install when validation fails. Open an issue and include the validator
output, OS, Python version, and commit hash.

## Install locally

### macOS / Linux

```bash
PET_DIR="$HOME/.codex/pets/yukino-yukinoshita"
mkdir -p "$PET_DIR"
cp pet/pet.json "$PET_DIR/pet.json"
cp pet/spritesheet.webp "$PET_DIR/spritesheet.webp"
```

Verify:

```bash
shasum -a 256 pet/spritesheet.webp "$HOME/.codex/pets/yukino-yukinoshita/spritesheet.webp"
```

The two hashes must match.

### Windows PowerShell

```powershell
$petDir = Join-Path $HOME ".codex\pets\yukino-yukinoshita"
New-Item -ItemType Directory -Force -Path $petDir | Out-Null
Copy-Item pet\pet.json (Join-Path $petDir "pet.json") -Force
Copy-Item pet\spritesheet.webp (Join-Path $petDir "spritesheet.webp") -Force
Get-FileHash pet\spritesheet.webp -Algorithm SHA256
Get-FileHash (Join-Path $petDir "spritesheet.webp") -Algorithm SHA256
```

## Select and wake the pet

### Desktop app

1. Open or restart the Codex / ChatGPT desktop app.
2. Open the profile menu and choose **Pets**, or open **Settings > Pets**.
3. Click **Refresh** so locally installed pets are rescanned.
4. Select **雪之下雪乃**.
5. Enter `/pet`, or open the command menu and choose **Wake Pet**.
6. Enter `/pet` again, or choose **Tuck Away Pet**, to hide it.

The selected pet and its position should persist after reopening the app.

### Codex CLI

In an interactive CLI session:

```text
/pets
```

or:

```text
/pet
```

Choose **雪之下雪乃** from the picker. Use `/pets off` to disable terminal
pets.

Terminal rendering requires iTerm2 3.6+, Kitty graphics, or Sixel support.
Pets are unavailable inside tmux and Zellij. The Codex IDE extension does not
provide the pet picker or floating overlay.

## Update

```bash
cd yukino-coding-company
git status
git pull --ff-only
source .venv/bin/activate  # if the environment already exists
python scripts/validate_pet.py
cp pet/pet.json "$HOME/.codex/pets/yukino-yukinoshita/pet.json"
cp pet/spritesheet.webp "$HOME/.codex/pets/yukino-yukinoshita/spritesheet.webp"
```

Return to **Settings > Pets**, click **Refresh**, and reselect the pet if
necessary.

Never use `git reset --hard` to update a repository containing local work.

## Uninstall

Remove only this pet's directory:

```bash
rm -rf "$HOME/.codex/pets/yukino-yukinoshita"
```

Then open **Settings > Pets**, click **Refresh**, and choose another pet or the
default option. Review the path carefully before running the removal command.

## Web upload versus local v2 install

This repository packages a local Codex v2 atlas (`1536x2288`, 11 rows).
Current documented web **Upload pet** flows may use a different upload
contract. Do not resize or truncate this v2 atlas to satisfy a web upload UI;
install it locally under `~/.codex/pets` and use the desktop app or compatible
CLI picker.

## Troubleshooting

### The pet does not appear

- Confirm both files are directly inside
  `~/.codex/pets/yukino-yukinoshita/`.
- Confirm the filename is exactly `spritesheet.webp`.
- Confirm `pet.json` contains `"spriteVersionNumber": 2`.
- Run `python scripts/validate_pet.py` again.
- Click **Refresh** in **Settings > Pets**.
- Fully restart the desktop app.

### The pet is visible but not animated

- Check whether the operating system's reduced-motion setting is enabled.
- Use `/pet` or **Wake Pet** to wake the overlay.
- In the CLI, verify terminal graphics support and avoid tmux/Zellij.

### The old hover action is still shown

- Compare repository and installed SHA-256 hashes.
- Replace both `pet.json` and `spritesheet.webp`.
- Click **Refresh** and restart the app.

### Permission denied for `~/.codex`

Do not use broad permission changes such as `chmod -R 777`. Confirm ownership
of your home directory and ask your coding agent to request a scoped approval
for the two copy operations.

## Official product references

- <https://learn.chatgpt.com/docs/pets>
- <https://learn.chatgpt.com/docs/reference/settings#pets>
