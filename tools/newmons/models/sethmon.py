"""Sethmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a red tiger-striped beast with a pale blue belly, a sweeping white skull-mask with long tusks, a black shark-fin crest and a shaggy green tail.
15 blocks. Built by _sethmon.make(wild=False).

Front is -z, y is up. 30 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _sethmon import make

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a red tiger-striped beast with a pale blue belly, a sweeping white skull-mask with long tusks, a black shark-fin crest and a shaggy green tail"
build = make("sethmon", wild=False)
