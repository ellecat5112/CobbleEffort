"""Greymon (Orange) (a Digimon of the CobbleEffort: Digital crossover; built after the official art on wikimon.net): a deep orange Greymon with dark stripes and a silver helmet, from the old virtual pet.
The Agumon line's Greymon body with its own colours (_greyvar.make). Adult stage, 15 blocks tall.

Front is -z, y is up. 41 units tall; baseScale 6.0 like Greymon.
"""
from __future__ import annotations

from _greyvar import make

SCALE = 6.0
HITBOX = [1.6, 2.55]
KIND = "biped"
K = 3
HEIGHT = 41
ANIM = {"leg_amp": 14}
LOOK = "a deep orange Greymon with dark stripes and a silver helmet, from the old virtual pet"
build = make("greymonorange", base={'orange': (220, 110, 30), 'orange_dark': (160, 66, 14), 'belly': (240, 170, 90), 'stripe': (60, 40, 30), 'helmet': (180, 184, 196), 'helmet_dark': (110, 114, 126)}, shiny={'orange': (110, 170, 60), 'orange_dark': (60, 110, 20)})
