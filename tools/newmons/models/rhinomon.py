"""Rhinomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
Armor Digimon of knowledge: a golden-armoured rhinoceros with a long silver drill horn and red gems. 15 blocks. Built by
_rhinomon.make(x=False).

Front is -z, y is up. 30 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _rhinomon import make

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a sturdy golden-armoured rhinoceros with a long silver drill horn, scrolled gold plates set with red gems and golden hooves"
build = make("rhinomon", x=False)
