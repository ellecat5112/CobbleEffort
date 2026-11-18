"""Mirage Gaogamon: Burst Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the wolf knight in silver-white armour with a mane of white blade-feathers, golden energy blades flaring from its gauntlets and a crescent of golden light behind it. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage. Built by _miragegaogamon.make(burst=True).
"""
from __future__ import annotations

from _digi import sized
from _miragegaogamon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "the wolf knight in silver-white armour with a mane of white blade-feathers, golden energy blades flaring from its gauntlets and a crescent of golden light behind it"
build = make("miragegaogamonburstmode", burst=True)
