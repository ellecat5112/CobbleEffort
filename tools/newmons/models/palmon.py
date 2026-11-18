"""Palmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a little green plant creature with a big pink tropical flower on its head, dark round eyes, long vine arms with violet claws and root feet. 1 block tall.

Front is -z, y is up. 24 units tall; Child stage. Built by _palmon.make(x=False).
"""
from __future__ import annotations

from _digi import sized
from _palmon import make

HEIGHT = 24
SCALE, HITBOX = sized(1, HEIGHT, 1.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a little green plant creature with a big pink tropical flower on its head, dark round eyes, long vine arms with violet claws and root feet"
build = make("palmon", x=False)
