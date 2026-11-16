"""Shared palette for the Arkadimon line (CobbleEffort: Digital; hand-built after the official art on wikimon.net):
the bewitching beast that grows by eating data. Grey baby, pink child, peach-skinned adult with exposed muscle lines,
then mint-green armour with dark crimson tentacle masses, and a final dark steel form.

Shiny: violet hides and teal tentacles."""
from __future__ import annotations

from _digidetail import armour, metal, skin, solid
from _route import pal

BASE = {"grey": (200, 200, 206), "grey_dark": (120, 120, 130), "grey_light": (246, 246, 250), "red": (220, 30, 40),
        "pink": (240, 170, 190), "pink_dark": (190, 110, 140), "pink_light": (255, 220, 230), "crimson": (130, 24, 40),
        "crimson_dark": (70, 10, 20), "crimson_light": (200, 80, 90), "peach": (240, 196, 160), "peach_dark": (190, 130, 100),
        "peach_light": (255, 230, 210), "muscle": (200, 80, 70), "mint": (190, 220, 200), "mint_dark": (110, 140, 120),
        "mint_light": (236, 250, 240), "steel": (90, 96, 110), "steel_dark": (40, 44, 54), "steel_light": (160, 168, 186),
        "nail": (30, 26, 30), "claw": (170, 40, 60), "hair": (30, 24, 28), "hair_light": (80, 70, 80),
        "eye": (255, 220, 60), "pupil": (20, 16, 10), "wing": (150, 120, 190, 220), "wing_dark": (90, 60, 130, 230), "white": (250, 250, 250)}
SHINY = {"grey": (160, 150, 200), "grey_dark": (90, 80, 140), "pink": (190, 160, 240), "pink_dark": (130, 100, 190),
         "crimson": (20, 120, 130), "crimson_dark": (10, 60, 70), "crimson_light": (80, 200, 200), "peach": (200, 190, 240),
         "peach_dark": (140, 130, 190), "mint": (200, 180, 230), "mint_dark": (130, 110, 170), "claw": (20, 140, 150),
         "muscle": (60, 150, 170), "steel": (110, 80, 140), "steel_dark": (50, 30, 70), "steel_light": (180, 150, 210),
         "hair": (230, 226, 236), "hair_light": (255, 255, 255)}


def P(v):
    return pal(BASE, SHINY, v)


GREY = metal(P, "grey", dark="grey_dark", light="grey_light")
PINK = skin(P, "pink", dark="pink_dark", light="pink_light", var=0.03)
CRIMSON = skin(P, "crimson", dark="crimson_dark", light="crimson_light", var=0.04)
MINT = armour(P, "mint", "mint_dark", light="mint_light")
STEEL = armour(P, "steel", "steel_dark", light="steel_light")
CLAW = metal(P, "claw", dark="crimson_dark", streak=2.0)
