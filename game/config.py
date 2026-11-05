"""
GameConfig — tweak these constants or ask IBM Bob to adjust them.
All magic numbers live here; nowhere else.
"""

from dataclasses import dataclass
from pathlib import Path

_ASSET_DIR = Path(__file__).resolve().parent.parent / "assets"


@dataclass(frozen=True)
class _GameConfig:
    # Window
    TITLE: str = "Flappy Bob"
    SCREEN_WIDTH: int = 640
    SCREEN_HEIGHT: int = 720
    FPS: int = 60

    # Colors  (R, G, B)
    COLOR_BG: tuple[int, int, int] = (15, 15, 25)
    COLOR_PRIMARY: tuple[int, int, int] = (80, 200, 255)
    COLOR_ACCENT: tuple[int, int, int] = (255, 80, 120)
    COLOR_TEXT: tuple[int, int, int] = (230, 230, 230)
    COLOR_GRID: tuple[int, int, int] = (30, 30, 50)

    # Assets (official IBM Bob artwork, see assets/README.md). Already prepared: do not
    # download or generate images. Renderer loads these through Renderer._load_sprite().
    SPRITE_BOB: str = str(_ASSET_DIR / "bob.png")  # head with hard hat, transparent
    SPRITE_BOB_SIZE: tuple[int, int] = (64, 61)
    SPRITE_LOGO: str = str(_ASSET_DIR / "logo.png")  # full mascot, transparent
    SPRITE_LOGO_SIZE: tuple[int, int] = (155, 240)

    # Game-specific constants — IBM Bob will add more here
    # Example: GRAVITY: float = 1500.0
    # Example: PIPE_GAP: int = 190
    # Example: PIPE_SPEED_START: float = 160.0


GameConfig = _GameConfig()
