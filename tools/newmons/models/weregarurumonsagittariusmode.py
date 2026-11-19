"""Were Garurumon: Sagittarius Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Were Garurumon armed as the archer: sleek blue fur under blue-steel armour, a great crossbow-gauntlet and blades of ice-blue light fanned behind it. 25 blocks.

Front is -z, y is up. Perfect stage. Built by _weregarurumon.make.
"""
from __future__ import annotations

from _digi import sized
from _weregarurumon import make

HEIGHT = 62
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "Were Garurumon armed as the archer: sleek blue fur under blue-steel armour, a great crossbow-gauntlet and blades of ice-blue light fanned behind it"
build = make("weregarurumonsagittariusmode", "sagittarius")
