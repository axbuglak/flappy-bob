#!/usr/bin/env bash
# scripts/lint.sh — Run ruff (linter + formatter check) and mypy (type checker)
#
# Usage:
#   ./scripts/lint.sh           # lint + typecheck
#   ./scripts/lint.sh --fix     # also auto-fix ruff issues AND format (line length 100)
#   ./scripts/lint.sh --types   # type check only
#   ./scripts/lint.sh --lint    # lint only
#
# Exit codes:
#   0 — all checks passed
#   1 — one or more checks failed

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
# shellcheck source=scripts/_env.sh
source "$ROOT/scripts/_env.sh"

DO_LINT=true
DO_TYPES=true
DO_FIX=false
FAILED=false

# ── Parse args ──────────────────────────────────────────────────────────────
for arg in "$@"; do
  case "$arg" in
    --fix)   DO_FIX=true ;;
    --lint)  DO_TYPES=false ;;
    --types) DO_LINT=false ;;
    *) echo "Unknown argument: $arg" && exit 1 ;;
  esac
done

# ── Colours ─────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'

header() { echo -e "\n${CYAN}── $1 ─────────────────────────────────${NC}"; }
pass()   { echo -e "${GREEN}✓ $1${NC}"; }
fail()   { echo -e "${RED}✗ $1${NC}"; FAILED=true; }

# ── Ruff ────────────────────────────────────────────────────────────────────
if $DO_LINT; then
  header "ruff — linter"
  if $DO_FIX; then
    run_ruff check --fix . && pass "ruff check (with fixes)" || fail "ruff check"
    run_ruff format .      && pass "ruff format"            || fail "ruff format"
  else
    run_ruff check .         && pass "ruff check" || fail "ruff check"
    run_ruff format --check . && pass "ruff format (check only)" || fail "ruff format (run --fix to auto-format)"
  fi
fi

# ── mypy ────────────────────────────────────────────────────────────────────
if $DO_TYPES; then
  header "mypy — type checker"
  run_mypy game/ main.py && pass "mypy" || fail "mypy"
fi

# ── Summary ─────────────────────────────────────────────────────────────────
echo ""
if $FAILED; then
  echo -e "${RED}One or more checks failed.${NC}"
  exit 1
else
  echo -e "${GREEN}All checks passed ✓${NC}"
fi
