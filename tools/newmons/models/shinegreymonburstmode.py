"""Shine Greymon: Burst Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a radiant light dragon-man in red-and-white armour with wings of roaring flame, a flame sword and a flame shield.
35 blocks. Built by _shinegreymon.make(look="burst").

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _shinegreymon import make

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a radiant light dragon-man in red-and-white armour with wings of roaring flame, a flame sword and a flame shield"
build = make("shinegreymonburstmode", look="burst")
