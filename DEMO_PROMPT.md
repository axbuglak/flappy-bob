# Live demo: "Flappy Bob" with IBM Bob (Agent mode)

Internal IBM event. Goal: start Bob, and about 5 minutes later there is a playable Flappy Bird
where the bird is **Bob**, the IBM Bob mascot.

## Idea

Flappy Bird, but you play Bob with his hard hat. The pipes are server racks with blinking LEDs,
the world uses the IBM Carbon colours, the score is "Bugs fixed", and a crash is "Build failed!".
The official Bob artwork is already in `assets/` and already loaded by the renderer, so Bob
only writes game logic, drawing and input. That is what keeps the run short.

## Checklist BEFORE the stage (tick once)

Prepared state: `.venv` and `uv.lock` exist, `lint.sh` and `smoke.sh` are green on the empty
starter, the assets are in place, a finished fallback game exists in `../flappy-bob-fallback`.

- [ ] **Bob auto-approve** (bar above the input field): switch on **Read, Edit, Execute, Todo**.
      For safety also **Skill, Subtask, Subagent, Mode**. For Execute, add an allow-list with
      `./scripts/lint.sh --fix` and `./scripts/smoke.sh`. Without these switches Bob waits for a
      click after every step. This is the most common showstopper.
- [ ] Open the folder `flappy-bob/` as the Bob workspace, mode **Agent**.
- [ ] Check the starter (terminal in `flappy-bob/`):
  ```bash
  ./scripts/lint.sh       # must be green
  ./scripts/smoke.sh      # must print "smoke OK"
  ```
- [ ] **Dry run with the real prompt** on a copy of the folder (`cp -R flappy-bob /tmp/flappy-bob-probe`
      and open that). Time it (target: under 5 to 7 minutes) and watch for every click. Each click
      you need is a missing auto-approve switch.
- [ ] **Reset the stage folder after a run** (restores `game/` and `main.py` from the backup
      folder `.starter/` inside this project; assets and docs stay):
  ```bash
  ./scripts/reset.sh
  ```
- [ ] **Fallback:** the finished game is in `../flappy-bob-fallback`. Start it with
      `cd ../flappy-bob-fallback && uv run python main.py`. Keep a second terminal window ready.
- [ ] Disconnect other MCP connections or review rules in this session. They can trigger an
      approval question.
- [ ] Projector test: the window is 640x720 and fits 1080p. Use a large terminal font.
- [ ] Test network and model with one short question to Bob. Backup: phone hotspot.

## The prompt (copy and paste)

