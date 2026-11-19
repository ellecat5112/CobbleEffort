"""Sleipmon: Burst Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the Royal Knight centaur in radiant silver-white armour with golden crystal wings and a crossbow.
35 blocks. Built by _sleipmon.make(look="burst").

Front is -z, y is up. 72 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _sleipmon import make

HEIGHT = 72
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "the Royal Knight centaur in radiant silver-white armour with golden crystal wings and a crossbow"
build = make("sleipmonburstmode", look="burst")
