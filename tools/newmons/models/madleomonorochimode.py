"""Mad Leomon (Orochi Mode) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after
the official art on wikimon.net): the undead lion-man in grey plate armour with a golden mane, entwined with long
silver serpents with yellow and white heads. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect (no level on wikimon) stage. Built by _madleomon.make(mode="orochi").
"""
from __future__ import annotations

from _digi import sized
from _madleomon import make

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "an undead lion-man in grey plate armour with a golden mane, entwined with long silver serpents with yellow and white heads"
build = make("madleomonorochimode", mode="orochi")
