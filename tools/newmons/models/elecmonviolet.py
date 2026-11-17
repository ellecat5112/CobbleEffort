"""Elecmon (Violet) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Elecmon's violet cousin, purple striped with yellow, with red eyes and a violet tail fan streaked with yellow.
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
LOOK = "a little purple electric beast striped with yellow, with red eyes, long ears and a violet tail fan streaked yellow"
build = make("elecmonviolet", violet=True)
