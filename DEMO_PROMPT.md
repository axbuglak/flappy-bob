# Live demo: "Flappy Bob" with IBM Bob (Agent mode)

Internal IBM event. Goal: start Bob, and about 5 minutes later there is a playable Flappy Bird
where the bird is **Bob**, the IBM Bob mascot.

## Idea

Flappy Bird, but you play Bob with his hard hat. The pipes are server racks with blinking LEDs,
the world uses the IBM Carbon colours, the score is "Bugs fixed", and a crash is "Build failed!".
The official Bob artwork is already in `assets/` and already loaded by the renderer, so Bob
only writes game logic, drawing and input. That is what keeps the run short.

## Checklist BEFORE the stage (tick once)

Prepared state: `.venv` and `uv.lock` exist and the assets are in place. Bob runs NO commands in
this demo (no scripts, no terminal), so the only thing you do is paste the prompt.

- [ ] **Bob auto-approve** (bar above the input field): switch on **Read, Edit, Todo**.
      For safety also **Skill, Subtask, Subagent, Mode**. Leave **Execute** off: Bob must not need
      it. Without these switches Bob waits for a click after every step. This is the most common
      showstopper.
- [ ] Open the folder `flappy-bob/` as the Bob workspace, mode **Agent**.
- [ ] **Dry run with the real prompt** on a copy of the folder (`cp -R flappy-bob /tmp/flappy-bob-probe`
      and open that). Time it (target: under 5 to 7 minutes), watch for every click, and start the
      result once with `uv run python main.py`. Check every screen (ready, playing, paused, game
      over): yellow text on a dark box, drawn above pipes, Bob and the logo, and no two boxes
      touching. Any command Bob tries is a prompt bug.
- [ ] **Reset the stage folder after a run** (restores `game/` and `main.py` from the backup
      folder `.starter/` inside this project; assets and docs stay):
  ```bash
  ./scripts/reset.sh
  ```
- [ ] **Fallback:** keep a finished game ready in a second folder and a second terminal window.
- [ ] Disconnect other MCP connections or review rules in this session. They can trigger an
      approval question.
- [ ] Projector test: the window is 640x720 and fits 1080p. Use a large terminal font.
- [ ] Test network and model with one short question to Bob. Backup: phone hotspot.

## The prompt (copy and paste)

