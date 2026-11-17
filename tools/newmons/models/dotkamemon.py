"""Dot Kamemon (a Digimon of the CobbleEffort: Digital crossover; after the pixel-sprite art on wikimon.net): a little green turtle of chunky pixel blocks under a big blue helmet, with black eyes, an orange shell front with a yellow plate, green arms and white feet. Its
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
LOOK = "a little green turtle of chunky pixel blocks under a big blue helmet, with black eyes, an orange shell front with a yellow plate, green arms and white feet"
ROWS = ['...BBBBBB...', '..BBBBBBBB..', '.BBBBBBBBBB.', 'BBBBBBBBBBBB', '.GGKGGGGKGG.', '.GGKGGGGKGG.', '..GGGGGGGG..', 'GGOOOYYOOOGG', 'G.OOOYYOOO.G', '..OOOOOOOO..', '..GG....GG..', '.WWW....WWW.']
BASE = {'B': (40, 110, 230), 'G': (100, 230, 120), 'K': (20, 20, 24), 'O': (250, 140, 40), 'Y': (250, 230, 50), 'W': (240, 240, 240)}
SHINY = {'B': (230, 60, 60), 'G': (230, 230, 120)}
build = make("dotkamemon", ROWS, BASE, SHINY, px=2.0, depth=4, head_rows=6, leg_rows=2, deep={'K': 7, 'Y': 7, 'O': 6, 'B': 7})
