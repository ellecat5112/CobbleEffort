"""Growmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
Growmon awakened by the X-Antibody: a lean upright red dinosaur with a pale ridged belly, black bands, a white mane and long white claws. Adult stage, 15 blocks tall.

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
LOOK = "Growmon awakened by the X-Antibody: a lean upright red dinosaur with a pale ridged belly, black bands, a white mane and long white claws"
build = make("growmonxantibody", "adult", colours={'hide': (220, 60, 30), 'hide_dark': (140, 24, 10), 'hide_light': (255, 150, 110), 'belly': (240, 226, 214)}, shiny_colours={'hide': (60, 58, 66)})