```
Build "Flappy Bob": Flappy Bird where the bird is Bob, the IBM Bob mascot with the hard hat. Work
alone and ask no questions. Make sensible assumptions and list them at the end.

EVERY TEXT HAS A VISIBLE DARK BOX BEHIND IT: a semi-transparent black box with padding
(alpha 160), so the text stays readable over the pipes, the logo and the background.
There must be no other panel, pill, badge, bar, border, outline, shadow or glow around any text.

AUTONOMY
- No skills, no MCP tools, no review tools, no mode switch, no subagents.
- Work only inside this workspace. Use only read_file, write_file, apply_diff and
  search_and_replace; always pass `path` to write_file. Do not look into `.venv`.
- Run NO commands, not even once: no shell, no terminal, no scripts, no installs, no git, no
  tests, no renders or screenshots, and never start the game. You have no way to ask me anything
  and nobody can approve a command, so a command would just block the run. If you want to verify
  something, do it by re-reading the files. I start the game myself.
- ONE tool call per turn for every file edit. Never put two edit calls (write_file, apply_diff,
  search_and_replace) on the same file in the same turn: both read the file and write it back, so
  the second silently overwrites the first and the tool still reports success. Wait for the
  result, then `read_file` the file to confirm the change is there, and only then make the
  next edit. Order: config.py first, then the files that use its constants.
- After the first write of a file, never rewrite it: fix with small edits. One-line change:
  `search_and_replace` with a single-line search string. Block: `apply_diff` with the exact
  `:start_line:` from a fresh `read_file` (never guess it).
- If a constant is missing in config.py later, collect ALL missing ones first and add them in ONE
  single edit. Never one edit per constant.
- Create no images; the artwork is in assets/ and already loaded. Keep it compact (about 700
  lines in total) and add nothing beyond this spec.

CODE QUALITY (nothing checks your code, so get it right the first time)
- Python 3.11+, fully typed for mypy strict: every parameter, return type (`-> None` too) and
  attribute; element types on list, dict and tuple.
- ruff style: lines up to 100 characters, 4 spaces, double quotes, sorted imports (standard
  library, third party, `game.*`), no unused imports or variables.
- Write config.py first and COMPLETE, in ONE write_file call. Before that, do a constant inventory
  in your plan: go through the spec section by section (TEXT, BACKGROUND, LOOK, RULES, STAGES,
  Effects) and list every number, colour, size, offset, count, seed, frequency and text. Check
  these easily forgotten groups: LED blink (phase step, cycle length, on/off thresholds), screen
  shake (frequencies, amplitude, duration), particle values, parallax factors and seeds, rack and
  cable sizes, text box values, layout positions. Think through how state.py and renderer.py will
  use each one. Add none later, leave none unused. Every `GameConfig.X` used elsewhere must exist
  there with the exact same name. No magic numbers in state.py or renderer.py.
- FINAL CHECK, by reading the files again, not from memory (a success message from a tool proves
  nothing): `read_file` config.py, state.py, renderer.py and input_handler.py, write down every
  `GameConfig.X` name used in the last three, and compare it name by name with the names defined
  in config.py. Every used name must be defined. Every defined name must be used. Fix any gap
  with ONE edit, then read the file again to confirm.
- Then re-read the four files once and fix wrong names, types and imports. The game must not
  crash on the Ready screen or after restart.

TEXT
- One helper `_draw_text(text, font, color, center)`: `surf = font.render(text, True, color)`
  (exactly these three arguments, never a background colour). Shrink it with smoothscale if it is
  wider than 640 - 2 * 24 px. Then draw the box:
  `box = pygame.Surface((w + 2 * pad, h + 2 * pad), pygame.SRCALPHA)`, fill it with
  `GameConfig.TEXT_BOX_COLOR` and `GameConfig.TEXT_BOX_ALPHA`, blit it at the text rect inflated
  by the padding, then blit the text on top. All texts use it: score, "Bugs fixed   Best N" line,
  title, hints, banner, overlay titles.
- config.py: `TEXT_BOX_COLOR = (0, 0, 0)`, `TEXT_BOX_ALPHA = 160`, `TEXT_BOX_PADDING = 8`.
  Never hard-code these in renderer.py. The box is the only allowed backing behind text.
- Z-ORDER: draw all text last, directly on the screen, after the scene, the screen shake and
  the pause/game-over dim layer. Text is therefore above pipes, Bob, the logo, particles and
  the dim layer. Never draw text into the off-screen scene surface.
- Colours: score, "Bugs fixed   Best N" line and all hints yellow (241,194,27), stored as
  `COLOR_TEXT`. Title, stage banner and pause title cyan (51,177,255). Game-over title red
  (250,77,86).
- Without running anything, check from the numbers in config.py that on the Ready screen no two
  text boxes touch (including the padding). Increase the vertical gaps in config.py if they do.

BACKGROUND (never empty: it must show clear detail on EVERY screen)
- The background is NEVER a flat or empty colour. Ready, Playing, Paused and Game over all draw the
  full background first, every frame: gradient, then the 3 layers, then everything else. Pause and
  game over only add the dark layer on top of it.
- Gradient: one vertical gradient per stage (see STAGES), covering the whole window (build once).
  While the stage changes, draw the lower stage gradient and the next one on top with
  alpha = fractional part of `stage_blend`.
- 3 parallax layers on top of the gradient. Build each ONCE in the renderer as
  `pygame.Surface((1280, 720), pygame.SRCALPHA)` (the SRCALPHA flag is mandatory, otherwise the
  layer covers the gradient), paint every item at x and x + 640 so it scrolls seamlessly, and blit it
  at x = -(scroll * factor % 640). Detail must be clearly visible, not just faintly. Draw ALL of it
  in code with `pygame.draw` and `font.render`; load no image or SVG file for the background (the
  files in assets/source/ are off limits). Use fixed random seeds, so the picture is the same every
  run:
  * far, factor 0.08: 50 stars (1 to 3 px, white, alpha 120) spread over the whole playfield, and a
    faint circuit grid: horizontal and vertical lines every 80 px, colour (255,255,255) alpha 14;
  * middle, factor 0.25: 9 rack silhouettes standing on the floor line (40 to 70 px wide, 120 to
    300 px high, black alpha 90), spread evenly over the width so there are no big gaps. Each has a
    thin light row every 16 px (white alpha 36) and 3 to 6 tiny status LEDs (3 px squares, green
    (66,190,101) or cyan (51,177,255), alpha 160) at random rows. Plus 12 code tokens ("</>",
    "{ }", "01", "fn()", "=>", "git", "#!") in (64,60,110), 18 px, spread over the sky above the
    racks (y from 40 to 320) without overlapping each other;
  * near, factor 0.5: 7 vertical cables (3 px wide, 150 to 450 px long) from the ceiling, white
    alpha 32, each ending in a small connector: a 9 x 6 px rectangle, cyan alpha 90.
- The background scrolls with `scroll` while Playing. On the Ready screen it is shown standing
  still (scroll = 0) and fully drawn. Never skip or hide a layer on any screen.
- The only fill of the whole window is the gradient. Do not fill with a plain colour after it.

LOOK
- Player: `self.sprite_bob` (assets/bob.png, 64x61, already loaded), rotated as a copy each frame:
  nose up while rising, down while falling.
- Pipes = server racks: dark body, blue edge, rows of rack units with a blinking LED each (green /
  dark green, driven by the state's time) and a blue lip at the gap end.
- Floor: dark strip, 80 px high, blue top line, moving blue hazard stripes (scroll with the pipes).
- Colours (Carbon): blue (15,98,254), cyan (51,177,255), purple (138,63,252), red (250,77,86).
- Fonts (monospace): score 64 px bold; title and overlay titles 48 px bold; banner 28 px bold;
  all other texts 18 px.
- Layout (640 x 720): big score top centre, below it "Bugs fixed   Best N". Controls hint
  "Press P to pause" (18 px) centred on the floor strip while Ready and Playing.
- Ready screen: the normal scene (background, floor, bobbing Bob) with the title in cyan, the full
  mascot `self.sprite_logo` (assets/logo.png, 155x240) and the ready hint. No overlay, no dimming.
  No pipes on this screen. NOTHING MAY OVERLAP: use exactly this layout, with every position in
  config.py, so each item has its own free band (centres; all items centred at x = 320 except Bob):
  * score number y = 56 (about 18 to 94) and "Bugs fixed   Best N" y = 130 (about 120 to 140);
  * title "FLAPPY BOB" y = 200 (about 170 to 230);
  * Bob on the left at x = 120, bobbing around y = 320 (y about 280 to 361, x from 88 to 152): he
    must not touch the logo or any text;
  * logo `self.sprite_logo` at y = 400 (280 to 520), x from 242 to 398;
  * ready hint "Press SPACE to start" y = 570 (about 560 to 580);
  * controls hint "Press P to pause" y = 680 on the floor strip.
  The text boxes (text plus 8 px padding on every side) count as part of these rectangles: no two
  boxes may overlap or touch. While Playing, texts may sit over pipes, but two texts or a text and
  the logo must never overlap.
- Pause and game over: draw the scene, then ONE translucent black layer over the whole window
  (alpha 160), then the texts. The title ("Deployment paused" / "Build failed!") at y = 300 and its
  hint at y = 370, below the score lines (y = 56 and 130), so no text overlaps another.
- Stage banner: while `banner_time` > 0 and Playing, "Stage {number}: {name}" (number = stage + 1),
  28 px, centred at y = 200 (below the score lines, so the boxes do not touch).
- Texts (config.py): "FLAPPY BOB"; "Bugs fixed"; "Build failed!" / "Press R to redeploy";
  "Deployment paused" / "Press P to resume"; "Press SPACE to start"; "Press P to pause".
  The longest ("Deployment paused", "Build failed!" at 48 px bold monospace) must fit the window.
- Effects (animation state lives in state.py, not in the renderer):
  * Death: 28 small square particles from Bob (random direction, 80 to 280 px/s, gravity
    600 px/s^2, life 0.8 s, shrinking, alternating cyan and purple).
  * Death: screen shake 0.35 s, 8 px, fading to 0. Draw the scene to an off-screen surface and
    blit it with the state's shake offset (the text layer is drawn on the screen afterwards).
  * Ready: Bob bobs up and down (amplitude 10 px, 3 rad/s) around y = 320 (see Ready screen).

RULES (exactly these numbers, all in config.py)
- Playfield height = 720 - 80 (floor). Bob at x = 120, collision circle radius 20 px.
- Gravity 1500 px/s^2. Flap sets vy to -460 px/s (not added). Max fall speed 720 px/s. Tilt in
  degrees = -vy * 0.06, limited to 25 up and 70 down.
- Ceiling: clamp Bob to the radius and set upward speed to 0. No death.
- Death: touching the floor, or the circle overlapping a rack (top or bottom part of a pipe).
- Pipes: width 84 px, enter at the right edge, removed when fully left of the screen. Each pipe
  stores its own gap height (`Pipe.gap`, taken from the current stage when it spawns); collision
  and drawing use that value. Gap centre random, gap edges at least 100 px from ceiling and floor.
  A new pair spawns when the last pipe is `speed * 1.7` px from the right edge (constant 1.7 s).
- Speed depends on play TIME, not score. `play_time` counts seconds since the first flap.
  speed = 160 + (300 - 160) * (1 - exp(-play_time / 40)) px/s, always below 300. State property;
  floor, pipes and parallax scroll with it.
- Score +1 when the right edge of a pair passes Bob's x. Best score stays in memory for the
  session (survives restart, no file).
- Flow: Ready (Bob bobs, nothing moves) -> first flap starts -> Playing -> Game over.
  Pause with P (not in game over). Restart with R (only in game over).
- Controls: SPACE or UP = flap, P, R. ESC already works. No mouse. Events only via KEYDOWN.

STAGES (all numbers and tables in config.py)
- stage = min(score // 10, 3). Names "Sprint", "Staging", "Production", "Black Friday".
- Gap height per stage 190, 176, 163, 150 px.
- Sky gradient (top -> bottom) per stage: (22,22,22)->(44,26,96); (10,24,56)->(0,60,160);
  (28,16,56)->(110,45,200); (48,10,16)->(130,24,44).
- `stage_blend` (float) moves towards `stage` by at most 1.2 per second, never overshooting, also
  in game over.
- When a passed pair raises the stage: `banner_time = 1.8` and `shake_time = 0.15` (the same
  shake, weaker). `banner_time` counts down in `update`.
- `restart()` resets play_time, stage_blend and banner_time to 0; best score stays.

ARCHITECTURE (AGENTS.md, binding)
- state.py: no pygame import. Holds Bob, pipes, particles, shake time, world time (LED blink),
  `play_time`, `stage_blend`, `banner_time`; `stage`, `pipe_gap`, `pipe_speed` are properties.
  `update(dt)` returns early while paused and keeps particles, shake and `stage_blend` running in
  game over. `random` and `math` are fine.
- renderer.py: draws only, never changes state. config.py: every number, colour, size and text;
  keep the sprite entries. input_handler.py: the only place for pygame events; it calls GameState
  methods (`flap()`, `restart()`) and toggles `paused`.
- GameState keeps `score`, `game_over`, `paused`, `restart()`; remove `level` and `lives`.
  main.py needs no change.

PROCEDURE
1. Read AGENTS.md, the four files in game/ and main.py.
2. Write a plan of at most 8 lines plus the constant inventory (see CODE QUALITY), and continue at
   once, without waiting for approval.
3. Write config.py, state.py, renderer.py, input_handler.py, each in ONE call, one call per turn.
4. Do the FINAL CHECK from CODE QUALITY (compare the GameConfig names with config.py). Run nothing.
5. Finish with a 5-line summary, your assumptions and how to play.
```

## After the run (live)

1. Start `uv run python main.py` in a terminal and play. SPACE to flap. (This is your only
   command; Bob runs none.)
2. If you notice something, give Bob one short correction. Examples:
   - "Add sound effects: a short blip on flap and a low buzz on game over. Use pygame.mixer and
     generate the tones in code so no files are needed."
   - "Save the best score in a file `.highscore` and show it on start."
   - "Add a 'Stage clear' sound: three rising beeps when a new stage starts."
   - "Add a small 'Made with Bob' text at the bottom."
   Keep constants in `config.py` and state in `state.py`.

## Tips for the stage

- Bob needs a few minutes depending on the model. While it works, explain the architecture rules in
  `AGENTS.md` (logic separated from drawing: that is why particles and shake live in the state, not
  in the renderer) and point out that the Bob artwork was prepared in advance.
- The prompt is long and unambiguous on purpose. It prevents questions that would break the flow.
- If time is short, shorten the RULES block and keep LOOK, AUTONOMY and ARCHITECTURE.
- Do not use `scripts/run.sh` (the container needs XQuartz). `uv run python main.py` is more stable.
- If anything goes wrong on stage: say "and here is one I prepared earlier" and start the fallback.
