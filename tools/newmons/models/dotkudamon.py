"""Dot Kudamon (a Digimon of the CobbleEffort: Digital crossover; after the pixel-sprite art on wikimon.net): a little white fox of chunky pixel blocks with tall ears, red eyes, a gold-and-black bullet ornament on its ear and red-tipped paws. Its
sprite turned into a block figure (each pixel 2 units). Child stage, 1 block tall.

Front is -z, y is up. 22 units tall.
"""
from _digi import sized
from _dot import make

HEIGHT = 22
SCALE, HITBOX = sized(1.0, HEIGHT, 1.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a little white fox of chunky pixel blocks with tall ears, red eyes, a gold-and-black bullet ornament on its ear and red-tipped paws"
ROWS = ['..WW....WW..', '..WW...WWK..', '.WWWWWWWWYW.', '.WWWWWWWWWW.', '.WRWWWWWWRW.', '.WWWWWWWWWW.', 'RWWWWWWWWWWR', '...WWWWWW...', '..WWWWWWWW..', '..WWWWWWWW..', '..RR....RR..']
BASE = {'W': (246, 246, 248), 'R': (230, 40, 40), 'K': (30, 30, 34), 'Y': (240, 200, 40)}
SHINY = {'W': (240, 220, 160), 'R': (60, 120, 230)}
build = make("dotkudamon", ROWS, BASE, SHINY, px=2.0, depth=6, head_rows=2, leg_rows=1, deep={'R': 7, 'K': 7, 'Y': 7})
