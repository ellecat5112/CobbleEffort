"""Garudamon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after
the official art on wikimon.net): Garudamon awakened by the X-Antibody: a burlier orange-red flyer with a crimson mask
and a white crest, broad brown wings and a lance braced in its arm. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage. Built by _garudamon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _garudamon import make

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 3.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a burly orange-red bird-man with a crimson mask, a white crest, broad brown wings and a lance"
build = make("garudamonxantibody", x=True)
