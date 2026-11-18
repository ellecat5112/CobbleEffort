"""Megidramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a crimson armoured evil dragon on a coiled red-and-white serpent tail, a white ribcage, gold-clawed arms, a horned dragon head and great bat wings burning yellow. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage. Built by _megidramon.make(look="base").
"""
from __future__ import annotations

from _digi import sized
from _megidramon import make

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "a crimson armoured evil dragon on a coiled red-and-white serpent tail, a white ribcage, gold-clawed arms, a horned dragon head and great bat wings burning yellow"
build = make("megidramon", look="base")
