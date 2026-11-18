"""Metal Greymon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; built after the official art on wikimon.net): MetalGreymon changed by the X-Antibody: its orange body striped deep blue, a red mane of spines, blue steel armour and spiked wings of blue light.
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
LOOK = "MetalGreymon changed by the X-Antibody: its orange body striped deep blue, a red mane of spines, blue steel armour and spiked wings of blue light"
build = make("metalgreymonxantibody", metal=True,
             base={"stripe": (24, 40, 120), "helmet": (60, 90, 170), "helmet_dark": (24, 40, 110), "wing": (40, 90, 200), "wing_dark": (14, 40, 120), "metal": (90, 120, 200), "metal_dark": (40, 60, 130), "metal_light": (170, 200, 250)},
             shiny={"orange": (64, 62, 70), "orange_dark": (40, 38, 46), "wing": (200, 60, 60), "wing_dark": (120, 20, 20)})
