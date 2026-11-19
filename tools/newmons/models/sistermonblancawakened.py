"""Sistermon Blanc (Awakened) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
Sistermon Blanc awakened: her pink wings spread wide and her trident blazing with light. Built covered: a full-length habit. 1 block. Built by _sistermon.make("blanc", awake=True).

Front is -z, y is up. 64 units tall; Child stage.
"""
from __future__ import annotations

from _digi import sized
from _sistermon import make

HEIGHT = 64
SCALE, HITBOX = sized(1, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Sistermon Blanc awakened: her pink wings spread wide and her trident blazing with light"
build = make("sistermonblancawakened", "blanc", awake=True)
