"""Sistermon Ciel (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
a nun in a grey-white habit with clover marks, a pale-blue mouse-eared hood, long teal hair, a black cloak and a katana. Built covered: a full-length habit. 15 blocks. Built by _sistermon.make("ciel", awake=False).

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _sistermon import make

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a nun in a grey-white habit with clover marks, a pale-blue mouse-eared hood, long teal hair, a black cloak and a katana"
build = make("sistermonciel", "ciel", awake=False)
