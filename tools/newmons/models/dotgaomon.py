"""Dot Gaomon (a Digimon of the CobbleEffort: Digital crossover; after the pixel-sprite art on wikimon.net): a little blue dog of chunky pixel blocks with a red headband, a white face, black eyes and nose, big red gloves and black feet. Its
sprite turned into a block figure (each pixel 2 units). Child stage, 1 block tall.

Front is -z, y is up. 24 units tall.
"""
from _digi import sized
from _dot import make

HEIGHT = 24
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a little blue dog of chunky pixel blocks with a red headband, a white face, black eyes and nose, big red gloves and black feet"
ROWS = ['..BB....BB..', '..BBBBBBBB..', '..RRRRRRRR..', '.BBBBBBBBBB.', '.BKWWWWWWKB.', '.BWWWKKWWWB.', '..WWWWWWWW..', 'RRBBWWWWBBRR', 'RRBBWWWWBBRR', '...BBBBBB...', '...BB..BB...', '..KKK..KKK..']
BASE = {'B': (60, 160, 230), 'R': (220, 40, 50), 'W': (246, 246, 250), 'K': (24, 24, 28)}
SHINY = {'B': (230, 150, 60), 'R': (60, 120, 220)}
build = make("dotgaomon", ROWS, BASE, SHINY, px=2.0, depth=4, head_rows=6, leg_rows=2, deep={'W': 5, 'K': 5, 'R': 6})
