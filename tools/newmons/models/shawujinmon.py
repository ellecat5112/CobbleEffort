"""Shawujinmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the river monk of the journey west: a lean green-scaled kappa-like warrior in a white tunic and
green scale-mail leggings, blue hair tied back, a golden beaked mask over its face and a necklace of golden skulls, a
billowing red cape and blue sash, silver gauntlets, and a crescent-bladed staff with a revolver drum. 25 blocks.

Front is -z, y is up. 66 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import fabric, metal, scales, solid, strands
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a lean green-scaled river monk in a white tunic with a golden beaked mask, a golden skull necklace, a red cape and a crescent staff"
BASE = {"green": (80, 150, 70), "green_dark": (30, 80, 24), "white": (244, 244, 236), "white_dark": (190, 190, 176),
        "blue": (40, 70, 170), "blue_dark": (14, 30, 100), "red": (200, 30, 40), "red_dark": (110, 10, 16),
        "gold": (240, 200, 70), "gold_dark": (160, 120, 20), "steel": (200, 204, 216), "steel_dark": (100, 104, 120),
        "claw": (240, 220, 80)}
SHINY = {"green": (70, 90, 170), "green_dark": (24, 34, 100), "red": (60, 60, 70), "red_dark": (20, 20, 26)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = metal(P, "gold", dark="gold_dark")
STEEL = metal(P, "steel", dark="steel_dark")


def capef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["red_dark"] if face == "north" else p["red"], face), None


def build():
    m = Model("shawujinmon")
    mats = {"skin": fabric(P, "white", "white_dark", axis="y"), "neck": scales(P, "green", "green_dark"),
            "thigh": scales(P, "green", "green_dark"), "shin": scales(P, "green", "green_dark"), "forearm": STEEL,
            "hand": scales(P, "green", "green_dark"), "finger": solid(P, "claw"), "talon": solid(P, "claw")}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.9, talons=True, name="shawujinmon")
    bd = a["body"]
    cape(m, bd, 52.0, 14.0, 40.0, capef, z=4.0, flare=2.4, panels=6, seed=7, sweep=(15.0, 10.0))
    m.round_box(bd, 0, 0, 5.0, 3.8, 31.0, 33.0, solid(P, "blue"), cut=1)                    # blue sash
    rod(m, bd, (-3.0, 32.0, -3.0), (-6.0, 22.0, -2.0), 1, solid(P, "blue"), extend=0.2, t2=3)
    for j in range(9):                                                                   # golden skull necklace
        ang = math.pi * (0.1 + 0.8 * j / 8)
        ball(m, bd, (4.4 * math.cos(ang), 50.0 - 2.6 * math.sin(ang), -3.6 * math.sin(ang)), 0.8, GOLD, layers=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.6, 54.0, 60.0, scales(P, "green", "green_dark"), cut=1)
    m.round_box(hd, 0, -2.6, 2.4, 0.8, 55.0, 59.0, GOLD, cut=0)                              # golden beaked mask
    spike(m, hd, (0, 56.0, -3.4), (0, -0.4, -1), 1.4, 2.4, GOLD, tip=0.8)
    for j in range(5):                                                                   # blue hair tied back
        rod(m, hd, (0, 60.0, 0.6), ((j - 2) * 0.8, 58.0 - j, 6.0 + j), 1, strands(P, "blue", "blue_dark"), extend=0.2, t2=2)
    w = a["arm_right"]["wrist"]                                                          # crescent staff + drum
    ab = a["arm_right"]["bone"]
    rod(m, ab, (w[0] - 6.0, w[1] - 10.0, w[2]), (w[0] + 8.0, w[1] + 26.0, w[2]), 1, STEEL, extend=0.2)
    top_ = (w[0] + 8.0, w[1] + 26.0, w[2])
    for j in range(5):                                                                   # crescent blade
        ang = math.radians(30 + j * 30)
        p0 = (top_[0] + 4.0 * math.cos(ang), top_[1] + 4.0 * math.sin(ang), top_[2])
        m.box(ab, p0[0] - 0.8, p0[1] - 0.8, p0[2] - 0.4, p0[0] + 0.8, p0[1] + 0.8, p0[2] + 0.4, STEEL)
    rod(m, ab, (w[0] - 6.0, w[1] - 10.0, w[2] - 2.0), (w[0] - 6.0, w[1] - 10.0, w[2] + 3.0), 4, STEEL, extend=0.2)
    return m
