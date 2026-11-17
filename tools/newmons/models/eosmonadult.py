"""Eosmon (Adult) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the program of the dawn, a floating cluster of faceted blue crystal with crystal claws, an eye-like core, translucent hexagon-tiled wings and a glowing golden ring.
15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from _digi import sized
from _eosmon import make

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "floater"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a floating cluster of faceted blue crystal with crystal claws, an eye-like core, hexagon-tiled wings and a golden ring"
build = make("eosmonadult", "adult")
