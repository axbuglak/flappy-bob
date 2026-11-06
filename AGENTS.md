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
- The background is never empty: on EVERY screen (Ready, Playing, Paused, Game over) draw the
  gradient and all three parallax layers first (layers are `pygame.SRCALPHA` surfaces). Do not
  skip a layer or fill the window with a plain colour afterwards. Its details (stars, grid, rack
  silhouettes with LEDs, code tokens like `fn()`, cables) are drawn in code, never loaded from
  image or SVG files.
- Nothing overlaps on the Ready screen: score, title, Bob, logo and hints each get their own band
  with fixed positions in `config.py`. Two texts, or a text and the logo, never overlap.
- Every text gets a visible semi-transparent black box behind it, with padding
  (`TEXT_BOX_COLOR = (0, 0, 0)`, `TEXT_BOX_ALPHA = 160`, `TEXT_BOX_PADDING = 8` in `config.py`), so
  the text is readable on a dark box. Render the text with `font.render(text, True, color)` (three
  arguments, never a background colour); draw the box on a `pygame.SRCALPHA` surface first, then
  the text on top. The box is the only allowed backing: no other panel, pill, border, outline,
  shadow or glow behind any text. Only the pause and game-over screens may dim the whole window.
- Z-order: all text is drawn last, directly on the screen, after the scene, the screen shake and
  the dim layer, so it is above pipes, Bob, the logo and particles. Never draw text into the
  off-screen scene surface. Text box rectangles (with padding) must not overlap or touch.
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

**Run no commands at all, not even once**: no shell, no terminal, no scripts, no tests, no renders
or screenshots, no installs, no git, and never start the game (`uv run python main.py` opens a
window and never returns). The human starts the game. There is nobody to ask and nobody to approve
a command, so a command only blocks the run. To verify something, re-read the files. Since nothing
formats or checks your code, write it correctly the first time:

- Fully type-annotated Python 3.11+ (mypy strict): every parameter, return type (`-> None`
  included) and attribute, with element types on list, dict and tuple.
- ruff style: lines at most 100 characters, 4-space indent, double quotes, sorted imports
  (standard library, third party, `game.*`), no unused imports or variables.
- Define EVERY constant in `config.py` first, complete, in ONE `write_file` call, before writing
  `state.py` and `renderer.py`. First make an inventory in your plan: go through the spec section
  by section and list every number, colour, size, offset, count, seed, frequency and text. Easily
  forgotten: LED blink (phase step, cycle length, thresholds), screen shake (frequencies,
  amplitude, duration), particle values, parallax factors and seeds, text box values, layout
  positions. Add none later and leave none unused.
- Final check by reading the files again, not from memory: list every `GameConfig.X` used in
  `state.py`, `renderer.py` and `input_handler.py` and compare it name by name with `config.py`.
  Every used name must be defined, every defined name used. Then fix wrong types and imports.

## Working efficiently

- **Write each file in ONE `write_file` call and always include `path`.** Use only
  `read_file`, `write_file`, `apply_diff` and `search_and_replace`. Do not invent tools.
  Search strings must not end with a stray newline.
- **After the first write, fix with small edits, never rewrite a file.** For a one-line change use
  `search_and_replace` with a single-line search string. For a block use `apply_diff` with the
  exact `:start_line:` taken from a fresh `read_file`; never guess it (`:start_line: 1` fails).
  Avoid multi-line `search_and_replace`: it breaks on whitespace.
- **At most ONE edit call per file per turn.** Never put two edits on the same file in the same
  turn: each one reads the file and writes it back, so the second silently overwrites the first,
  and both report success. Wait for the result, `read_file` to confirm the change is there, then
  make the next edit to that file. Edits to different files are independent and may share one
  turn: write `config.py` alone first, then `state.py`, `renderer.py` and `input_handler.py`
  together in one turn.
- **Missing constants:** collect ALL of them first and add them in ONE single edit, never one edit
  per constant.
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
