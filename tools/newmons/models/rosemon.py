"""Rosemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the queen of flowers in a crimson bodysuit with green shoulder petals, a rose hood-mask, long golden hair, a white petal cape and a golden thorn whip.
35 blocks. Built by _rosemon.make(look="base").

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _rosemon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "the queen of flowers in a crimson bodysuit with green shoulder petals, a rose hood-mask, long golden hair, a white petal cape and a golden thorn whip"
build = make("rosemon", look="base")
