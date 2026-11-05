#!/usr/bin/env bash
# scripts/reset.sh — Put the stage project back to the empty starter after a demo run.
# Restores main.py and game/ from the backup in .starter/ (inside this project).
# Assets, scripts and docs stay.
#
# Usage: ./scripts/reset.sh

set -euo pipefail
cd "$(dirname "$0")/.."

STARTER=".starter"
if [[ ! -d "$STARTER/game" ]]; then
  echo "Starter backup not found: $STARTER" && exit 1
fi

rm -rf game
cp -R "$STARTER/game" game
cp "$STARTER/main.py" main.py
find . -name __pycache__ -not -path "./.venv/*" -prune -exec rm -rf {} + 2>/dev/null || true
rm -rf .ruff_cache .mypy_cache
echo "reset OK: starter restored"
