"""Were Garurumon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Were Garurumon changed by the X-Antibody: a towering wolf-man in heavy blue-steel armour plates with a fan of blade-spines at its back and long claws. 25 blocks.

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
LOOK = "Were Garurumon changed by the X-Antibody: a towering wolf-man in heavy blue-steel armour plates with a fan of blade-spines at its back and long claws"
build = make("weregarurumonxantibody", "x")
