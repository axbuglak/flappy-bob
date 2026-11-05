# Flappy Bob

> **IBM Bob live demo.** Flappy Bird, but the bird is Bob, the IBM Bob mascot.
> IBM Bob builds the whole game from one prompt in about 5 minutes.

For an internal IBM presentation. The Bob artwork in `assets/` is IBM property and is not for
redistribution outside IBM.

---

## Quick start

```bash
cd flappy-bob
uv sync                       # already done on the prepared machine
```

1. Open this folder as the workspace in IBM Bob, mode **Agent**.
2. Turn on auto-approve for Read, Edit and Todo (see the checklist in [`DEMO_PROMPT.md`](DEMO_PROMPT.md)).
3. Paste the prompt from [`DEMO_PROMPT.md`](DEMO_PROMPT.md). Bob runs no commands and asks nothing.
4. When Bob is done: `uv run python main.py`

## Play

| Key | Action |
|-----|--------|
| SPACE / UP | Flap |
| P | Pause |
| R | Restart (after "Build failed!") |
| ESC | Quit |

Flap is keyboard only (no mouse). `main.py` asks the OS to give the game window keyboard focus
at start, so SPACE works right away without clicking the window first.

## What is prepared

| Item | Where |
|------|-------|
| Project rules for Bob (architecture, no commands, assets) | [`AGENTS.md`](AGENTS.md) |
| The prompt, stage checklist, follow-up ideas | [`DEMO_PROMPT.md`](DEMO_PROMPT.md) |
| Official Bob artwork, already loaded by the renderer | [`assets/`](assets/README.md) |
| Empty starter with the four modules | `game/`, `main.py` |
| Reset after a run (you, not Bob) | `scripts/reset.sh` (restores from `.starter/` in this project) |
| Finished game as fallback | `../flappy-bob-fallback` |

## Checks (for you, after the demo; Bob never runs these)

```bash
./scripts/lint.sh          # ruff + mypy
./scripts/lint.sh --fix    # auto-fix style issues
./scripts/smoke.sh         # headless run of the game loop, ~3 s
```

## Project structure

```
flappy-bob/
├── AGENTS.md              ← IBM Bob reads this automatically
├── DEMO_PROMPT.md         ← the live-demo prompt and checklist
├── main.py                ← game loop
├── assets/                ← bob.png, logo.png (+ source/ originals)
├── game/
│   ├── config.py          ← constants
│   ├── state.py           ← game logic & data
│   ├── renderer.py        ← all drawing
│   └── input_handler.py   ← keyboard input
└── scripts/               ← lint, smoke, reset, container launch
```
