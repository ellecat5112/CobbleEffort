"""Pegasmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Armor Digimon of hope: an orange-coated winged horse armoured in gold with a horned helm, gem-set greaves, a long pale mane and great golden-white feathered wings. 15 blocks long.

Front is -z, y is up. 40 units tall; Adult (Armor) stage. Built by _pegasmon.make(x=False).
"""
from __future__ import annotations

from _digi import sized
from _pegasmon import make

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 4.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "the Armor Digimon of hope: an orange-coated winged horse armoured in gold with a horned helm, gem-set greaves, a long pale mane and great golden-white feathered wings"
build = make("pegasmon", x=False)
