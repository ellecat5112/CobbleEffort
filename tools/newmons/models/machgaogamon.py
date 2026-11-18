"""Mach Gaogamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the boxing wolf cyborg: a blue wolf-man with a white muzzle and chest fur and a visor, a red-and-
silver championship chest plate, white baggy trousers with black boots and silver greaves, a huge silver rocket-
booster gauntlet with red knuckles on one arm, a smaller silver gauntlet on the other, and a long blue belt-strap
tail. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, fabric, fur, leather, metal, skin, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a blue boxing wolf-man with a visor, a red-and-silver chest plate, white baggy trousers, black boots and a huge silver rocket gauntlet"
BASE = {"blue": (60, 90, 190), "blue_dark": (24, 40, 110), "white": (246, 244, 236), "white_dark": (190, 186, 170),
        "red": (210, 40, 40), "red_dark": (120, 14, 18), "silver": (210, 214, 226), "silver_dark": (100, 104, 120),
        "black": (34, 32, 36), "black_dark": (10, 10, 12), "eye": (250, 210, 60), "visor": (180, 220, 250)}
SHINY = {"blue": (80, 80, 90), "blue_dark": (30, 30, 36)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "blue", "blue_dark", tip="white", length=1.0)
SIL = metal(P, "silver", dark="silver_dark")
PANTS = fabric(P, "white", "white_dark", period=1.6)


def chestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 4.6 and 43.0 < y < 50.0:
        if math.hypot(x, y - 46.5) < 2.0:
            return tone(p["silver"], face), None
        return tone(p["red"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("machgaogamon")
    mats = {"skin": FUR, "chest": chestf, "abs": fur(P, "white", "white_dark"), "pelvis": PANTS, "neck": FUR,
            "deltoid": FUR, "upper_arm": FUR, "forearm": SIL, "hand": SIL, "finger": SIL, "thigh": PANTS, "knee": SIL,
            "shin": SIL, "calf": leather(P, "black", "black_dark"), "foot": leather(P, "black", "black_dark"),
            "toe": solid(P, "red")}
    a = humanoid(m, mats, bulk=1.05, arm_bulk=1.1, leg_bulk=1.1, name="machgaogamon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, -1))
    m.round_box(hd, 0, -1.0, 3.0, 3.4, 53.6, 60.4, FUR, cut=1)
    m.round_box(hd, 0, -5.2, 1.8, 2.0, 53.8, 57.0, fur(P, "white", "white_dark"), cut=1)
    m.round_box(hd, 0, -4.1, 2.8, 0.4, 57.4, 58.6, solid(P, "visor"), cut=0)
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 59.6, 0.4), (sx * 0.4, 1, 0.3), 1.6, 4.0, FUR, tip=0.8)
    hr = a["arm_right"]                                                              # huge rocket gauntlet
    hx, hy, hz = hr["hand"]
    m.round_box(hr["bone"], hx - 1.0, hz - 1.0, 4.4, 4.4, hy - 6.0, hy + 2.0, SIL, cut=2)
    for j in range(4):
        m.round_box(hr["bone"], hx - 3.0 + j * 1.4, hz - 5.6, 0.6, 0.4, hy - 4.0, hy - 2.6, solid(P, "red"), cut=0)
    rod(m, hr["bone"], (hx - 1.0, hy + 2.0, hz + 1.0), (hx - 1.0, hy + 12.0, hz + 4.0), 3, SIL, extend=0.6)
    tb = m.bone("tail", bd, (0, 32, 3))                                              # belt-strap tail
    pts = [(0, 32.0, 3.4), (2.0, 22.0, 9.0), (4.0, 12.0, 10.0), (6.0, 6.0, 8.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 1, leather(P, "blue", "blue_dark", stitch="silver"), extend=0.3, t2=3)
    return m
