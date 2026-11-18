"""Mad Leomon (Final Mode) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the undead lion-man grown into a towering violet beast with a wild red mane, bone spikes
all over, red claws and a loincloth. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect (no level on wikimon) stage. Built by _madleomon.make(mode="final").
"""
from __future__ import annotations

from _digi import sized
from _madleomon import make

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "an undead lion-man grown into a towering violet beast with a wild red mane, bone spikes all over, red claws and a loincloth"
build = make("madleomonfinalmode", mode="final")
