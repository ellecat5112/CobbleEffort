"""King Hangyomon (a Digimon of the CobbleEffort: Digital crossover; after its pixel-sprite art on wikimon.net, the
only picture there is): a crowned fish-man king in violet scale armour with a pale head, a golden crown, a red cape
and a trident, from a game sprite turned into a block figure (each pixel 2 units). 35 blocks tall (no level on wikimon:
built as Ultimate, a king of Hangyomon).

Front is -z, y is up. 44 units tall; Ultimate stage.
"""
from _digi import sized
from _dot import make

HEIGHT = 44
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 6}
LOOK = "a crowned fish-man king in violet scale armour with a pale head, a golden crown, a red cape and a trident, as a block-figure pixel sprite"
ROWS = ['........Y.Y.Y.........',
        '........YYYYY.........',
        '.......WWWWWWW........',
        '......WWBWWWBWW.......',
        '......WWWWWWWWW.......',
        '.......WWRRRWW........',
        'T......VVVVVVV........',
        'TT...VVVVGGGVVVV......',
        'T.T.VVVVVGGGVVVVV.....',
        'T..VVV.VVVVVVV.VVV....',
        'T..WW..VVVVVVV..WW....',
        'T......VVVYVVV........',
        'T.....RVVVVVVVR.......',
        'T.....RVVV.VVVR.......',
        'T.....RVV...VVR.......',
        'T......VV...VV........',
        'T......VV...VV........',
        '......WWW...WWW.......',
        '.....WWWW...WWWW......']
BASE = {'Y': (250, 210, 60), 'W': (230, 226, 240), 'B': (24, 24, 40), 'R': (200, 40, 50), 'V': (110, 70, 170),
        'G': (90, 220, 160), 'T': (220, 200, 120)}
SHINY = {'V': (60, 140, 120), 'R': (60, 80, 200)}
build = make("kinghangyomon", ROWS, BASE, SHINY, px=2.0, depth=5, head_rows=6, leg_rows=4,
             deep={'T': 1, 'R': 2, 'Y': 3}, front={'B': 0.2})
