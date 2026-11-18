"""Garudamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the great bird-man: a muscular red-feathered giant with a hawk's head under a red helm, a white
feather beard, great red wings striped gold and yellow, red trousers with white bands and yellow talons. 25 blocks.

Front is -z, y is up. 64 units tall; Perfect stage. Built by _garudamon.make().
"""
from __future__ import annotations

from _digi import sized
from _garudamon import make

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a muscular red-feathered bird-man with a hawk's head, a white beard, great red-and-gold wings and yellow talons"
build = make("garudamon")
