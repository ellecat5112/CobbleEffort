"""Greymon (Blue) (a Digimon of the CobbleEffort: Digital crossover; built after the official art on wikimon.net): a blue Greymon with black tiger stripes, a grey skull helmet and lavender claws.
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
LOOK = "a blue Greymon with black tiger stripes, a grey skull helmet and lavender claws"
build = make("greymonblue", base={'orange': (70, 110, 200), 'orange_dark': (40, 70, 150), 'belly': (140, 170, 230), 'stripe': (24, 26, 40), 'helmet': (140, 140, 150), 'helmet_dark': (90, 90, 100), 'claw': (200, 190, 240), 'eye': (250, 220, 60)}, shiny={'orange': (70, 70, 80), 'orange_dark': (40, 40, 48)})
