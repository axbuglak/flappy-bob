#!/usr/bin/env bash
# scripts/smoke.sh — Headless smoke test: runs the real main loop for ~3 s with
# simulated key presses (no window, no audio). Exit code 0 = no crash.
#
# Usage: ./scripts/smoke.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
# shellcheck source=scripts/_env.sh
source "$ROOT/scripts/_env.sh"

SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy run_py - <<'PY'
import pygame

from main import main

pygame.init()
pygame.display.set_mode((1, 1))
keys = [
    pygame.K_SPACE, pygame.K_UP, pygame.K_SPACE, pygame.K_p, pygame.K_p,
    pygame.K_SPACE, pygame.K_SPACE, pygame.K_r, pygame.K_SPACE,
]
for k in keys:
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=k))
pygame.time.set_timer(pygame.QUIT, 3000, loops=1)
try:
    main()
except SystemExit as e:
    if e.code not in (0, None):
        raise
print("smoke OK")
PY
