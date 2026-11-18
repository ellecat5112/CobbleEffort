"""Ravmon: Burst Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): the radiant raven in silver-white armour with a dark feather-tail and four vast wings of violet light.
35 blocks. Built by _ravmon.make(burst=True).

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _ravmon import make

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a radiant raven-man in silver-white armour with a dark feather-tail and four vast wings of glowing violet light"
build = make("ravmonburstmode", burst=True)
