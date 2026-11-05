"""
Flappy Bob - Main Entry Point
================================
This file is intentionally minimal.
IBM Bob implements the game in the game/ package; this loop stays almost unchanged.

The structure is already wired up:
  - GameConfig  → game/config.py
  - GameState   → game/state.py
  - Renderer    → game/renderer.py
  - InputHandler → game/input_handler.py
  - main loop   → here

Run with:
  uv run python main.py
Or inside Docker:
  ./scripts/run.sh
"""

import contextlib
import sys
import warnings

import pygame

from game.config import GameConfig
from game.input_handler import InputHandler
from game.renderer import Renderer
from game.state import GameState


def _focus_window() -> None:
    """Give the game window keyboard focus, so SPACE works without clicking it first."""
    with contextlib.suppress(AttributeError, pygame.error), warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        pygame.Window.from_display_module().focus()


def main() -> None:
    """Main game loop."""
    pygame.init()
    pygame.display.set_caption(GameConfig.TITLE)

    screen = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    state = GameState()
    renderer = Renderer(screen)
    input_handler = InputHandler()

    _focus_window()
    frame = 0

    running = True
    while running:
        dt = clock.tick(GameConfig.FPS) / 1000.0  # delta time in seconds

        # Ask for focus during the first 0.5 s: the OS may map the window a moment late.
        if frame < GameConfig.FPS // 2:
            _focus_window()
        frame += 1

        # --- Event handling ---
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # --- Input ---
        input_handler.handle(events, state)

        # --- Update (state decides itself what to do when paused / game over,
        #     so death effects such as particles keep animating) ---
        state.update(dt)

        # --- Render ---
        renderer.draw(state)
        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
