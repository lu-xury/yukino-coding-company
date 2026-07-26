#!/bin/zsh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SRC_JSON="$ROOT/pet/pet.json"
SRC_SHEET="$ROOT/pet/spritesheet.webp"
DEST_DIR="$HOME/.codex/pets/yukino-yukinoshita"

if [[ ! -f "$SRC_JSON" || ! -f "$SRC_SHEET" ]]; then
  echo "missing pet files under $ROOT/pet" >&2
  exit 1
fi

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "this convenience installer currently supports macOS only" >&2
  exit 1
fi

python3 - "$SRC_JSON" <<'PY'
import json
import sys
from pathlib import Path

pet = json.loads(Path(sys.argv[1]).read_text())
assert pet.get("id") == "yukino-yukinoshita"
assert pet.get("spriteVersionNumber") == 2
print(f"id={pet['id']}")
print(f"displayName={pet['displayName']}")
print(f"spriteVersionNumber={pet['spriteVersionNumber']}")
PY

WIDTH="$(sips -g pixelWidth "$SRC_SHEET" | awk '/pixelWidth/ {print $2}')"
HEIGHT="$(sips -g pixelHeight "$SRC_SHEET" | awk '/pixelHeight/ {print $2}')"
if [[ "$WIDTH" != "1536" || "$HEIGHT" != "2288" ]]; then
  echo "invalid atlas dimensions: ${WIDTH}x${HEIGHT}" >&2
  exit 1
fi

mkdir -p "$DEST_DIR"
cp -f "$SRC_JSON" "$DEST_DIR/pet.json"
cp -f "$SRC_SHEET" "$DEST_DIR/spritesheet.webp"

if ! cmp -s "$SRC_JSON" "$DEST_DIR/pet.json"; then
  echo "installed pet.json does not match source" >&2
  exit 1
fi
if ! cmp -s "$SRC_SHEET" "$DEST_DIR/spritesheet.webp"; then
  echo "installed spritesheet does not match source" >&2
  exit 1
fi

SHA="$(shasum -a 256 "$DEST_DIR/spritesheet.webp" | awk '{print $1}')"
echo "atlas=${WIDTH}x${HEIGHT}"
echo "sha_match=true"
echo "sha=$SHA"
echo "install_path=$DEST_DIR"
echo "install_ok"

echo
echo "Next: open Codex Settings > Pets > Refresh, select 雪之下雪乃 / Yukinoshita Yukino."
