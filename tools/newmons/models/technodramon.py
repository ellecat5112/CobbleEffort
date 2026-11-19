"""Technodramon (a Digimon of the CobbleEffort: Digital crossover; after the pixel-sprite art on wikimon.net, its only
picture): a crested machine dragon of chunky pixel blocks in dark gunmetal, with a glowing red eye, a horned head, a
clawed arm and a curling tail. Its sprite turned into a block figure (each pixel 4 units). 35 blocks.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from _digi import sized
from _dot import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a crested gunmetal machine dragon of chunky pixel blocks with a glowing red eye and a curling tail"
ROWS = ['........DDDDDD..', '.....DDDD...D...', '....DDEDD.DDD...', '..DDD..DD...DD..', '.DDDDDDDD.DDD...',
        '.DDDDDDDD.D.....', '..DDDDDDDD......', '....DDDDD.......', '....DDDDDD...DD.', '...DDD.D.DD..DD.',
        '...DD.DD.DD.DDD.', '...DDD..DDDDDDD.', '....DDDDDDDDDD..', '...DDDDDDDDDD...', '...DDDDDDDDDDD..',
        '..DDDDD..DDDDD..']
BASE = {'D': (70, 74, 88), 'E': (255, 60, 50)}
SHINY = {'D': (170, 150, 90)}
build = make("technodramon", ROWS, BASE, SHINY, px=4.0, depth=12, head_rows=8, leg_rows=2, deep={'E': 13})
