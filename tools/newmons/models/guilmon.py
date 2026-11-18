"""Guilmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the Tamers' red dinosaur: a red reptile with black Hazard-like markings, a white belly with the Hazard emblem, bat-wing ears, fierce yellow eyes and white claws. Child stage, 1.0 block tall.

Front is -z, y is up. 34 units tall. Built by _guilmon.make().
"""
from __future__ import annotations

from _digi import sized
from _guilmon import make

HEIGHT = 34
SCALE, HITBOX = sized(1.0, HEIGHT, 1.0)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 16}
LOOK = "the Tamers' red dinosaur: a red reptile with black Hazard-like markings, a white belly with the Hazard emblem, bat-wing ears, fierce yellow eyes and white claws"
build = make("guilmon", "child", colours=None, shiny_colours=None)
