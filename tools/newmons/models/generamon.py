"""Generamon (a Digimon of the CobbleEffort: Digital crossover; after its pixel-sprite art on wikimon.net, the only
picture there is): a jagged 16 x 16 monochrome virtual-pet sprite, all dark pixels, turned into a block figure (each
pixel 2 units, the gaps left open). Perfect stage, 25 blocks tall.

Front is -z, y is up. 32 units tall.
"""
from _digi import sized
from _dot import make

HEIGHT = 32
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "floater"
K = 4
LOOK = "a jagged monochrome virtual-pet sprite of dark pixels turned into a block figure"
ROWS = ['..A....AAA..AAA.', '.AAA..A...AAA..A', '.A.A.AAAAA.AAA.A', '.A.AA.....AA.A.A', '.A.AA.AA.AAA.AAA',
        '.A.AA.....A...A.', '.A.A.AAAAAAAAA..', '.A.AAA..A.AAAAAA', '.A.A.AAA..AA.A.A', 'AAAAA....A.AAAAA',
        '.AAAAAAAAAAA.A.A', 'A..A.A..A..A.A.A', '.AAAAA..AAAAAAAA', '..A.AAAAAA..AAA.', '.A....A.A....A..',
        '.AAAAAA.AAAAAA..']
BASE = {'A': (40, 44, 40)}
SHINY = {'A': (60, 120, 70)}
build = make("generamon", ROWS, BASE, SHINY, px=2.0, depth=4)
