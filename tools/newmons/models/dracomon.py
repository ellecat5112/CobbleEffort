"""Dracomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a sturdy little teal dragon with a cream belly, red antler horns, small red bat wings, red eyes, a toothy grin and a long tail.
Child stage, 1 block tall.

Front is -z, y is up. 30 units tall; Child stage.
"""
from _digi import sized
from _dracomon import make

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a sturdy little teal dragon with a cream belly, red antler horns, small red bat wings and a toothy grin"
build = make("dracomon")
