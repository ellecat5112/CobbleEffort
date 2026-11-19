"""Tengumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a tengu mountain-hermit warrior: a long-nosed red tengu mask under wild violet hair, great dark
blue-and-black crow wings, a muscular green-skinned body covered by a dark armoured vest, a fur collar, rope prayer
beads, a huge black war-fan painted with gold seals in one hand, and a single tall geta clog. 35 blocks.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing
from _digibody import humanoid
from _digidetail import armour, fabric, feathers, fur, plane, skin, solid, strands
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 8.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a tengu warrior with a long-nosed red mask, wild violet hair, great dark crow wings, a dark armoured vest and a huge black war-fan"
BASE = {"green": (80, 130, 90), "green_dark": (40, 80, 50), "armour": (60, 70, 90), "armour_dark": (24, 28, 40),
        "red": (210, 40, 40), "red_dark": (130, 14, 14), "violet": (180, 150, 210), "violet_dark": (110, 80, 150),
        "wing": (50, 70, 130), "wing_dark": (16, 20, 40), "fur": (200, 200, 210), "fur_dark": (130, 130, 140),
        "black": (30, 28, 34), "gold": (230, 180, 60), "wood": (150, 110, 60), "bead": (240, 140, 170),
        "eye": (250, 230, 120)}
SHINY = {"wing": (190, 60, 50), "wing_dark": (90, 20, 14)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "armour", "armour_dark", trim="gold", panel=(3.0, 3.0))
GREEN = skin(P, "green", dark="green_dark")


def fanf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "south") and box is not None:
        cx = box.lo[0] + box.size[0] / 2
        cy = box.lo[1] + box.size[1] / 2
        for dx in (-3.0, 3.0):
            d = math.hypot(x - cx - dx, y - cy)
            if d < 2.4:
                return (p["gold"] if d > 1.2 else p["black"]), None
    return tone(p["black"], face), None


def build():
    m = Model("tengumon")
    mats = {"skin": GREEN, "chest": ARM, "abs": ARM, "pelvis": fabric(P, "armour", "armour_dark"),
            "deltoid": ARM, "upper_arm": GREEN, "forearm": ARM, "hand": GREEN, "thigh": fabric(P, "armour",
            "armour_dark"), "knee": ARM, "shin": ARM, "foot": solid(P, "wood"), "neck": GREEN}
    a = humanoid(m, mats, bulk=1.2, arm_bulk=1.25, leg_bulk=1.1, name="tengumon")
    bd = a["body"]
    m.round_box(bd, 0, 0.4, 6.4, 4.8, 49.0, 53.0, fur(P, "fur", "fur_dark"), cut=2)         # fur collar
    for j in range(12):                                                                 # prayer beads
        ang = j / 11 * math.pi
        ball(m, bd, (5.4 * math.cos(ang), 44.0 - 5.0 * math.sin(ang), -4.8), 0.7, solid(P, "bead"), layers=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                                # tall geta teeth
        ank = a[nm]["ankle"]
        m.box(a[nm]["bone"], ank[0] - 1.0, -0.0, ank[2] - 1.0, ank[0] + 1.0, 0.6, ank[2] + 1.0, solid(P, "wood"))
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 3.2, 3.4, 54.0, 61.0, skin(P, "red", dark="red_dark"), cut=1)  # tengu mask
    rod(m, hd, (0, 57.6, -3.0), (0, 58.0, -10.0), 2, skin(P, "red", dark="red_dark"), extend=0.0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 2.0), 58.8, -3.9, max(sx * 0.6, sx * 2.0), 59.6, -3.5, solid(P, "eye", glow=True))
    for j in range(9):                                                                  # wild hair
        ang = (j - 4) * 0.35
        spike(m, hd, (math.sin(ang) * 2.6, 60.0, 1.0), (math.sin(ang) * 1.2, 0.8, 0.8), 2.0, 9.0,
              strands(P, "violet", "violet_dark"), tip=0.8)
    for sx in (-1, 1):                                                                  # crow wings
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 3.0, 48.0, 4.0))
        feather_wing(m, wb, (sx * 3.0, 48.0, 4.0), 30.0, 16.0, 3, feathers(P, "wing", "wing_dark"), side=sx,
                     sweep=25, droop=-6.0)
    h = a["arm_left"]["hand"]                                                           # war-fan
    lb = a["arm_left"]["bone"]
    rod(m, lb, h, (h[0] + 2.0, h[1] - 6.0, h[2]), 1, solid(P, "wood"), extend=0.5)
    m.box(lb, h[0] - 7.0, h[1] - 18.0, h[2] - 0.5, h[0] + 9.0, h[1] - 6.0, h[2] + 0.5, fanf)
    return m
