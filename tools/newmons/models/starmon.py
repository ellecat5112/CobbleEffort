"""Starmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a living metal star sheriff with a black face, spiked blue boxing gloves, red-and-blue boots and a golden chain-scarf.
15 blocks. Built by _starmon.make(x=False).

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _starmon import make

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a living metal star sheriff with a black face, spiked blue boxing gloves, red-and-blue boots and a golden chain-scarf"
build = make("starmon", x=False)
