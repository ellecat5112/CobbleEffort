"""Zamielmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the demon huntsman: a lean figure in olive-green segmented armour with gold-studded boots, a pointed
green hood over a hidden face, two round green shoulder pods bristling with red-fletched arrows, a long white tasset,
claws, a bow-arm and a whip of a tail, and a great arrow with a checkered tip rising over its head. 25 blocks.

Front is -z, y is up. 66 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, fabric, metal, solid
from _route import pal, tone

HEIGHT = 79
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a lean demon huntsman in olive-green segmented armour with a pointed hood, shoulder pods bristling with red-fletched arrows and a great arrow"
BASE = {"green": (90, 120, 50), "green_dark": (40, 60, 20), "gold": (240, 200, 70), "white": (240, 236, 220),
        "white_dark": (190, 184, 160), "red": (200, 40, 40), "steel": (200, 204, 216), "black": (30, 30, 34),
        "eye": (250, 220, 60)}
SHINY = {"green": (110, 60, 140), "green_dark": (50, 20, 80)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "green", "green_dark", trim="gold", panel=(2.4, 2.4))


def arrow(m, bone, base_pt, d, L):
    rod(m, bone, base_pt, tuple(base_pt[i] + d[i] * L for i in range(3)), 1, solid(P, "black"), extend=0.0)
    tip = tuple(base_pt[i] + d[i] * L for i in range(3))
    spike(m, bone, tip, d, 1.0, 2.0, metal(P, "steel"), tip=0.8)
    m.box(bone, base_pt[0] - 0.8, base_pt[1] - 0.8, base_pt[2] - 0.1, base_pt[0] + 0.8, base_pt[1] + 0.8, base_pt[2] + 0.1,
          solid(P, "red"))


def build():
    m = Model("zamielmon")
    mats = {"skin": ARM, "chest": ARM, "abs": ARM, "pelvis": ARM, "deltoid": ARM, "upper_arm": ARM, "forearm": ARM,
            "hand": metal(P, "steel"), "finger": metal(P, "steel"), "claw": metal(P, "steel"), "thigh": ARM,
            "knee": ARM, "shin": ARM, "calf": ARM, "foot": metal(P, "gold"), "neck": ARM}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=0.9, leg_bulk=0.95, claws=True, name="zamielmon")
    bd = a["body"]
    m.box(bd, -2.4, 12.0, -4.6, 2.4, 31.0, -3.8, fabric(P, "white", "white_dark"))          # white tasset
    for sx in (-1, 1):                                                                  # shoulder pods with arrows
        ball(m, bd, (sx * 8.0, 50.0, 0), 4.0, ARM, layers=3)
        for j in range(3):
            d = (sx * 0.4, 1, -0.2 + j * 0.2)
            n = math.sqrt(sum(v * v for v in d))
            arrow(m, bd, (sx * 8.0, 50.0, 0), tuple(v / n for v in d), 12.0 + j * 2.0)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 3.0, 3.2, 54.0, 61.0, ARM, cut=1)
    m.box(hd, -2.2, 56.0, -3.4, 2.2, 59.0, -3.0, solid(P, "black"))
    for sx in (-1, 1):
        m.box(hd, sx * 1.0 - 0.4, 57.4, -3.5, sx * 1.0 + 0.4, 58.0, -3.3, solid(P, "eye", glow=True))
    spike(m, hd, (0, 60.6, 0.4), (0.2, 1, 0.4), 2.4, 7.0, ARM, tip=0.8)                    # pointed hood
    arrow(m, hd, (0, 62.0, -1.0), (0, 1, 0), 16.0)                                         # great arrow
    tl = m.bone("tail", bd, (0, 30, 4))
    pts = [(0, 30.0, 4.0), (-4.0, 20.0, 8.0), (-10.0, 16.0, 8.0), (-14.0, 20.0, 6.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, ARM, extend=0.3)
    return m
