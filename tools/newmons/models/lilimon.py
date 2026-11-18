"""Lilimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the flower fairy: a small fairy in a pink petal dress with a tulip-bell skirt, a pink bud hat, green hair, leaf sleeves and boots with yellow flowers, and four big green leaf wings.
25 blocks tall. Built by _lilimon.make(x=False), fully clothed as drawn.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

from _digi import sized
from _lilimon import make

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a small fairy in a pink petal dress with a tulip-bell skirt, a pink bud hat, green hair, leaf sleeves and boots with yellow flowers, and four big green leaf wings"
build = make("lilimon", x=False)
