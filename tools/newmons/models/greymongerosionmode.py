"""Greymon: "G" Erosion Mode (a Digimon of the CobbleEffort: Digital crossover; built after the official art on
wikimon.net): Greymon being eaten away by corruption: its hide gone charcoal-black from the head down, the orange
showing only on its belly, a dark brown helmet and horns, blue streaks and glowing amber eyes. The Agumon line's
Greymon body with its own colours (_greyvar.make). Adult stage, 15 blocks tall.

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
LOOK = "a charcoal-black corrupted Greymon with an orange belly, a dark brown helmet, blue streaks and amber eyes"
build = make("greymongerosionmode",
             base={"orange": (54, 50, 56), "orange_dark": (26, 24, 28), "belly": (240, 160, 40),
                   "stripe": (60, 110, 200), "helmet": (80, 50, 36), "helmet_dark": (46, 28, 20),
                   "eye": (250, 180, 40)},
             shiny={"orange": (200, 200, 210), "orange_dark": (140, 140, 150), "belly": (120, 200, 250)})
