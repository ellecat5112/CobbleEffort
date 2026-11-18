"""Rize Greymon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; built after the official art on wikimon.net): Rize Greymon changed by the X-Antibody: its armour turned black and crimson, glowing gold energy wings and a heavier blade-gun arm.
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
LOOK = "Rize Greymon changed by the X-Antibody: its armour turned black and crimson, glowing gold energy wings and a heavier blade-gun arm"
build = make("rizegreymonxantibody", metal=True,
             base={"metal": (60, 56, 64), "metal_dark": (20, 18, 24), "metal_light": (200, 40, 40), "wing": (250, 210, 90), "wing_dark": (200, 150, 40), "helmet": (200, 40, 40), "helmet_dark": (110, 14, 14)},
             shiny={"orange": (200, 200, 210), "orange_dark": (140, 140, 150)})
