"""Goddramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the holy dragon-god of the west, one of the Four Great Dragons: a dragon-man with a lion-like
mane, a horned silver helm, a golden robe with red-banded sleeves, a silver serpentine tail curling through clouds and
great fans of white feathered wings. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage. Built by _goddramon.make().
"""
from __future__ import annotations

from _digi import sized
from _goddramon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = ("a dragon-man with a lion-like mane, a horned silver helm, a golden robe, a silver serpentine tail through clouds "
        "and great fans of white wings")
build = make("goddramon")
