"""Yaeger Dorulumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Dorulumon risen as a hunter: a hulking silver-armoured wolf beast-man standing upright,
a lion-like orange mane round a steel-masked muzzle with a single horn, spiked shoulder plates, a tattered orange cape,
a huge golden drill lance on its right arm, and clawed armoured feet with a tufted tail. 25 blocks.

Front is -z, y is up. 66 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import armour, fabric, fur, metal, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 8.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a hulking silver-armoured wolf beast-man with an orange lion mane, spiked shoulder plates, a tattered orange cape and a huge golden drill lance"
BASE = {"silver": (210, 214, 226), "silver_dark": (110, 114, 130), "orange": (230, 130, 50), "orange_dark": (160, 70, 20),
        "gold": (240, 200, 70), "gold_dark": (170, 120, 20), "grey": (120, 120, 130), "eye": (250, 220, 60)}
SHINY = {"silver": (70, 70, 84), "silver_dark": (26, 26, 34), "orange": (90, 150, 220), "orange_dark": (40, 80, 160)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "silver", "silver_dark", trim="gold", panel=(3.0, 3.0))


def drillf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (z * 0.8 + math.atan2(x, y) * 1.4) % 2.0 < 0.5:
        return tone(p["gold_dark"], face), None
    return metal(P, "gold")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("yaegerdorulumon")
    mats = {"skin": ARM, "chest": ARM, "abs": metal(P, "grey"), "pelvis": ARM, "deltoid": ARM,
            "upper_arm": fur(P, "orange", "orange_dark"), "forearm": ARM, "hand": ARM, "finger": ARM,
            "claw": metal(P, "silver"), "thigh": ARM, "knee": ARM, "shin": ARM, "calf": ARM, "foot": ARM,
            "talon": metal(P, "silver"), "neck": fur(P, "orange", "orange_dark")}
    a = humanoid(m, mats, bulk=1.4, arm_bulk=1.35, leg_bulk=1.3, digitigrade=True, claws=True, talons=True,
                 name="yaegerdorulumon")
    bd = a["body"]
    for sx in (-1, 1):
        m.round_box(bd, sx * 8.6, 0, 4.4, 4.6, 46.0, 54.0, ARM, cut=2)
        for j in range(3):
            spike(m, bd, (sx * (8.0 + j * 1.6), 54.0, -1.0 + j), (sx * 0.6, 1, 0), 1.6, 6.0 - j, metal(P, "silver"), tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 3.2, 4.0, 54.0, 61.0, ARM, cut=1)
    m.round_box(hd, 0, -5.6, 2.2, 2.0, 54.4, 57.6, metal(P, "silver", dark="silver_dark"), cut=1)
    m.box(hd, -2.4, 58.4, -4.4, 2.4, 59.2, -4.0, solid(P, "eye", glow=True))
    spike(m, hd, (0, 60.6, -2.0), (0, 1, -0.5), 1.4, 6.0, metal(P, "gold"), tip=0.8)
    for j in range(11):                                                                 # orange lion mane
        ang = (j - 5) * 0.32
        spike(m, hd, (math.sin(ang) * 3.4, 57.0 + math.cos(ang) * 2.0, 1.4), (math.sin(ang), 0.4, 0.8), 2.0, 8.0,
              strands(P, "orange", "orange_dark"), tip=0.8)
    cb = m.bone("cape", bd, (0, 52, 4))
    cape(m, cb, 52.0, 16.0, 40.0, fabric(P, "orange", "orange_dark"), z=4.8, flare=0.8, panels=7, seed=14)
    h = a["arm_right"]["hand"]                                                          # golden drill lance
    spike(m, a["arm_right"]["bone"], (h[0], h[1] + 2.0, h[2]), (-0.3, -0.25, -1), 4.0, 26.0, drillf, tip=0.8)
    tl = m.bone("tail", bd, (0, 30, 4))
    rod(m, tl, (0, 30.0, 4.0), (2.0, 20.0, 12.0), 2, ARM, extend=0.5)
    spike(m, tl, (2.0, 20.0, 12.0), (0.2, -0.6, 1), 2.0, 4.0, fur(P, "orange", "orange_dark"), tip=0.8)
    return m
