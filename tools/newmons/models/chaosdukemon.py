"""Chaos Dukemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): the fallen knight: blackened Holy Knight armour, a tall plumed helm, a great round black shield, a long black lance and a tattered violet-black cape. 35 blocks tall.

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
LOOK = "the fallen knight: blackened Holy Knight armour, a tall plumed helm, a great round black shield, a long black lance and a tattered violet-black cape"

build = make("chaosdukemon", core=False)
