"""Chaos Dukemon Core (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): Chaos Dukemon's data core: the fallen knight rendered as a pale blue spectre with its shield, lance and cape. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

from _chaosdukemon import make
from _digi import sized

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "Chaos Dukemon's data core: the fallen knight rendered as a pale blue spectre with its shield, lance and cape"

build = make("chaosdukemoncore", core=True)
