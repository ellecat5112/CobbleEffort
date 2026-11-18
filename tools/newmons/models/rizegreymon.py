"""Rize Greymon (a Digimon of the CobbleEffort: Digital crossover; built after the official art on wikimon.net): the Savers Greymon armed: its orange hide striped blue, crimson cyborg armour, a great revolver-arm and wings of white-and-red blade feathers.
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
LOOK = "the Savers Greymon armed: its orange hide striped blue, crimson cyborg armour, a great revolver-arm and wings of white-and-red blade feathers"
build = make("rizegreymon", metal=True,
             base={"metal": (200, 40, 40), "metal_dark": (110, 14, 14), "metal_light": (240, 130, 130), "wing": (230, 230, 236), "wing_dark": (200, 40, 40), "helmet": (180, 184, 196), "helmet_dark": (90, 94, 108)},
             shiny={"orange": (64, 62, 70), "orange_dark": (40, 38, 46)})
