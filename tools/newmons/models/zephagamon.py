"""Zephagamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the magic knight of the gale: a slim knight in teal-green and silver armour with red trim, a tall
crested dragon helm with a visor, a towering white-and-red shoulder-wing mantle, two vast wings of layered teal
blade-feathers sweeping out wide and down, and arcs of green wind blowing round it. 35 blocks.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digibody import humanoid
from _digidetail import armour, feathers, metal, solid
from _route import pal, tone

HEIGHT = 65
SCALE, HITBOX = sized(35, HEIGHT, 10.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a slim knight in teal-green and silver armour with a crested dragon helm and two vast wings of layered teal blade-feathers"
BASE = {"teal": (60, 160, 160), "teal_dark": (20, 90, 100), "silver": (220, 224, 236), "silver_dark": (120, 124, 140),
        "red": (200, 40, 50), "white": (240, 242, 248), "white_dark": (180, 186, 204), "wind": (140, 255, 190, 150),
        "eye": (120, 255, 200)}
SHINY = {"teal": (190, 90, 150), "teal_dark": (110, 30, 80), "wind": (255, 170, 220, 150)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "teal", "teal_dark", trim="red", panel=(3.0, 3.0))
SILVER = armour(P, "silver", "silver_dark", trim="red", panel=(2.4, 2.4))


def build():
    m = Model("zephagamon")
    mats = {"skin": SILVER, "chest": ARM, "abs": SILVER, "pelvis": ARM, "deltoid": ARM, "upper_arm": SILVER,
            "forearm": ARM, "hand": SILVER, "thigh": ARM, "knee": SILVER, "shin": ARM, "calf": ARM, "foot": ARM,
            "talon": metal(P, "silver"), "neck": SILVER}
    a = humanoid(m, mats, bulk=1.0, arm_bulk=0.95, leg_bulk=1.0, digitigrade=True, talons=True, name="zephagamon")
    bd = a["body"]
    for sx in (-1, 1):                                                                  # tall shoulder-wing mantle
        for j in range(3):
            spike(m, bd, (sx * 6.0, 52.0, 2.0 + j), (sx * 0.2, 1, 0.1), 2.4, 16.0 - j * 3.0,
                  armour(P, "white", "white_dark", trim="red"), tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.8, 3.0, 3.8, 54.0, 61.0, ARM, cut=1)
    m.box(hd, -2.4, 57.6, -4.4, 2.4, 58.6, -4.0, solid(P, "eye", glow=True))
    spike(m, hd, (0, 61.0, -2.0), (0, 1, 0.3), 1.4, 7.0, SILVER, tip=0.8)
    for sx in (-1, 1):
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 3.0, 46.0, 4.0))
        feather_wing(m, wb, (sx * 3.0, 46.0, 4.0), 34.0, 18.0, 4, feathers(P, "teal", "teal_dark"), side=sx, sweep=10,
                     droop=10.0)
    wd = m.bone("wind", bd, (0, 30, 0))
    for sx in (-1, 1):
        for i in range(10):
            ang = math.pi * (0.1 + i / 12)
            cx, cy = sx * (16.0 + 10.0 * math.sin(ang)), 20.0 + 14.0 * math.cos(ang)
            m.box(wd, cx - 1.2, cy - 1.2, -2.0, cx + 1.2, cy + 1.2, -1.0, solid(P, "wind", glow=True))
    return m
