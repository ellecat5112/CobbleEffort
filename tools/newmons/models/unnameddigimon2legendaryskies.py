"""Unnamed Digimon 2 (Legendary Skies) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail
standard after a manga panel on wikimon.net): a stern armoured warrior from the Legendary Skies manga: a tall crested
helm with a visor over a scarred face, great swept spiked pauldrons, a heavy breastplate engraved with a skull,
segmented gauntlets, a long cape of dark cloth and armoured greaves. 25 blocks.

Front is -z, y is up. Perfect stage (by analogy: wikimon gives no level).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import armour, fabric, metal, plane, skin, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a stern armoured warrior with a crested visored helm, great spiked pauldrons, a skull-engraved breastplate and a dark cape"
BASE = {"plate": (120, 124, 140), "plate_dark": (50, 54, 66), "trim": (210, 200, 160), "skin": (220, 190, 160),
        "skin_dark": (170, 130, 100), "cape": (60, 56, 70), "cape_dark": (24, 20, 30), "eye": (240, 220, 120),
        "skull": (220, 216, 200)}
SHINY = {"plate": (150, 110, 70), "plate_dark": (80, 50, 24), "cape": (110, 30, 40), "cape_dark": (60, 10, 16)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "plate", "plate_dark", trim="trim", panel=(3.0, 3.0))


def chestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        if math.hypot(a, b - 46.0) < 2.0 and not any(math.hypot(a - sx * 0.8, b - 46.4) < 0.5 for sx in (-1, 1)):
            return tone(p["skull"], face), None
    return ARM(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("unnameddigimon2legendaryskies")
    mats = {"skin": ARM, "chest": chestf, "abs": ARM, "pelvis": ARM, "deltoid": ARM, "upper_arm": ARM,
            "forearm": ARM, "hand": ARM, "thigh": ARM, "knee": ARM, "shin": ARM, "calf": ARM, "foot": ARM,
            "neck": ARM}
    a = humanoid(m, mats, bulk=1.25, arm_bulk=1.25, leg_bulk=1.2, name="unnameddigimon2legendaryskies")
    bd = a["body"]
    for sx in (-1, 1):                                                                  # swept spiked pauldrons
        m.round_box(bd, sx * 8.0, 0, 4.0, 4.0, 47.0, 54.0, ARM, cut=1)
        for j in range(3):
            spike(m, bd, (sx * (8.0 + j * 1.2), 54.0, -1.0 + j), (sx * 0.8, 0.8, 0), 1.4, 6.0 - j, metal(P, "trim"),
                  tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 3.2, 3.4, 54.0, 61.0, skin(P, "skin", dark="skin_dark"), cut=1)
    m.round_box(hd, 0, 0.6, 3.6, 3.8, 58.6, 62.6, ARM, cut=1)
    m.box(hd, -3.0, 58.0, -4.4, 3.0, 59.4, -3.6, ARM)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 2.0), 57.0, -3.6, max(sx * 0.6, sx * 2.0), 57.8, -3.3, solid(P, "eye"))
    spike(m, hd, (0, 62.4, 0), (0, 1, 0.4), 1.4, 6.0, metal(P, "trim"), tip=0.8)
    cb = m.bone("cape", bd, (0, 53, 4))
    cape(m, cb, 53.0, 15.0, 46.0, fabric(P, "cape", "cape_dark"), z=4.8, flare=0.6, panels=6, seed=9)
    return m
