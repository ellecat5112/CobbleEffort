"""Metal Greymon: "G" Erosion Mode (a Digimon of the CobbleEffort: Digital crossover; built after the official art on wikimon.net): MetalGreymon eaten away by corruption: its hide charcoal-black except one orange arm and leg, silver armour, a red crest and wings of jagged magenta spikes.
The Agumon line's MetalGreymon body with its own colours (_greyvar.make). Perfect stage, 25 blocks tall.

Front is -z, y is up. 42 units tall (the wings); baseScale 9.7 like MetalGreymon.
"""
from __future__ import annotations

from _greyvar import make

SCALE = 9.7
HITBOX = [1.6, 2.6]
KIND = "biped"
K = 3
HEIGHT = 42
ANIM = {"leg_amp": 12}
LOOK = "MetalGreymon eaten away by corruption: its hide charcoal-black except one orange arm and leg, silver armour, a red crest and wings of jagged magenta spikes"
build = make("metalgreymongerosionmode", metal=True,
             base={"orange": (54, 50, 56), "orange_dark": (26, 24, 28), "belly": (90, 86, 96), "stripe": (60, 110, 200), "helmet": (200, 204, 214), "helmet_dark": (130, 134, 146), "wing": (210, 40, 200), "wing_dark": (110, 14, 120), "eye": (60, 120, 250)},
             shiny={"orange": (200, 200, 210), "orange_dark": (140, 140, 150), "wing": (60, 220, 160), "wing_dark": (20, 120, 80)})
