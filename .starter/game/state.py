"""
GameState — the single source of truth for everything that can change at runtime.

IBM Bob will expand this class with game-specific fields and logic.
Keep ALL mutable game data here; renderers and input handlers only READ this.
"""


class GameState:
    def __init__(self) -> None:
        # --- Meta ---
        self.score: int = 0
        self.level: int = 1
        self.lives: int = 3
        self.game_over: bool = False
        self.paused: bool = False

        # TODO: IBM Bob will add game-specific state here.
        # Examples for a Tetris-like game:
        #   self.board: list[list[int]] = ...
        #   self.current_piece: Piece | None = None
        #   self.next_piece: Piece | None = None
        #   self.drop_timer: float = 0.0

        self._init_game()

    def _init_game(self) -> None:
        """(Re-)initialise game-specific state. Called on start and restart."""
        # TODO: IBM Bob implements this.
        pass

    def update(self, dt: float) -> None:
        """
        Advance the simulation by *dt* seconds.
        Called every frame by main.py, also while paused or game over. Return early
        when paused; keep effects (particles, shake) running in game over.
        """
        # TODO: IBM Bob implements physics, timers, collision, etc.
        pass

    def restart(self) -> None:
        """Reset everything and start a fresh game."""
        self.score = 0
        self.level = 1
        self.lives = 3
        self.game_over = False
        self.paused = False
        self._init_game()