```
Design and build "Flappy Bob": a Flappy Bird game where the bird is Bob, the IBM Bob mascot with
the hard hat. Work completely on your own and ask no questions. For open points make sensible
assumptions and list them at the end in a short list.

AUTONOMY (so nobody has to click)
- Do not activate skills (also no brainstorming), use no MCP tools and no review tools, do not
  switch modes and do not start subagents.
- Work only inside this workspace folder. Read and write nothing outside it.
- Run shell commands one at a time, without &&, ;, pipes or cd. Only these are allowed:
  `./scripts/lint.sh --fix` and `./scripts/smoke.sh`.
- Install nothing (the environment is ready) and run no git commands.
- Download, generate or convert no images. The artwork is already in assets/ and loaded.
- Time budget: keep the implementation compact (about 700 lines in total, no features beyond this
  spec).
- Do not hand-wrap long lines: `./scripts/lint.sh --fix` formats the code. Use only read_file,
  write_file, apply_diff and search_and_replace, and always pass `path` to write_file.
- Do not look into `.venv` (hidden, complete). If a script says "uv: command not found", the
  script handles it: do not investigate and retry at most once.

CONCEPT
- Player = Bob. Use `self.sprite_bob` from Renderer.__init__ (assets/bob.png, already loaded,
  64x61 px). Tilt it with pygame.transform.rotate: nose up while rising, down while falling.
- Pipes = server racks: dark body with a blue edge, rows of small rack units with a LED each that
  blinks (green / dark green, driven by the state's time), and a blue lip at the gap end.
- Background: a vertical gradient per stage (see STAGES) plus 3 parallax layers on top, each built
  ONCE in the renderer as a transparent surface twice the window width (paint everything at x and
  x + 640 so it scrolls seamlessly; offset = scroll * factor % 640):
  * far, factor 0.08: 40 tiny stars (1 to 3 px, white, alpha 90), fixed random seed;
  * middle, factor 0.25: 9 dark rack silhouettes standing on the floor (40 to 70 px wide, 120 to
    300 px high, black alpha 80, with thin light rows every 16 px, white alpha 28) and the faint
    code tokens ("</>", "{ }", "01", "fn()", "=>"), colour (48,44,80);
  * near, factor 0.5: 7 thin vertical cables (3 px wide, 150 to 450 px long) hanging from the
    ceiling, white alpha 26.
  Build one gradient surface per stage once. While the stage changes, draw the lower stage
  gradient and the next one on top with alpha = fraction of `stage_blend`.
- Floor: dark strip, 80 px high, blue top line and moving blue hazard stripes (scroll with pipes).
- Wording (all in config.py): title "FLAPPY BOB"; score label "Bugs fixed"; game over
  "Build failed!" with hint "Press R to redeploy"; pause "Deployment paused" with hint
  "Press P to resume"; ready hint "Press SPACE to start"; play hint "Press P to pause";
  stage banner "Stage {number}: {name}" (number = stage index + 1).
- Colours (Carbon): primary blue (15,98,254), cyan (51,177,255), purple (138,63,252),
  red (250,77,86), text (244,244,244).
- Layout (window 640 x 720 px): big score number top centre, below it "Bugs fixed   Best N".
  Ready screen: title in cyan, the full mascot `self.sprite_logo` (assets/logo.png, 155x240) in
  the middle, the ready hint below it. Overlays for pause and game over: dark translucent layer.
- TEXT MUST ALWAYS BE READABLE: draw ALL text last, after the world, the sprites, the logo and the
  dark layer, so nothing covers it and the dark layer does not dim it. Give every text a dark
  outline (draw it 5 times in black, offset 2 px, then the colour on top) through one helper
  `_draw_text`. Every text must fit inside the window with a 24 px margin left and right; if a
  line is wider, scale it down in that helper. Check the longest texts ("Deployment paused",
  "Build failed!" at 48 px bold monospace).
- Stage banner: while the state's `banner_time` is above 0 (and Playing), show the stage banner in
  cyan, 28 px, centred at y = 160, through `_draw_text`, after everything else.
- Controls hint: while Ready and while Playing (not paused, not game over) always show
  "Press P to pause" centred on the floor strip at the bottom, 18 px, so the audience sees it.
- Effects (the animation state lives in state.py, not in the renderer):
  * On death: 28 small square particles fly out of Bob (random direction, speed 80 to 280 px/s,
    gravity 600 px/s^2, life 0.8 s, shrinking, alternating cyan and purple).
  * On death: screen shake for 0.35 s, strength 8 px fading to 0. The renderer draws the world to
    an off-screen surface and blits it with the shake offset from the state.
  * On the ready screen Bob bobs up and down (amplitude 10 px, 3 rad/s) around the vertical middle
    of the playfield.

RULES (use exactly these numbers, put them all in config.py)
- Playfield height = 720 - 80 (floor). Bob stays at x = 120. Collision shape for Bob: circle,
  radius 20 px.
- Gravity 1500 px/s^2. Flap sets the vertical speed to -460 px/s (not an addition). Maximum fall
  speed 720 px/s. Bob's tilt in degrees = -vy * 0.06, limited to 25 up and 70 down.
- Ceiling: Bob bumps against it (position clamped to the radius, upward speed set to 0), no death.
- Death: touching the floor, or the circle overlapping a rack (top or bottom part of a pipe).
- Pipes: width 84 px, entering at the right edge. The gap height comes from the current stage
  (see STAGES) and is stored in each pipe when it spawns (`Pipe.gap`), so pipes already on screen
  keep their gap; the collision test and the renderer use the pipe's own gap. Gap centre is
  random, at least 100 px away from ceiling and floor for the gap edges. A new pair spawns when the
  last pipe is `speed * 1.7` px away from the right edge, so the time between pairs stays 1.7 s.
  Remove pipes that left the screen to the left.
- Speed depends on play TIME, not on score: `play_time` counts seconds since the first flap
  (0 before it). speed = 160 + (300 - 160) * (1 - exp(-play_time / 40)) px/s, always below 300.
  Make it a property of the state; the floor, the pipes and the parallax scroll with it.
- Score +1 when the right edge of a pair passes Bob's x. Best score is kept in memory for the
  session only (survives restart, no file).
- State flow: Ready (Bob bobs, nothing moves) -> first flap starts the game -> Playing -> Game over.
  Pause with P (not during game over). Restart with R, only after game over.
- Controls: SPACE or arrow UP = flap. P = pause. R = restart (after game over). No mouse
  control. ESC = quit (already exists in main.py). Events only via KEYDOWN.

STAGES (difficulty and look change with the score; all numbers and tables in config.py)
- stage = min(score // 10, 3). Names: "Sprint", "Staging", "Production", "Black Friday".
- Gap height per stage: 190, 176, 163, 150 px.
- Background gradient (top colour -> bottom colour) per stage: (22,22,22)->(44,26,96);
  (10,24,56)->(0,60,160); (28,16,56)->(110,45,200); (48,10,16)->(130,24,44).
- State field `stage_blend` (float) moves towards `stage` by at most 1.2 per second (it never
  overshoots), so the background changes smoothly. It is updated also in game over.
- When a passed pair raises the stage: set `banner_time = 1.8` and `shake_time = 0.15` (the
  existing shake, weaker). `banner_time` counts down in `update`.
- `restart()` resets play_time, stage_blend and banner_time to 0; best score stays.

ARCHITECTURE (from AGENTS.md, binding)
- state.py: no pygame import. Bob, pipes, particles, shake time, the world time (for LED
  blinking), `play_time`, `stage_blend` and `banner_time` are state; `stage`, `pipe_gap` and
  `pipe_speed` are properties. `update(dt)` moves everything. main.py now calls it every frame, so
  `update` must return early while paused and keep particles and shake running in game over.
  `random` and `math` are fine.
- renderer.py: draws only, never changes state. Read everything from the state.
- config.py: all numbers, colours, sizes and texts. Keep the existing sprite entries.
- input_handler.py: the only place for pygame events. It only calls GameState methods
  (e.g. `flap()`, `restart()`) and toggles `paused`.
- GameState must keep `score`, `game_over`, `paused`, `restart()`. Remove `level` and `lives`.
- main.py needs no change (window size, title and keyboard focus on the game window are done).

PROCEDURE
1. First read AGENTS.md and all four files in game/ plus main.py.
2. Write a short plan (maximum 8 lines), then continue immediately, without waiting for approval.
3. Order: config.py, state.py, renderer.py, input_handler.py. Define EVERY constant that state.py
   and renderer.py use in config.py first (e.g. MAX_DT), and write each file in one call.
4. After each file run `./scripts/lint.sh --fix` and fix errors until it is green.
5. At the end run `./scripts/smoke.sh` (headless, it returns) and fix until it prints
   "smoke OK". Do NOT run `uv run python main.py`: the window would block you. I start the game
   myself.
6. Finish with 5 lines of summary, your assumptions, and how to play.
```

## After the run (live)

1. Start `uv run python main.py` in the terminal and play. SPACE to flap.
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
- If time is short, shorten the RULES block and keep CONCEPT, AUTONOMY and ARCHITECTURE.
- Do not use `scripts/run.sh` (the container needs XQuartz). `uv run python main.py` is more stable.
- If anything goes wrong on stage: say "and here is one I prepared earlier" and start the fallback.
