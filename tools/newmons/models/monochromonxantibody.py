"""Monochromon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Monochromon changed by the X-Antibody: black armour plating, a towering blade horn edged red, steel claws and a curved blade on its tail. 15 blocks long.

Front is -z, y is up. 34 units tall; Adult stage. Built by _monochromon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _monochromon import make

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 4.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "Monochromon changed by the X-Antibody: black armour plating, a towering blade horn edged red, steel claws and a curved blade on its tail"
build = make("monochromonxantibody", x=True)
