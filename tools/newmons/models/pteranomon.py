"""Pteranomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
mechanical pteranodon of blue-steel plates with long red-marked jet wings and missile racks. 15 blocks. Built by
_pteranomon.make(x=False).

Front is -z, y is up. 30 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _pteranomon import make

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "a mechanical pteranodon of blue-steel plates with a long beak, long red-marked jet wings, missile racks and red talons"
build = make("pteranomon", x=False)
