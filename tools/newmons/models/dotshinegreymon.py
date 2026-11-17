"""Dot Shine Greymon (a Digimon of the CobbleEffort: Digital crossover; after the pixel-sprite art on wikimon.net): a towering red-and-gold dragon warrior of chunky pixel blocks with a gold horned helm, blazing gold wings, a red body with gold armour and a sun emblem on its chest. Its
sprite turned into a block figure (each pixel 2 units). Ultimate stage, 35 blocks tall.

Front is -z, y is up. 28 units tall.
"""
from _digi import sized
from _dot import make

HEIGHT = 28
SCALE, HITBOX = sized(35.0, HEIGHT, 1.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a towering red-and-gold dragon warrior of chunky pixel blocks with a gold horned helm, blazing gold wings, a red body with gold armour and a sun emblem on its chest"
ROWS = ['..G........G..', '..GG.RRRR.GG..', '...GRRRRRRG...', '...RGRRRRGR...', '...RRWWWWRR...', 'GG.RRRRRRRR.GG', 'GGGRRGYYGRRGGG', 'GG.RRRYYRRR.GG', 'G.RRGRRRRGRR.G', '..RR.RRRR.RR..', '...GRRRRRRG...', '...RRR..RRR...', '...RRR..RRR...', '..GGGG..GGGG..']
BASE = {'R': (210, 40, 30), 'G': (250, 200, 50), 'Y': (255, 240, 160), 'W': (250, 250, 250)}
SHINY = {'R': (60, 60, 70), 'G': (230, 230, 240)}
build = make("dotshinegreymon", ROWS, BASE, SHINY, px=2.0, depth=6, head_rows=5, leg_rows=3, deep={'Y': 7, 'W': 7, 'G': 3})
