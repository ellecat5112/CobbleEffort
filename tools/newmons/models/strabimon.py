"""Strabimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the warrior of light's fallen half as a child: a lean lavender wolf-boy with white-grey fur
patches, black jagged ears and tail tip, black belts strapped round its arms and legs, black clawed gauntlets with
silver claws, and a pink-clawed foot. 1 block. Child stage.

Front is -z, y is up. 64 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fur, leather, metal, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(1, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a lean lavender wolf-boy with white fur patches, black jagged ears, black belts round its limbs and black clawed gauntlets"
BASE = {"lav": (190, 180, 230), "lav_dark": (130, 120, 180), "white": (240, 240, 246), "white_dark": (180, 180, 196),
        "black": (30, 28, 34), "black_dark": (10, 10, 12), "steel": (210, 214, 226), "pink": (240, 140, 180),
        "eye": (240, 140, 40)}
SHINY = {"lav": (110, 160, 230), "lav_dark": (50, 90, 170)}


def P(v):
    return pal(BASE, SHINY, v)


def furf(x, y, z, face, variant, box=None, **k):
    if math.sin(x * 0.9 + y * 0.4) * math.cos(z * 0.6 + y * 0.3) > 0.4:
        return fur(P, "white", "white_dark", length=1.2)(x, y, z, face, variant, box=box, **k)
    return fur(P, "lav", "lav_dark", length=1.2)(x, y, z, face, variant, box=box, **k)


def beltf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (y % 3.0) < 1.0:
        return tone(p["black"], face), None
    return furf(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("strabimon")
    mats = {"skin": furf, "forearm": beltf, "shin": beltf, "hand": leather(P, "black", "black_dark"),
            "finger": leather(P, "black", "black_dark"), "claw": metal(P, "steel"), "talon": solid(P, "pink")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.85, leg_bulk=0.85, claws=True, talons=True, digitigrade=True,
                 name="strabimon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 2.6, 3.2, 54.0, 60.0, furf, cut=1)
    m.round_box(hd, 0, -4.4, 1.4, 1.4, 54.4, 57.0, furf, cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.0), 57.6, -4.3, max(sx * 0.8, sx * 2.0), 58.4, -4.1, solid(P, "eye"))
        for j in range(3):                                                               # black jagged ears
            spike(m, hd, (sx * 2.0, 60.0 + j, -0.4 + j * 0.6), (sx * 0.5, 1, 0.3), 1.4 - j * 0.2, 5.0 - j, solid(P, "black"),
                  tip=0.8)
    tl = m.bone("tail", bd, (0, 32, 3))
    pts = [(0, 32.0, 3.0), (2.0, 24.0, 10.0), (4.0, 18.0, 14.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 3, furf, extend=0.4)
    spike(m, tl, pts[-1], (0.3, -0.4, 1), 2.0, 4.0, solid(P, "black"), tip=0.8)
    return m
