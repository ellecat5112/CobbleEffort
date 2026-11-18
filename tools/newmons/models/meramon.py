"""Meramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a hunched man of living flame, dark red-black fire licked all over by orange and yellow flames, a crown of fire, a jagged grin and a ball of fire in its right hand. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage. Built by _meramon.make(x=False).
"""
from __future__ import annotations

from _digi import sized
from _meramon import make

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 2.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a hunched man of living flame, dark red-black fire licked all over by orange and yellow flames, a crown of fire, a jagged grin and a ball of fire in its right hand"
build = make("meramon", x=False)
