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

    # Colors  (R, G, B) — IBM Carbon.
    COLOR_BG: tuple[int, int, int] = (22, 22, 22)
    COLOR_PRIMARY: tuple[int, int, int] = (15, 98, 254)
    COLOR_ACCENT: tuple[int, int, int] = (250, 77, 86)
    COLOR_TEXT: tuple[int, int, int] = (241, 194, 27)  # yellow: score, lines, hints

    # Text box: the only allowed backing behind text (no outline, shadow or glow).
    TEXT_BOX_COLOR: tuple[int, int, int] = (0, 0, 0)
    TEXT_BOX_ALPHA: int = 160
    TEXT_BOX_PADDING: int = 8

    # Assets (official IBM Bob artwork, see assets/README.md). Already prepared: do not
    # download or generate images. Renderer loads these through Renderer._load_sprite().
    SPRITE_BOB: str = str(_ASSET_DIR / "bob.png")  # head with hard hat, transparent
    SPRITE_BOB_SIZE: tuple[int, int] = (64, 61)
    SPRITE_LOGO: str = str(_ASSET_DIR / "logo.png")  # full mascot, transparent
    SPRITE_LOGO_SIZE: tuple[int, int] = (155, 240)

    # Game-specific constants — IBM Bob will add more here (physics, pipes, stages, texts)


GameConfig = _GameConfig()
