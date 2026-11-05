"""
Renderer — responsible for ALL drawing.  It never mutates GameState.

IBM Bob will implement draw_game() based on your game spec.
"""

import pygame

from game.config import GameConfig
from game.state import GameState


class Renderer:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font_large = pygame.font.SysFont("monospace", 48, bold=True)
        self.font_medium = pygame.font.SysFont("monospace", 28)
        self.font_small = pygame.font.SysFont("monospace", 18)

        # Official IBM Bob artwork, already in assets/ (transparent PNG).
        self.sprite_bob = self._load_sprite(GameConfig.SPRITE_BOB, GameConfig.SPRITE_BOB_SIZE)
        self.sprite_logo = self._load_sprite(GameConfig.SPRITE_LOGO, GameConfig.SPRITE_LOGO_SIZE)

    @staticmethod
    def _load_sprite(path: str, size: tuple[int, int]) -> pygame.Surface:
        """Load a PNG scaled to *size*; falls back to a plain circle if the file is missing."""
        try:
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.smoothscale(image, size)
        except (pygame.error, FileNotFoundError):
            fallback = pygame.Surface(size, pygame.SRCALPHA)
            pygame.draw.ellipse(fallback, GameConfig.COLOR_PRIMARY, fallback.get_rect())
            return fallback

    # ------------------------------------------------------------------
    # Public interface — called once per frame from main.py
    # ------------------------------------------------------------------

    def draw(self, state: GameState) -> None:
        self.screen.fill(GameConfig.COLOR_BG)

        if state.game_over:
            self._draw_game_over(state)
        elif state.paused:
            self._draw_paused(state)
        else:
            self._draw_game(state)

        self._draw_hud(state)

    # ------------------------------------------------------------------
    # Private helpers — IBM Bob fills these in
    # ------------------------------------------------------------------

    def _draw_game(self, state: GameState) -> None:
        """Draw the active game scene.  IBM Bob implements this."""
        # TODO: draw board, pieces, enemies, bullets, player, etc.
        placeholder = self.font_medium.render(
            "Describe your game to IBM Bob →", True, GameConfig.COLOR_PRIMARY
        )
        rect = placeholder.get_rect(
            center=(GameConfig.SCREEN_WIDTH // 2, GameConfig.SCREEN_HEIGHT // 2)
        )
        self.screen.blit(placeholder, rect)

    def _draw_hud(self, state: GameState) -> None:
        """Heads-up display: score, level, lives."""
        score_surf = self.font_small.render(
            f"SCORE  {state.score:06d}", True, GameConfig.COLOR_TEXT
        )
        level_surf = self.font_small.render(
            f"LEVEL  {state.level:02d}", True, GameConfig.COLOR_TEXT
        )
        lives_surf = self.font_small.render(f"LIVES  {state.lives}", True, GameConfig.COLOR_ACCENT)

        self.screen.blit(score_surf, (12, 8))
        self.screen.blit(level_surf, (12, 30))
        self.screen.blit(lives_surf, (GameConfig.SCREEN_WIDTH - lives_surf.get_width() - 12, 8))

    def _draw_game_over(self, state: GameState) -> None:
        self._draw_overlay("GAME OVER", f"Score: {state.score}", "Press R to restart")

    def _draw_paused(self, state: GameState) -> None:
        self._draw_overlay("PAUSED", "", "Press P to resume")

    def _draw_overlay(self, title: str, subtitle: str, hint: str) -> None:
        overlay = pygame.Surface(
            (GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        cx, cy = GameConfig.SCREEN_WIDTH // 2, GameConfig.SCREEN_HEIGHT // 2
        title_surf = self.font_large.render(title, True, GameConfig.COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, cy - 60)))

        if subtitle:
            sub_surf = self.font_medium.render(subtitle, True, GameConfig.COLOR_TEXT)
            self.screen.blit(sub_surf, sub_surf.get_rect(center=(cx, cy)))

        hint_surf = self.font_small.render(hint, True, GameConfig.COLOR_PRIMARY)
        self.screen.blit(hint_surf, hint_surf.get_rect(center=(cx, cy + 60)))
