"""Guilmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
Guilmon awakened by the X-Antibody: a sleeker bright red dinosaur with sweeping horn-ears, black bands, a pale belly and long white claws. Child stage, 1.0 block tall.

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
LOOK = "Guilmon awakened by the X-Antibody: a sleeker bright red dinosaur with sweeping horn-ears, black bands, a pale belly and long white claws"
build = make("guilmonxantibody", "child", colours={'hide': (220, 50, 30), 'hide_dark': (140, 20, 10), 'hide_light': (255, 140, 100), 'belly': (230, 210, 190)}, shiny_colours={'hide': (60, 58, 66)})
