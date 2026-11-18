"""Metal Greymon (Virus) (a Digimon of the CobbleEffort: Digital crossover; built after the official art on wikimon.net): the virus MetalGreymon: a blue Greymon body half rebuilt in steel, a grey steel helmet and Trident Arm, ragged black-and-violet wings and red spines.
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
LOOK = "the virus MetalGreymon: a blue Greymon body half rebuilt in steel, a grey steel helmet and Trident Arm, ragged black-and-violet wings and red spines"
build = make("metalgreymonvirus", metal=True,
             base={"orange": (70, 100, 190), "orange_dark": (30, 50, 120), "belly": (150, 180, 230), "stripe": (24, 34, 90), "helmet": (150, 154, 166), "helmet_dark": (90, 94, 104), "wing": (60, 50, 120), "wing_dark": (20, 16, 40), "eye": (250, 220, 60)},
             shiny={"orange": (140, 60, 160), "orange_dark": (80, 24, 100), "belly": (220, 170, 230), "wing": (40, 40, 44)})
