"""Mad Leomon: Armed Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the undead lion-man with one arm turned into a huge spiked chainsaw, a wild black mane
and banded black armour. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage. Built by _madleomon.make(mode="armed").
"""
from __future__ import annotations

from _digi import sized
from _madleomon import make

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "an undead lion-man with one arm turned into a huge spiked chainsaw, a wild black mane and banded black armour"
build = make("madleomonarmedmode", mode="armed")
