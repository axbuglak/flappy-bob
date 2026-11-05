# AGENTS.md — Project context for IBM Bob

> This file is read automatically by IBM Bob when you open this project.
> It tells Bob everything it needs to know to build the game.

## What this project is

A **spec-driven arcade game starter**, prepared for the live demo **"Flappy Bob"**:
Flappy Bird, but the bird is **Bob**, the IBM Bob mascot with the hard hat.

The code structure and the artwork are already wired up. Your job is to implement the game
logic, the drawing and the input handling from the spec you receive. Do not ask questions;
make sensible assumptions and list them at the end.

---

## Repository layout

```
flappy-bob/
├── main.py                  ← entry point; game loop lives here (calls state.update(dt) every frame)
├── assets/
│   ├── bob.png              ← Bob's head with hard hat, transparent. READY TO USE.
│   ├── logo.png             ← full Bob mascot, transparent. READY TO USE (Ready screen).
│   └── source/              ← originals from bob.ibm.com. NOT used by the game.
├── game/
│   ├── config.py            ← ALL constants (window size, colours, physics, texts, asset paths)
│   ├── state.py             ← ALL mutable game data (bob, pipes, score, particles, timers)
│   ├── renderer.py          ← ALL drawing code (never mutates state); sprites already loaded
│   └── input_handler.py     ← ALL keyboard handling
├── scripts/
│   ├── lint.sh              ← ruff + mypy quality checks
│   ├── smoke.sh             ← headless run of the real game loop (~3 s)
│   └── run.sh / run.bat     ← Podman container launch (not used in the demo)
├── Dockerfile
└── pyproject.toml           ← uv / hatchling project config
```

### The four modules — where everything goes

| File | What goes in it | What must NOT go in it |
|------|-----------------|------------------------|
| `config.py` | Constants, colours, sizes, speeds, texts | Any runtime state |
| `state.py` | Game entities, timers, score, particles | pygame imports, drawing |
| `renderer.py` | All `pygame.draw.*` and `blit` calls | Mutation of state |
| `input_handler.py` | Key event mapping | Business logic |

---

## Hard rules (apply to every change)

- `state.py` never imports pygame. The `random` and `math` modules are allowed.
- ALL mutable state lives in `state.py`. That includes animations: timers, effect progress,
  particles, screen-shake time, message text with remaining time. `renderer.py` only reads
  this state and draws it. It changes nothing.
- All numbers, colours, text constants and sizes live in `config.py`.
- Only `input_handler.py` reads pygame events and the keyboard. It calls methods of `GameState`.
- `main.py` calls `state.update(dt)` every frame. `GameState.update` must therefore return
  early while `paused`, and keep animating effects (particles, shake) while `game_over`.
- `main.py` may be adjusted if the window size or loop requires it (ESC and window close
  already work).
- Starter fields such as `level` and `lives` may be removed if the game does not need them.
  `GameState` must keep `score`, `game_over`, `paused` and `restart()`, because `main.py`,
  `input_handler.py` and `smoke.sh` use them.

## Assets (already prepared, do not touch)

- `assets/bob.png` and `assets/logo.png` are official IBM Bob artwork. They are already loaded
  in `Renderer.__init__` as `self.sprite_bob` and `self.sprite_logo`, through the paths and
  sizes in `GameConfig` (`SPRITE_BOB`, `SPRITE_BOB_SIZE`, `SPRITE_LOGO`, `SPRITE_LOGO_SIZE`).
- Use these two surfaces. Do not download, generate or convert images. Do not add other
  asset files. Do not use anything in `assets/source/`.
- Rotate the sprite with `pygame.transform.rotate` for tilt. Do not rotate the stored surface
  in place; rotate a copy each frame.

---

## Checking your work without blocking

`uv run python main.py` opens a window and never returns. As an agent, **do not run it**.
Instead, run these two commands, one per call:

```bash
./scripts/lint.sh --fix     # ruff + mypy, formats automatically
./scripts/smoke.sh          # runs the real game loop headless for ~3 s with simulated keys
```

Both must end with exit code 0 before a task counts as done. The environment (`.venv`) is
already installed. Do not install anything and do not run git.

## Working efficiently (lessons from rehearsals)

- **Do not hand-wrap long lines.** `./scripts/lint.sh --fix` runs `ruff format` (line length
  100, E501 ignored). Just write the code and let the script format it.
- **Define every constant in `config.py` first**, then write `state.py` and `renderer.py`.
  Re-check that each `GameConfig.X` you use exists (for example `MAX_DT`).
- **Write each file in ONE `write_file` call and always include `path`.** Use only
  `read_file`, `write_file`, `apply_diff` and `search_and_replace`. Do not invent tools.
  Search strings must not end with a stray newline.
- **`.venv` is hidden and already complete.** Do not inspect it or glob for it.
- **If a script prints "uv: command not found"**, the scripts already handle it (they fall
  back to `.venv/bin`). Do not investigate, and do not retry more than once.
- Keep the whole game compact, about 700 lines across `game/*.py`.

---

## Tech stack

| Tool | Purpose |
|------|---------|
| Python 3.12 | Language |
| pygame-ce | 2D rendering + input |
| uv | Package manager / venv (already synced) |
| ruff | Linter + formatter |
| mypy | Static type checker (strict) |
