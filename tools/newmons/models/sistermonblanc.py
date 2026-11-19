"""Sistermon Blanc (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
a little nun in a white habit with gold crosses, a pink rabbit-eared hood, pink feathered wings and a golden trident. Built covered: a full-length habit. 1 block. Built by _sistermon.make("blanc", awake=False).

Front is -z, y is up. 64 units tall; Child stage.
"""
from __future__ import annotations

from _digi import sized
from _sistermon import make

HEIGHT = 64
SCALE, HITBOX = sized(1, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a little nun in a white habit with gold crosses, a pink rabbit-eared hood, pink feathered wings and a golden trident"
build = make("sistermonblanc", "blanc", awake=False)
