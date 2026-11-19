"""Venom Vamdemon Undead (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Venom Vamdemon rotting and undead: darker red hide streaked with bone white, shredded bat wings
trailing smoke, grey-furred legs and sickly grey-blue claws. 35 blocks.

Front is -z, y is up. Ultimate stage (by analogy: wikimon gives no level). Built by _venomvamdemon.make.
"""
from __future__ import annotations

from _digi import sized
from _venomvamdemon import make

HEIGHT = 76
SCALE, HITBOX = sized(35, HEIGHT, 8.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a rotting towering demon with shredded smoking bat wings, grey-furred legs and sickly grey-blue claws"
build = make("venomvamdemonundead", True)
