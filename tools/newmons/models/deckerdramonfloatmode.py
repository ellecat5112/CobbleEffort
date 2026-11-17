"""Deckerdramon Float Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Deckerdramon turned hovercraft, riding on two great black hex-panelled pontoons with its snout tucked low at the front.
15 blocks tall.

Front is -z, y is up. 18 units tall; Adult stage.
"""
from _digi import sized
from _deckerdramon import make

HEIGHT = 18
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a hovercraft hull on two black hex-panelled pontoons with a crocodile snout tucked low at the front"
build = make("deckerdramonfloatmode", float_mode=True)
