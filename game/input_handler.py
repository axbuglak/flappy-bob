"""
InputHandler — translates raw pygame events into game actions.

Only this class touches pygame events.  GameState never imports pygame.
IBM Bob will expand handle() with game-specific key bindings.
"""

import pygame

from game.state import GameState


class InputHandler:
    def handle(self, events: list[pygame.event.Event], state: GameState) -> None:
        """Process *events* and mutate *state* accordingly."""
        keys = pygame.key.get_pressed()

        for event in events:
            if event.type == pygame.KEYDOWN:
                self._on_keydown(event.key, state)

        # Continuous key input (held keys) — IBM Bob adds movement etc. here
        self._on_keys_held(keys, state)

    # ------------------------------------------------------------------

    def _on_keydown(self, key: int, state: GameState) -> None:
        """Single key-press events (rotate, fire, restart, pause…)."""
        if key == pygame.K_p and not state.game_over:
            state.paused = not state.paused

        if key == pygame.K_r and state.game_over:
            state.restart()

        # TODO: IBM Bob adds game-specific key-down bindings here.
        # Example (Tetris):
        #   if key == pygame.K_UP:   state.rotate_piece()
        #   if key == pygame.K_SPACE: state.hard_drop()

    def _on_keys_held(self, keys: pygame.key.ScancodeWrapper, state: GameState) -> None:
        """Continuous movement / actions while key is held."""
        if state.game_over or state.paused:
            return

        # TODO: IBM Bob adds directional / continuous controls here.
        # Example (Snake / Breakout):
        #   if keys[pygame.K_LEFT]:  state.move_left()
        #   if keys[pygame.K_RIGHT]: state.move_right()
