"""Titamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a giant oni war-god: green-skinned and heavily muscled, clad in dark green armour edged in red
with skull ornaments on its belt and knees, a horned skull-faced helm trailing white hair and black cables, and an
enormous jagged bone-and-gold sword trailing dark smoke. 35 blocks.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a giant green oni war-god in dark green armour with skull ornaments, a horned skull helm and an enormous jagged bone sword"
BASE = {"green": (90, 150, 80), "green_dark": (40, 90, 40), "armour": (50, 80, 50), "armour_dark": (20, 40, 22),
        "red": (190, 40, 40), "bone": (236, 226, 200), "bone_dark": (170, 156, 120), "gold": (220, 170, 60),
        "gold_dark": (140, 96, 30), "white": (240, 240, 244), "white_dark": (190, 190, 200), "black": (30, 30, 34),
        "eye": (255, 60, 40), "smoke": (90, 90, 100, 150)}
SHINY = {"green": (170, 90, 160), "green_dark": (100, 40, 100), "armour": (60, 50, 90), "armour_dark": (26, 20, 46)}


def P(v):
    return pal(BASE, SHINY, v)


GREEN = skin(P, "green", dark="green_dark")
ARM = armour(P, "armour", "armour_dark", trim="red", panel=(3.0, 3.0))
BONE = skin(P, "bone", dark="bone_dark")


def skull(m, bone, c, r):
    x, y, z = c
    m.round_box(bone, x, z, r, r, y - r, y + r * 0.9, BONE, cut=0)
    for sx in (-1, 1):
        m.box(bone, x + sx * r * 0.45 - 0.5, y, z - r - 0.1, x + sx * r * 0.45 + 0.5, y + 0.9, z - r + 0.2, solid(P, "black"))


def build():
    m = Model("titamon")
    mats = {"skin": GREEN, "chest": ARM, "abs": GREEN, "pelvis": ARM, "deltoid": ARM, "upper_arm": GREEN,
            "forearm": ARM, "hand": GREEN, "thigh": ARM, "knee": ARM, "shin": ARM, "calf": ARM, "foot": ARM,
            "talon": BONE, "neck": GREEN}
    a = humanoid(m, mats, bulk=1.4, arm_bulk=1.4, leg_bulk=1.25, talons=True, name="titamon")
    bd = a["body"]
    m.round_box(bd, 0, 0, 6.6, 5.0, 29.6, 32.4, metal(P, "gold", dark="gold_dark"), cut=1)
    skull(m, bd, (0, 31.0, -5.6), 1.8)
    for nm in ("leg_left", "leg_right"):
        k = a[nm]["knee"]
        skull(m, a[nm]["bone"], (k[0], k[1], k[2] - 3.4), 1.6)
    for sx in (-1, 1):
        m.round_box(bd, sx * 8.4, 0, 4.0, 4.4, 47.0, 54.0, ARM, cut=1)
        for j in range(3):
            spike(m, bd, (sx * (7.0 + j * 1.6), 53.6, 0), (sx * 0.4, 1, 0), 1.2, 4.0 + j, BONE, tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 3.4, 3.6, 54.0, 62.0, ARM, cut=1)
    m.round_box(hd, 0, -2.6, 2.6, 1.4, 54.4, 60.0, BONE, cut=1)                          # skull face
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 2.0), 57.6, -4.1, max(sx * 0.6, sx * 2.0), 58.6, -3.9, solid(P, "eye", glow=True))
        pts = [(sx * 3.0, 61.0, 0), (sx * 6.0, 64.0, 0.6), (sx * 7.0, 68.0, 1.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, BONE, extend=0.4)
    for j in range(7):
        ang = (j - 3) * 0.4
        spike(m, hd, (math.sin(ang) * 3.0, 60.0, 2.4), (math.sin(ang) * 0.6, -0.4, 1), 1.6, 9.0,
              strands(P, "white", "white_dark"), tip=0.8)
    h = a["arm_right"]["hand"]                                                          # giant bone sword
    rb = a["arm_right"]["bone"]
    m.box(rb, h[0] - 0.8, h[1] - 0.8, h[2] - 4.0, h[0] + 0.8, h[1] + 0.8, h[2] + 4.0, metal(P, "gold", dark="gold_dark"))
    for j in range(6):
        z0 = h[2] - 4.0 - j * 5.0
        m.box(rb, h[0] - 0.8, h[1] - 3.0 - j * 0.2, z0 - 5.2, h[0] + 0.8, h[1] + 2.0, z0, BONE)
        spike(m, rb, (h[0], h[1] + 2.0, z0 - 2.6), (0, 1, -0.3), 1.0, 2.4, BONE, tip=0.8)
    for j in range(4):
        ball(m, rb, (h[0], h[1] + 2.0 + j, h[2] - 32.0 - j * 2.0), 2.4, solid(P, "smoke"), layers=1)
    return m
