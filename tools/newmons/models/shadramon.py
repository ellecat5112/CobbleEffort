"""Shadramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Armor Digimon of courage: a fire-insect of red-brown armour flaring into blazing yellow-and-red
flame fins at shoulders, wings and limbs, a pointed insect helm with a pink nose and dark green joints, and flame-tipped
claws. 15 blocks.

Front is -z, y is up. 66 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a fire-insect of red-brown armour flaring into blazing yellow-and-red flame fins, a pointed insect helm and flame-tipped claws"
BASE = {"red": (180, 60, 40), "red_dark": (100, 24, 14), "yellow": (250, 210, 50), "flame": (240, 70, 40),
        "green": (40, 80, 40), "pink": (230, 80, 140), "eye": (30, 30, 30)}
SHINY = {"red": (60, 80, 170), "red_dark": (20, 30, 100), "flame": (90, 180, 250)}


def P(v):
    return pal(BASE, SHINY, v)


def finf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    c = p["yellow"] if (abs(x) + y) % 4.0 < 2.0 else p["flame"]
    return c, c


ARM = armour(P, "red", "red_dark")


def build():
    m = Model("shadramon")
    mats = {"skin": ARM, "neck": solid(P, "green"), "upper_arm": solid(P, "green"), "thigh": solid(P, "green")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.8, leg_bulk=0.8, claws=True, talons=True, name="shadramon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 2.6, 3.4, 54.0, 60.0, ARM, cut=1)
    spike(m, hd, (0, 57.0, -4.0), (0, -0.3, -1), 1.6, 3.0, solid(P, "pink"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.4), 58.0, -4.5, max(sx * 1.0, sx * 2.4), 58.8, -4.3, solid(P, "eye"))
        spike(m, hd, (sx * 1.6, 60.0, -1.0), (sx * 0.6, 1, 0.4), 1.2, 6.0, finf, tip=0.8)
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 3.0, 50.0, 3.0))
        for j in range(4):                                                               # blazing flame-fin wings
            ang = math.radians(-10 + j * 25)
            spike(m, wb, (sx * 3.0, 50.0, 3.0 + j * 0.2), (sx * math.cos(ang), math.sin(ang), 0.4), 3.0, 18.0 - j * 2.0,
                  finf, tip=0.8)
    for side in ("arm_left", "arm_right", "leg_left", "leg_right"):                      # flame fins on the limbs
        key = "elbow" if side.startswith("arm") else "knee"
        p0 = a[side][key]
        sx = 1 if side.endswith("left") else -1
        spike(m, a[side]["bone"], p0, (sx * 0.8, -0.6, 0.4), 2.4, 8.0, finf, tip=0.8)
    return m
