"""Sistermon Noir (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
a nun in a black habit with a white collar and cat-eared hood, long black hair and two silver pistols. Built covered: a full-length habit. 15 blocks. Built by _sistermon.make("noir", awake=False).

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
LOOK = "a nun in a black habit with a white collar and cat-eared hood, long black hair and two silver pistols"
build = make("sistermonnoir", "noir", awake=False)
