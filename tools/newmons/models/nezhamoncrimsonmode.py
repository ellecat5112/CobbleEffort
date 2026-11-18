"""Nezhamon: Crimson Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Nezhamon in red armour wielding a flaming blade in each hand, riding its Wind-Fire Wheels turned into a blazing motorcycle. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage. Built by _nezhamon.make(crimson=True).
"""
from __future__ import annotations

from _digi import sized
from _nezhamon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "Nezhamon in red armour wielding a flaming blade in each hand, riding its Wind-Fire Wheels turned into a blazing motorcycle"
build = make("nezhamoncrimsonmode", crimson=True)
