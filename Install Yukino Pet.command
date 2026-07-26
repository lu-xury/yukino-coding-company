#!/bin/zsh
cd "$(dirname "$0")"
./install-to-codex.sh
echo
echo "Optional: patch Codex desktop to play pet interactions once at half speed."
echo "This modifies the installed application bundle and changes its vendor signature."
read -q "REPLY?Apply the version-locked, restorable runtime patch? [y/N] "
echo
if [[ "$REPLY" == [Yy] ]]; then
  python3 scripts/patch_codex_pet_runtime.py apply --acknowledge-signature-change
else
  echo "Runtime patch skipped."
fi
echo
read -k 1 "?Press any key to close..."
