"""Rampage Greymon (a Digimon of the CobbleEffort: Digital crossover; built after the manga panel on wikimon.net, its
only picture): a Greymon gone berserk in a heap of grafted machinery: the Agumon line's MetalGreymon body with a
rust-orange hide, gunmetal armour, scorched black stripes and wings of grey steel. Perfect stage (no level on
wikimon; by analogy with MetalGreymon), 25 blocks tall.

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
LOOK = "a berserk Greymon of grafted machinery: rust-orange hide, gunmetal armour, scorched black stripes and grey steel wings"
build = make("rampagegreymon", metal=True,
             base={"orange": (170, 90, 50), "orange_dark": (100, 46, 20), "belly": (190, 150, 110), "stripe": (30, 28, 30),
                   "helmet": (110, 114, 124), "helmet_dark": (50, 52, 60), "metal": (120, 124, 134),
                   "metal_dark": (50, 52, 60), "wing": (130, 134, 144), "wing_dark": (60, 62, 70), "eye": (250, 60, 40)},
             shiny={"orange": (120, 120, 140), "orange_dark": (60, 60, 80), "helmet": (210, 190, 120),
                    "helmet_dark": (140, 120, 60)})
