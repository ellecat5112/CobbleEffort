"""Growmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
a big red dinosaur with black markings, a white Hazard belly, a white mane, bat-wing ears, white elbow blades and claws. Adult stage, 15 blocks tall.

Front is -z, y is up. 44 units tall. Built by _guilmon.make().
"""
from __future__ import annotations

from _digi import sized
from _guilmon import make

HEIGHT = 44
SCALE, HITBOX = sized(15, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a big red dinosaur with black markings, a white Hazard belly, a white mane, bat-wing ears, white elbow blades and claws"
build = make("growmon", "adult", colours=None, shiny_colours=None)
