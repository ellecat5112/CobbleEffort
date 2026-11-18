"""Master V-dramon (a Digimon of the CobbleEffort: Digital crossover; after its pixel-sprite art on wikimon.net, the
only picture there is): a blue V-dramon with a white belly and V mark, a horn, fanged jaws and clawed hands, from a
game sprite turned into a block figure (each pixel 2 units). 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from _digi import sized
from _dot import make

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 8}
LOOK = "a blue V-dramon with a white belly and V mark, a horn, fanged jaws and clawed hands, as a block-figure pixel sprite"
ROWS = ['.......W..........',
        '......BBB.........',
        '.....BBBBB........',
        '....BBEBBBB.......',
        '....BBBBBBBBB.....',
        '....BBBTTTBB......',
        '.W..BBBBBBB....W..',
        'WWB.BBWWWBBB..BWW.',
        '.WBBBBWYWBBBBBBW..',
        '...BBBWWWBBBB.....',
        '....BBWWWWBB......',
        '....BBBWWBBB......',
        '.....BBBBBB.......',
        '....BBB..BBB......',
        '...BBB....BBB.BBB.',
        '..WBB......BBW.BB.',
        '..WW........WW....']
BASE = {'B': (60, 90, 200), 'W': (240, 240, 250), 'E': (240, 40, 40), 'T': (250, 250, 250), 'Y': (250, 210, 60)}
SHINY = {'B': (40, 140, 90)}
build = make("mastervdramon", ROWS, BASE, SHINY, px=2.0, depth=5, head_rows=6, leg_rows=4, deep={'W': 4, 'Y': 1}, front={'E': 0.2, 'T': 0.2, 'Y': 0.6})
