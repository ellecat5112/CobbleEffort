"""Dot Mirage Gaogamon (a Digimon of the CobbleEffort: Digital crossover; after the pixel-sprite art on wikimon.net): a towering blue-armoured wolf knight of chunky pixel blocks with a gold-crested helm, yellow eyes, a red chest gem, gold-trimmed gauntlets and a flowing blue cape. Its
sprite turned into a block figure (each pixel 2 units). Ultimate stage, 35 blocks tall.

Front is -z, y is up. 30 units tall.
"""
from _digi import sized
from _dot import make

HEIGHT = 30
SCALE, HITBOX = sized(35.0, HEIGHT, 1.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a towering blue-armoured wolf knight of chunky pixel blocks with a gold-crested helm, yellow eyes, a red chest gem, gold-trimmed gauntlets and a flowing blue cape"
ROWS = ['.....GG.......', '....BBBB......', '...BBBBBB.....', '...BYBBYB.....', '...BBWWBB.....', '.GBBBBBBBBG...', 'BBBBBRRBBBBB..', 'BBGBBBBBBGBBC.', 'GG.BBBBBB.GGCC', 'GG.BBBBBB.GGCC', '...BBGGBB...CC', '...BBBBBB...C.', '...BBB.BBB....', '...BBB.BBB....', '..GGGG.GGGG...']
BASE = {'B': (40, 80, 200), 'G': (240, 200, 60), 'Y': (250, 230, 60), 'W': (240, 240, 244), 'R': (220, 40, 40), 'C': (30, 50, 140)}
SHINY = {'B': (120, 120, 140), 'C': (80, 80, 100)}
build = make("dotmiragegaogamon", ROWS, BASE, SHINY, px=2.0, depth=6, head_rows=5, leg_rows=3, deep={'R': 7, 'Y': 7, 'C': 2, 'G': 7})
