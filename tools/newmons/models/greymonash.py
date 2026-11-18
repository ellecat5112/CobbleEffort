"""Greymon (Ash) (a Digimon of the CobbleEffort: Digital crossover; built after the official art on wikimon.net): the ash-grey Greymon of the old virtual pet: a grey tyrant with pale pink stripes, a dark helmet, red eyes.
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
LOOK = "the ash-grey Greymon of the old virtual pet: a grey tyrant with pale pink stripes, a dark helmet, red eyes"
build = make("greymonash", base={'orange': (130, 128, 136), 'orange_dark': (84, 82, 90), 'belly': (190, 186, 196), 'stripe': (230, 160, 190), 'helmet': (60, 58, 66), 'helmet_dark': (34, 32, 38), 'eye': (230, 40, 40)}, shiny={'orange': (230, 200, 160), 'orange_dark': (180, 140, 100)})
