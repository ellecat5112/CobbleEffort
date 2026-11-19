"""Wolvermon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a cyborg wolverine brawler: a grey-and-white shaggy beast-man with a black mask band over its
eyes, a white fur chest with a gold star badge, a red studded belt and baggy grey trousers, big red mechanical
gauntlets with long red claws and spinning drum knuckles, red boots, and black cable whips streaming from its back. 15
blocks.

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, fabric, fur, leather, metal, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a grey-and-white wolverine brawler with a black mask, a gold star badge, big red mechanical clawed gauntlets and cable whips"
BASE = {"grey": (130, 130, 140), "grey_dark": (70, 70, 80), "white": (246, 246, 250), "white_dark": (190, 190, 200),
        "black": (30, 30, 34), "red": (200, 30, 60), "red_dark": (120, 10, 30), "gold": (250, 210, 60),
        "steel": (190, 194, 206), "steel_dark": (90, 94, 106), "eye": (250, 80, 80)}
SHINY = {"grey": (150, 110, 70), "grey_dark": (90, 60, 30), "red": (60, 120, 200), "red_dark": (20, 60, 130)}


def P(v):
    return pal(BASE, SHINY, v)


GREY = fur(P, "grey", "grey_dark", length=1.2)
REDA = armour(P, "red", "red_dark", trim="steel", panel=(2.4, 2.4))


def chestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if math.hypot(x - 2.0, y - 46.0) < 1.2:
            return tone(p["gold"], face), None
        if abs(x) < 4.0:
            return fur(P, "white", "white_dark")(x, y, z, face, variant, box=box, **k)
    return GREY(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("wolvermon")
    PANTS = fabric(P, "grey", "grey_dark")
    mats = {"skin": GREY, "chest": chestf, "abs": chestf, "pelvis": PANTS, "deltoid": GREY, "upper_arm": GREY,
            "forearm": REDA, "hand": REDA, "finger": REDA, "claw": solid(P, "red"), "thigh": PANTS, "knee": PANTS,
            "shin": leather(P, "red", "red_dark"), "calf": leather(P, "red", "red_dark"),
            "foot": leather(P, "red", "red_dark"), "neck": fur(P, "white", "white_dark")}
    a = humanoid(m, mats, bulk=1.15, arm_bulk=1.2, leg_bulk=1.1, claws=True, name="wolvermon")
    bd = a["body"]
    m.round_box(bd, 0, 0, 5.6, 4.2, 30.0, 32.4, leather(P, "red", "red_dark"), cut=1)
    for nm in ("leg_left", "leg_right"):
        k = a[nm]["knee"]
        m.round_box(a[nm]["bone"], k[0], k[2], 3.2, 3.2, 10.0, 24.0, PANTS, cut=1)
    for nm in ("arm_left", "arm_right"):                                               # gauntlets + drum knuckles
        h = a[nm]["hand"]
        sx = 1 if nm == "arm_left" else -1
        m.round_box(a[nm]["bone"], h[0], h[2], 3.0, 3.0, h[1] - 1.0, h[1] + 6.0, REDA, cut=1)
        m.round_box(a[nm]["bone"], h[0] + sx * 3.0, h[2], 1.0, 2.0, h[1] + 1.0, h[1] + 4.0, metal(P, "steel"), cut=0)
        for f in range(3):
            spike(m, a[nm]["bone"], (h[0] + (f - 1) * 1.4, h[1] - 1.0, h[2] - 2.0), (0, -0.6, -1), 1.0, 5.0,
                  solid(P, "red"), tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.8, 3.2, 3.8, 54.0, 61.0, GREY, cut=1)
    m.round_box(hd, 0, -4.8, 1.8, 1.6, 54.4, 57.4, fur(P, "white", "white_dark"), cut=1)
    m.box(hd, -3.3, 58.0, -4.6, 3.3, 59.6, -4.0, solid(P, "black"))
    for sx in (-1, 1):
        m.box(hd, sx * 1.4 - 0.5, 58.6, -4.8, sx * 1.4 + 0.5, 59.2, -4.6, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.6, 60.4, 0.4), (sx * 0.4, 1, 0.2), 1.6, 3.4, GREY, tip=0.8)
    for j in range(7):                                                                 # shaggy grey mane
        ang = (j - 3) * 0.45
        spike(m, hd, (math.sin(ang) * 3.0, 59.4, 2.0), (math.sin(ang), 0.3, 1), 1.6, 7.0, GREY, tip=0.8)
    wb = m.bone("cables", bd, (0, 50, 4))                                               # cable whips
    for i in range(3):
        pts = [(0, 50.0, 4.0), (4.0 + i * 2.0, 58.0 + i * 2.0, 8.0), (10.0 + i * 3.0, 62.0 + i, 6.0),
               (16.0 + i * 2.0, 56.0 + i * 2.0, 4.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, wb, p0, p1, 1, solid(P, "black"), extend=0.2)
    return m
