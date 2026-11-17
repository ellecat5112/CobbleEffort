"""Dot Agumon (a Digimon of the CobbleEffort: Digital crossover; after the pixel-sprite art on wikimon.net): a little yellow dinosaur of chunky pixel blocks with green eyes, a toothy grin, stubby clawed arms and big feet. Its
sprite turned into a block figure (each pixel 2 units). Child stage, 1 block tall.

Front is -z, y is up. 26 units tall.
"""
from _digi import sized
from _dot import make

HEIGHT = 26
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a little yellow dinosaur of chunky pixel blocks with green eyes, a toothy grin, stubby clawed arms and big feet"
ROWS = ['....YYYYY...', '...YYYYYYY..', '..YYGYYYGYY.', '..YYYYYYYYY.', '..YWWWWWWWY.', '..YRRRRRRRY.', '...YYYYYYY..', '.YYYYYYYYYYY', 'CY.YYYYYYY.Y', '...YYYYYYY.C', '...YYY.YYY..', '..YYYY.YYYY.', '..CCCC.CCCC.']
BASE = {'Y': (250, 200, 40), 'G': (40, 160, 60), 'W': (250, 250, 250), 'R': (200, 40, 40), 'C': (240, 240, 240)}
SHINY = {'Y': (250, 150, 60)}
build = make("dotagumon", ROWS, BASE, SHINY, px=2.0, depth=4, head_rows=7, leg_rows=3, deep={'G': 5, 'W': 5, 'R': 5, 'C': 3})
