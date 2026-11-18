"""Ofanimon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Ofanimon changed by the X-Antibody: brighter teal armour, a red plume, translucent crystal wings and a golden wheel at her feet. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage. Built covered (full armour). Built by _ofanimon.make(look="x").
"""
from __future__ import annotations

from _digi import sized
from _ofanimon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = "Ofanimon changed by the X-Antibody: brighter teal armour, a red plume, translucent crystal wings and a golden wheel at her feet"
build = make("ofanimonxantibody", look="x")
