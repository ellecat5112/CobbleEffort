"""Greymon (Blue) (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; built after the official art on wikimon.net): a deep blue Greymon slashed with red X-stripes, a black horned helmet and steel tail spike.
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
LOOK = "a deep blue Greymon slashed with red X-stripes, a black horned helmet and steel tail spike"
build = make("greymonbluexantibody", base={'orange': (40, 60, 150), 'orange_dark': (20, 34, 100), 'belly': (80, 110, 190), 'stripe': (210, 30, 40), 'helmet': (40, 38, 46), 'helmet_dark': (20, 18, 24), 'eye': (250, 160, 40)}, shiny={'orange': (200, 200, 210), 'orange_dark': (150, 150, 160)})
