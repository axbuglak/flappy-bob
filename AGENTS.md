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
├── scripts/                 ← for the human only. Bob does NOT run any of them.
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
- Text has NO background: draw it as bare letters with `font.render(text, True, color)` (three
  arguments, never a background colour). No box, panel, fill, border, outline, shadow or glow
  behind any text. Only the pause and game-over screens may dim the whole window.
- Only `input_handler.py` reads pygame events and the keyboard. It calls methods of `GameState`.
- `main.py` calls `state.update(dt)` every frame. `GameState.update` must therefore return
  early while `paused`, and keep animating effects (particles, shake) while `game_over`.
- `main.py` may be adjusted if the window size or loop requires it (ESC and window close
  already work).
- Starter fields such as `level` and `lives` may be removed if the game does not need them.
  `GameState` must keep `score`, `game_over`, `paused` and `restart()`, because `main.py` and
  `input_handler.py` use them.

## Assets (already prepared, do not touch)

- `assets/bob.png` and `assets/logo.png` are official IBM Bob artwork. They are already loaded
  in `Renderer.__init__` as `self.sprite_bob` and `self.sprite_logo`, through the paths and
  sizes in `GameConfig` (`SPRITE_BOB`, `SPRITE_BOB_SIZE`, `SPRITE_LOGO`, `SPRITE_LOGO_SIZE`).
- Use these two surfaces. Do not download, generate or convert images. Do not add other
  asset files. Do not use anything in `assets/source/`.
- Rotate the sprite with `pygame.transform.rotate` for tilt. Do not rotate the stored surface
  in place; rotate a copy each frame.

---

## No commands (important)

**Run no commands at all**: no shell, no scripts, no tests, no installs, no git, and never start
the game (`uv run python main.py` opens a window and never returns). The human starts the game.
Nothing may ask for an approval. Since nothing formats or checks your code, write it correctly the
first time:

- Fully type-annotated Python 3.11+ (mypy strict): every parameter, return type (`-> None`
  included) and attribute, with element types on list, dict and tuple.
- ruff style: lines at most 100 characters, 4-space indent, double quotes, sorted imports
  (standard library, third party, `game.*`), no unused imports or variables.
- Define every constant in `config.py` first, then write `state.py` and `renderer.py`. Re-check
  that each `GameConfig.X` you use exists and is spelled identically.
- When all files are written, re-read them once and fix wrong names, missing constants, types or
  imports.

## Working efficiently

- **Write each file in ONE `write_file` call and always include `path`.** Use only
  `read_file`, `write_file`, `apply_diff` and `search_and_replace`. Do not invent tools.
  Search strings must not end with a stray newline.
- **`.venv` is hidden and already complete.** Do not inspect it or glob for it.
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
