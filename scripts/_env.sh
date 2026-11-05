#!/usr/bin/env bash
# scripts/_env.sh — sourced by lint.sh, smoke.sh and reset.sh. Do not run directly.
#
# Bob's shell is non-interactive and does not load ~/.zshrc, so `uv` is often not on PATH.
# 1. Add the usual uv locations to PATH.
# 2. If uv is still missing, run the tools straight from the prepared .venv.
#
# Provides: run_py (python), run_ruff, run_mypy.

export PATH="$HOME/.local/bin:$HOME/.cargo/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"

VENV_BIN="$ROOT/.venv/bin"

if command -v uv >/dev/null 2>&1; then
  run_py()   { uv run python "$@"; }
  run_ruff() { uv run ruff "$@"; }
  run_mypy() { uv run mypy "$@"; }
elif [[ -x "$VENV_BIN/python" ]]; then
  echo "note: uv not found, using $VENV_BIN"
  run_py()   { "$VENV_BIN/python" "$@"; }
  run_ruff() { "$VENV_BIN/ruff" "$@"; }
  run_mypy() { "$VENV_BIN/mypy" "$@"; }
else
  echo "ERROR: neither uv nor $VENV_BIN found. Run 'uv sync' once in $ROOT." >&2
  exit 1
fi
