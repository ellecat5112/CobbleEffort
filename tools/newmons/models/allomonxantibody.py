"""Allomon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Allomon awakened by the X-Antibody. A lighter blue hide with crimson-and-pink bands,
a shaggy brown fur mantle over its shoulders with a white fringe, a war bonnet of black-tipped white feathers running
from its crown down its back, a gold medallion necklace and a gaping fanged mouth. 15 blocks tall.

Front is -z, y is up. 50 units tall; Adult stage. Built by allomon.make.
"""
from __future__ import annotations

from allomon import BASE as _B, HEIGHT, K, KIND, SCALE, HITBOX, ANIM, make

LOOK = ("a light blue dinosaur with crimson-and-pink bands, a shaggy brown fur mantle, a war bonnet of black-tipped "
        "white feathers down its back, a gold medallion necklace and a fanged mouth")
BASE = dict(_B, blue=(70, 150, 226), blue_dark=(30, 80, 160), blue_light=(140, 200, 250), belly=(170, 220, 250),
            band=(200, 30, 70), band2=(250, 120, 170))
SHINY = {"blue": (230, 150, 60), "blue_dark": (150, 80, 20), "blue_light": (255, 210, 130), "belly": (255, 230, 180),
         "belly_dark": (220, 180, 120), "band": (40, 40, 160), "band2": (100, 140, 240), "mantle": (60, 60, 70),
         "mantle_dark": (30, 30, 36), "mantle_light": (110, 110, 124)}
build = make("allomonxantibody", BASE, SHINY, x=True)
