"""Sistermon Ciel (Awakened) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
Sistermon Ciel awakened: a golden lightning blade and her cloak torn into wings. Built covered: a full-length habit. 15 blocks. Built by _sistermon.make("ciel", awake=True).

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
LOOK = "Sistermon Ciel awakened: a golden lightning blade and her cloak torn into wings"
build = make("sistermoncielawakened", "ciel", awake=True)
