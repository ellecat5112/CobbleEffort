"""Splashmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a slender water-man in a gold-banded white bodysuit with long flowing lilac wave hair and a glassy bubble of water in one hand.
25 blocks. Built by _splashmon.make(mode="base").

Front is -z, y is up. 70 units tall; Perfect stage.
"""
from __future__ import annotations

from _digi import sized
from _splashmon import make

HEIGHT = 70
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a slender water-man in a gold-banded white bodysuit with long flowing lilac wave hair and a glassy bubble of water in one hand"
build = make("splashmon", mode="base")
