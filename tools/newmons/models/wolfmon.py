"""Wolfmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the human spirit of light: a lean warrior in silver-white armour with violet trim, a wolf-crested
helm and visor, long violet-and-white checked scarves streaming from its shoulders and back, clawed armoured feet, and
twin sabres of golden light in its hands. 15 blocks.

Front is -z, y is up. 64 units tall; Adult stage (Hybrid).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, fabric, metal, solid
from _route import pal, tone

HEIGHT = 63
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a lean warrior in silver-white armour with a wolf-crested helm, violet checked scarves and twin sabres of golden light"
BASE = {"silver": (220, 224, 236), "silver_dark": (120, 124, 146), "violet": (140, 100, 200), "violet_dark": (70, 40, 130),
        "white": (250, 250, 255), "black": (40, 40, 50), "light": (255, 240, 150, 210), "eye": (120, 220, 255)}
SHINY = {"silver": (60, 60, 76), "silver_dark": (20, 20, 30), "violet": (200, 60, 70), "violet_dark": (120, 20, 30)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "silver", "silver_dark", trim="violet", panel=(3.0, 3.0))


def checkf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    c = p["violet"] if (int(x * 0.8 + 40) + int(y * 0.8) + int(z * 0.8 + 40)) % 2 else p["white"]
    return tone(c, face), None


def build():
    m = Model("wolfmon")
    mats = {"skin": metal(P, "black"), "chest": ARM, "abs": metal(P, "black"), "pelvis": ARM, "deltoid": ARM,
            "upper_arm": metal(P, "black"), "forearm": ARM, "hand": ARM, "thigh": ARM, "knee": ARM, "shin": ARM,
            "calf": ARM, "foot": ARM, "talon": metal(P, "silver"), "neck": metal(P, "black")}
    a = humanoid(m, mats, bulk=1.0, arm_bulk=0.95, leg_bulk=1.0, digitigrade=True, talons=True, name="wolfmon")
    bd = a["body"]
    for sx in (-1, 1):
        m.round_box(bd, sx * 7.0, 0, 3.2, 3.4, 48.0, 53.4, ARM, cut=1)
        for j in range(2):                                                             # checked scarves
            m.box(bd, sx * (6.0 + j * 2.0) - 1.2, 24.0 + j * 4.0, 3.6 + j, sx * (6.0 + j * 2.0) + 1.2, 52.0, 4.2 + j,
                  checkf, rotation=(15 + j * 10, 0, sx * 12), pivot=(sx * 6.0, 52.0, 4.0))
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 3.0, 3.8, 54.0, 61.0, ARM, cut=1)
    m.round_box(hd, 0, -4.6, 1.8, 1.6, 55.0, 58.0, ARM, cut=1)                             # wolf muzzle
    m.box(hd, -2.4, 58.4, -4.2, 2.4, 59.4, -3.8, solid(P, "eye", glow=True))
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.2, 60.6, 0.4), (sx * 0.3, 1, 0.2), 1.6, 4.0, ARM, tip=0.8)
    for nm in ("arm_left", "arm_right"):                                               # light sabres
        h = a[nm]["hand"]
        sx = 1 if nm == "arm_left" else -1
        m.box(a[nm]["bone"], h[0] - 0.5, h[1] - 0.4, h[2] - 18.0, h[0] + 0.5, h[1] + 0.6, h[2] - 1.0,
              solid(P, "light", glow=True), rotation=(25, sx * 30, 0), pivot=h)
    return m
