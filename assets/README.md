# Assets

Official IBM Bob artwork, downloaded from <https://bob.ibm.com>.

| File | What | Origin |
|------|------|--------|
| `bob.png` | In-game sprite, Bob's head with hard hat, source 96x91 px, used at 64x61, transparent | cut from `source/bob-standing.png` |
| `logo.png` | Full Bob mascot for the Ready screen, 155x240 px, transparent | `source/bob-standing.png` |
| `source/bob-standing.png` | Full mascot, 512x512, transparent | `https://bob.ibm.com/assets/bob-standing-BECrMjXJ.webp` (converted to PNG) |
| `source/bob-standing-BECrMjXJ.webp` | Original download | same URL |
| `source/bob-og.png` | Mascot on light background, 1200x630 | `https://bob.ibm.com/bob-og.png` |
| `source/icon.svg` | Official Bob icon | `https://bob.ibm.com/icon.svg` |

## Usage

- Game code only loads `bob.png` and `logo.png`, via the paths in `game/config.py`.
- Do not download or generate other image files. The files in `source/` are not used by the game.

## Branding note

Bob and the Bob artwork are IBM property. They are used here for an internal IBM presentation
only. Do not redistribute outside IBM.
