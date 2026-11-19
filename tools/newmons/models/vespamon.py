"""Vespamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a slim cyborg hornet soldier in orange and black striped armour: a visored insect helm with antennae,
translucent wings, a long silver lance blazing with blue energy and a glowing hexagonal energy shield on its other
arm. 25 blocks.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, metal, plane, solid
from _route import pal, tone

HEIGHT = 65
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a slim cyborg hornet soldier in orange and black striped armour with a blue-energy lance and a hexagonal energy shield"
BASE = {"orange": (240, 150, 40), "orange_dark": (170, 90, 10), "black": (36, 32, 30), "steel": (210, 214, 226),
        "steel_dark": (110, 114, 126), "blue": (120, 200, 255, 200), "shield": (150, 210, 255, 160),
        "wing": (220, 240, 255, 140), "eye": (90, 230, 120)}
SHINY = {"orange": (110, 190, 90), "orange_dark": (50, 120, 40)}


def P(v):
    return pal(BASE, SHINY, v)


def stripef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (y % 3.6) < 1.0:
        return tone(p["black"], face), None
    return metal(P, "orange", dark="orange_dark")(x, y, z, face, variant, box=box, **k)


ARM = armour(P, "orange", "orange_dark", trim="black", panel=(3.0, 3.0))


def hexf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    a, b = plane(x, y, z, face)
    if (abs((a * 0.7) % 2.0 - 1.0) < 0.12) or (abs((b * 0.7 + a * 0.35) % 2.0 - 1.0) < 0.12):
        return p["blue"], p["blue"][:3]
    return p["shield"], p["shield"][:3]


def build():
    m = Model("vespamon")
    mats = {"skin": stripef, "chest": ARM, "abs": stripef, "pelvis": ARM, "deltoid": ARM, "upper_arm": stripef,
            "forearm": ARM, "hand": ARM, "thigh": stripef, "knee": ARM, "shin": stripef, "calf": stripef,
            "foot": ARM, "talon": metal(P, "steel"), "neck": stripef}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=0.9, leg_bulk=0.95, talons=True, name="vespamon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.8, 3.2, 54.0, 61.0, ARM, cut=1)
    m.box(hd, -2.4, 57.0, -3.7, 2.4, 58.4, -3.2, solid(P, "eye", glow=True))
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.2, 61.0, -1.0), (sx * 0.2, 1, 0.2), 0.8, 6.0, solid(P, "black"), tip=0.8)
        x0, x1 = sorted((sx * 2.0, sx * 14.0))
        m.box(bd, x0, 40.0, 4.0, x1, 52.0, 4.2, solid(P, "wing"), rotation=(0, 0, sx * 15), pivot=(sx * 2.0, 50.0, 4.1))
    h = a["arm_right"]["hand"]                                                          # lance, held across
    rb = a["arm_right"]["bone"]
    rod(m, rb, (h[0] + 8.0, h[1] + 3.0, h[2]), (h[0] - 10.0, h[1] - 3.0, h[2]), 1, metal(P, "steel", dark="steel_dark"),
        extend=0.0)
    spike(m, rb, (h[0] - 10.0, h[1] - 3.0, h[2]), (-1, -0.33, 0), 2.0, 16.0, solid(P, "blue", glow=True), tip=0.8)
    h = a["arm_left"]["hand"]                                                           # hex energy shield
    m.box(a["arm_left"]["bone"], h[0] - 5.0, h[1] - 4.0, h[2] - 4.0, h[0] + 5.0, h[1] + 12.0, h[2] - 3.6, hexf)
    return m
