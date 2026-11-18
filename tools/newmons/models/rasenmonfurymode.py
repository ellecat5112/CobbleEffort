"""Rasenmon: Fury Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): a nine-tailed violet beast of rage with long golden claws and nine great coiling blue tails webbed with
glowing lines. 35 blocks. Built by _rasenmon.make(fury=True).

Front is -z, y is up. 60 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _rasenmon import make

HEIGHT = 60
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a nine-tailed violet-and-black striped beast of rage with long golden claws and nine coiling blue tails webbed with light"
build = make("rasenmonfurymode", fury=True)
