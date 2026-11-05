# Facilitator Guide: "Flappy Bob" with IBM Bob

A 5 to 10 minute live demo. The audience watches Bob turn one prompt into a playable game.

## Flow

| Time | What happens |
|------|--------------|
| 0:00 | Show the empty starter and `AGENTS.md` (the "contract" Bob reads) |
| 0:30 | Paste the prompt from `DEMO_PROMPT.md`, press enter |
| 0:30 to 5:00 | Bob plans, writes config, state, renderer, input; lint after each file; smoke test. Talk through the talking points below |
| 5:00 | `uv run python main.py`, play live |
| 6:00 | One follow-up prompt (see below) |

## Talking points while Bob works

1. **AGENTS.md is a contract.** Bob reads it every time. Good context means fewer questions and mistakes.
2. **Logic and drawing are separate.** `state.py` never imports pygame, so particles and screen shake
   live in the state and the renderer only draws them.
3. **Spec first.** The prompt fixes every number (gravity, gap, speed), so Bob does not guess.
4. **Lint and smoke in the loop.** Bob checks itself with two scripts and never starts a blocking window.
5. **Prepared assets.** The official Bob artwork was added beforehand; Bob only uses it.

## Follow-up prompts (pick one, keep them short)

```
Add sound effects: a short blip on flap and a low buzz on game over.
Use pygame.mixer and generate the tones in code, no files. Constants in config.py.
```

```
Save the best score in a file .highscore in the project root and load it on start.
```

```
Night mode: after 10 points the background gets darker and the rack LEDs blink faster.
All numbers in config.py, timers in state.py.
```

```
Add a "Made with Bob" text at the bottom of the screen. Renderer and config only.
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Bob waits for a click | An auto-approve switch is off. Turn on Read, Edit, Execute, Todo. Click once to continue. |
| Bob asks a question | Answer briefly ("your choice") and continue. The prompt forbids questions, but models can slip. |
| Bob tries `uv run python main.py` and hangs | Stop the command and tell Bob: "Use ./scripts/smoke.sh instead." |
| Anything goes wrong | Say "here is one I prepared earlier" and run `cd ../flappy-bob-fallback && uv run python main.py` |
| Need to run the demo again | `./scripts/reset.sh` |
