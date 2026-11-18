"""Ofanimon Core (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Ofanimon's core: blue armour and wings of golden flame, after its pixel sprite. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage. Built covered (full armour). Built by _ofanimon.make(look="core").
"""
from __future__ import annotations

from _digi import sized
from _ofanimon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = "Ofanimon's core: blue armour and wings of golden flame, after its pixel sprite"
build = make("ofanimoncore", look="core")
