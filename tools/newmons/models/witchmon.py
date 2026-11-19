"""Witchmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a young witch riding a broom: a tall crooked red witch's hat with a gold buckle and a dangling charm,
short blonde hair, a red coat with wide sleeves over a black bodysuit, red gloves with long claws, black buckled boots,
a black cape, and a straw broom carrying her through the air. 15 blocks.

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import fabric, leather, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 73
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a young witch in a tall red hat and red coat with a black cape, red clawed gloves, riding a straw broom"
BASE = {"red": (200, 40, 40), "red_dark": (120, 14, 14), "black": (34, 32, 38), "black_dark": (12, 12, 14),
        "skin": (250, 224, 206), "skin_dark": (210, 176, 160), "hair": (240, 210, 110), "hair_dark": (190, 150, 50),
        "gold": (240, 196, 60), "wood": (140, 90, 50), "straw": (230, 190, 100), "straw_dark": (180, 130, 50),
        "eye": (60, 120, 200)}
SHINY = {"red": (70, 50, 150), "red_dark": (34, 20, 90)}


def P(v):
    return pal(BASE, SHINY, v)


RED = fabric(P, "red", "red_dark")
BLACK = leather(P, "black", "black_dark")


def build():
    m = Model("witchmon")
    mats = {"skin": BLACK, "chest": RED, "abs": BLACK, "pelvis": RED, "deltoid": RED, "upper_arm": RED, "forearm": RED,
            "hand": leather(P, "red", "red_dark"), "finger": leather(P, "red", "red_dark"), "claw": solid(P, "black"),
            "thigh": BLACK, "knee": BLACK, "shin": BLACK, "calf": BLACK, "foot": BLACK,
            "neck": skin(P, "skin", dark="skin_dark")}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.8, leg_bulk=0.85, claws=True, name="witchmon")
    bd = a["body"]
    m.round_box(bd, 0, 0, 5.4, 4.0, 24.0, 34.0, RED, cut=1)                                 # coat skirt
    for nm in ("arm_left", "arm_right"):
        w = a[nm]["wrist"]
        m.box(a[nm]["bone"], w[0] - 2.4, w[1] - 2.0, w[2] - 2.4, w[0] + 2.4, w[1] + 4.0, w[2] + 2.4, RED)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.8, 3.0, 54.0, 61.0, skin(P, "skin", dark="skin_dark"), cut=1)
    m.round_box(hd, 0, 0.8, 3.2, 3.0, 57.6, 61.6, strands(P, "hair", "hair_dark"), cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.8), 58.0, -3.2, max(sx * 0.6, sx * 1.8), 58.8, -3.0, solid(P, "eye"))
    m.round_box(hd, 0, 0, 6.6, 6.6, 61.0, 62.0, RED, cut=3)                                 # hat brim
    for j in range(6):                                                                  # crooked tall hat
        r = 3.4 - j * 0.5
        m.round_box(hd, j * 0.5, j * 0.4, max(r, 0.8), max(r, 0.8), 62.0 + j * 1.8, 63.8 + j * 1.8, RED,
                    cut=1 if r > 1.2 else 0)
    m.box(hd, -3.6, 62.0, -3.7, 3.6, 63.2, -3.4, metal(P, "gold"))
    ball(m, hd, (4.0, 70.0, 2.0), 0.8, metal(P, "gold"), layers=1)
    cb = m.bone("cape", bd, (0, 52, 4))
    cape(m, cb, 52.0, 12.0, 30.0, fabric(P, "black", "black_dark"), z=4.4, flare=0.6, panels=5, seed=2)
    bb = m.bone("broom", top_bone(m), (0, 26, 0))                                       # straw broom between the legs
    rod(m, bb, (0, 27.0, -16.0), (0, 27.0, 14.0), 1, solid(P, "wood"), extend=0.0)
    for j in range(8):
        ang = j * math.pi / 4
        spike(m, bb, (0.8 * math.cos(ang), 27.0 + 0.8 * math.sin(ang), 13.0), (0.3 * math.cos(ang), 0.3 * math.sin(ang), 1),
              1.6, 8.0, fabric(P, "straw", "straw_dark"), tip=0.8)
    return m


def top_bone(m):
    return m.bones[0]["name"]
