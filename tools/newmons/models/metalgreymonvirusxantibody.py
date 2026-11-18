"""Metal Greymon (Virus) (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; built after the official art on wikimon.net): the virus MetalGreymon changed by the X-Antibody: an indigo body, silver armour, a pink mane of spines and wings of crackling violet light.
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
LOOK = "the virus MetalGreymon changed by the X-Antibody: an indigo body, silver armour, a pink mane of spines and wings of crackling violet light"
build = make("metalgreymonvirusxantibody", metal=True,
             base={"orange": (60, 60, 140), "orange_dark": (26, 26, 80), "belly": (130, 140, 210), "stripe": (180, 60, 140), "helmet": (210, 214, 226), "helmet_dark": (130, 134, 150), "wing": (190, 160, 240), "wing_dark": (120, 90, 200), "eye": (90, 230, 250)},
             shiny={"orange": (60, 130, 90), "orange_dark": (24, 70, 40), "belly": (150, 220, 170), "wing": (240, 200, 120)})
