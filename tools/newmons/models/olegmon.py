"""Olegmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Viking pirate walrus: a hulking brown-furred brute in heavy gold armour plates and barrel-like
pauldrons, a horned golden helm over a fierce whiskered face with tusks, a thick mane, golden clawed feet, and two
great double-bladed battle axes, one with a black head, one with a red head. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, fur, metal, riveted, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("a hulking brown-furred Viking walrus in heavy gold armour with barrel pauldrons, a horned golden helm, tusks "
        "and two great double-bladed battle axes")
BASE = {"fur": (110, 80, 50), "fur_dark": (60, 40, 20), "gold": (230, 180, 60), "gold_dark": (150, 104, 20),
        "steel": (200, 204, 216), "steel_dark": (90, 94, 108), "black": (40, 38, 50), "red": (180, 30, 40),
        "tusk": (246, 240, 220), "eye": (240, 60, 40)}
SHINY = {"gold": (200, 210, 230), "gold_dark": (110, 120, 140), "fur": (200, 200, 210), "fur_dark": (130, 130, 140)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "fur", "fur_dark", length=1.6)
GOLD = riveted(P, "gold", "gold_dark", spacing=2.4)


def axe(m, bone, c, colour):
    rod(m, bone, (c[0], c[1] - 16.0, c[2]), (c[0], c[1] + 4.0, c[2]), 1, solid(P, "black"), extend=0.2, t2=1)
    for s in (-1, 1):
        x0, x1 = sorted((c[0] + s * 1.0, c[0] + s * 8.0))
        m.box(bone, x0, c[1] - 4.0, c[2] - 0.5, x1, c[1] + 4.0, c[2] + 0.5, metal(P, colour, dark="black"))
        m.box(bone, min(c[0] + s * 8.0, c[0] + s * 8.6), c[1] - 5.0, c[2] - 0.4, max(c[0] + s * 8.0, c[0] + s * 8.6),
              c[1] + 5.0, c[2] + 0.4, metal(P, "steel", dark="steel_dark"))
    spike(m, bone, (c[0], c[1] + 4.0, c[2]), (0, 1, 0), 1.2, 3.0, metal(P, "steel"), tip=0.8)


def build():
    m = Model("olegmon")
    mats = {"skin": FUR, "chest": GOLD, "abs": GOLD, "pelvis": GOLD, "neck": FUR, "deltoid": GOLD, "upper_arm": FUR,
            "forearm": GOLD, "hand": FUR, "finger": FUR, "thigh": FUR, "knee": GOLD, "shin": GOLD, "calf": GOLD,
            "foot": metal(P, "gold"), "toe": metal(P, "gold")}
    a = humanoid(m, mats, bulk=1.4, arm_bulk=1.4, leg_bulk=1.3, hand_pose="fist", name="olegmon")
    bd = a["body"]
    for sx in (-1, 1):                                                                   # barrel pauldrons
        m.round_box(bd, sx * 10.0, 0, 3.6, 3.6, 46.0, 56.0, GOLD, cut=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 3.0, 3.0, 54.0, 60.0, FUR, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.0), 57.4, -3.7, max(sx * 0.8, sx * 2.0), 58.2, -3.5, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 1.2, 55.0, -3.4), (sx * 0.1, -1, -0.2), 1.0, 4.0, solid(P, "tusk"), tip=0.8)   # tusks
        pts = [(sx * 3.0, 60.0, 0), (sx * 6.0, 64.0, 0), (sx * 5.0, 69.0, -1.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):                                 # helm horns
            rod(m, hd, p0, p1, 2 - j, metal(P, "gold"), extend=0.3)
    m.round_box(hd, 0, 0, 3.4, 3.4, 59.0, 61.6, GOLD, cut=1)                              # golden helm
    for i in range(9):                                                                   # thick mane / beard
        ang = math.radians(-90 + i * 22)
        spike(m, hd, (3.0 * math.sin(ang), 55.0, -2.4 * math.cos(ang)), (math.sin(ang) * 0.4, -1, -0.3), 1.6, 4.0, FUR,
              tip=0.8)
    for nm, colour in (("arm_left", "black"), ("arm_right", "red")):                    # two battle axes
        h = a[nm]["hand"]
        axe(m, a[nm]["bone"], (h[0], h[1] - 4.0, h[2] - 3.0), colour)
    return m
