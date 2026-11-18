"""Growmon (Orange) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
an orange Growmon with black markings, a white mane, a Hazard belly, white elbow blades and claws. Adult stage, 15 blocks tall.

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
LOOK = "an orange Growmon with black markings, a white mane, a Hazard belly, white elbow blades and claws"
build = make("growmonorange", "adult", colours={'hide': (240, 160, 40), 'hide_dark': (180, 100, 14), 'hide_light': (255, 210, 120), 'mark': (40, 30, 24)}, shiny_colours={'hide': (60, 58, 66), 'hide_dark': (24, 22, 28)})
