"""Dot Lalamon (a Digimon of the CobbleEffort: Digital crossover; after the pixel-sprite art on wikimon.net): a little pink bud of chunky pixel blocks with a yellow leaf sprout on top, black eyes, a lime-green mouth and leafy lime arms. Its
sprite turned into a block figure (each pixel 2 units). Child stage, 1 block tall.

Front is -z, y is up. 24 units tall.
"""
from _digi import sized
from _dot import make

HEIGHT = 24
SCALE, HITBOX = sized(1.0, HEIGHT, 1.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a little pink bud of chunky pixel blocks with a yellow leaf sprout on top, black eyes, a lime-green mouth and leafy lime arms"
ROWS = ['...YYYYYY...', '....YYYY....', '.....PP.....', '...PPPPPP...', '..PPPPPPPP..', '.PPKKPPKKPP.', '.PPKKPPKKPP.', '.PPPPPPPPPPL', '.PPPLLLLPPPL', '..PLLLLLLP..', '...LLLLLL...', '...LL..LL...']
BASE = {'P': (240, 160, 220), 'Y': (250, 230, 60), 'K': (30, 24, 30), 'L': (170, 240, 90)}
SHINY = {'P': (160, 200, 250), 'L': (250, 200, 90)}
build = make("dotlalamon", ROWS, BASE, SHINY, px=2.0, depth=6, head_rows=3, leg_rows=1, deep={'K': 7, 'L': 7, 'Y': 3})
