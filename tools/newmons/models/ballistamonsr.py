"""Ballistamon SR (a Digimon of the CobbleEffort: Digital crossover; hand-built after the art on wikimon.net, a manga
drawing): Ballistamon rebuilt for war: a heavier blue-and-red body, a huge drill in place of its right fist and twin
cannons on its back. 25 blocks tall.

Front is -z, y is up. 50 units tall; no level known (Perfect used). Built by ballistamon.make("sr").
"""
from __future__ import annotations

from _digi import sized
from ballistamon import ANIM, BASE, HEIGHT, K, KIND, SHINY, make

SCALE, HITBOX = sized(25, HEIGHT, 2.8)
LOOK = "Ballistamon rebuilt for war: a heavier body, a huge drill arm and twin cannons on its back"
build = make("ballistamonsr", "sr")
