"""Splashmon Darkness Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a raging liquid tiger-dragon of white-blue water with a fanged maw, golden claws and splashing droplets.
25 blocks. Built by _splashmon.make(mode="beast").

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

from _digi import sized
from _splashmon import make

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a raging liquid tiger-dragon of white-blue water with a fanged maw, golden claws and splashing droplets"
build = make("splashmondarknessmode", mode="beast")
