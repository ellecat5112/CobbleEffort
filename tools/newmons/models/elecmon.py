"""Elecmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a little red four-legged electric beast striped with blue, with big blue eyes, long pointed ears and a huge fan of nine crackling tail feathers.
Child stage, 1 block tall.

Front is -z, y is up. 24 units tall; Child stage.
"""
from _digi import sized
from _elecmon import make

HEIGHT = 24
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a little red electric beast striped with blue, with long pointed ears and a huge fan of nine tail feathers"
build = make("elecmon")
