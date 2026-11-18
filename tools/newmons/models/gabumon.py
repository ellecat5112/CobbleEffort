"""Gabumon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
shy reptile who wears a Garurumon's pelt: a stocky yellow body under a white, blue-striped wolf pelt with a ridged
horn, red eyes, a toothy grin, red claws and an emblem on its belly. Child stage, 1 block tall.

Front is -z, y is up. 30 units tall. Built by _gabumon.make().
"""
from __future__ import annotations

from _digi import sized
from _gabumon import make

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 14}
LOOK = "a stocky yellow reptile under a white blue-striped wolf pelt with a ridged horn, red eyes and red claws"
build = make("gabumon")
