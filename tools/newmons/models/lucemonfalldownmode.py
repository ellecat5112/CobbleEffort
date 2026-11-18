"""Lucemon: Falldown Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Lucemon fallen: a tall pale man with long blond hair in a black long coat with gold
trim and red-lined sleeves over white trousers and boots, a gold sun emblem on his chest, and wings split down the
middle: three white feathered angel wings on one side and three black bat wings on the other. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing, feather_wing
from _digibody import humanoid
from _digidetail import armour, fabric, feathers, gem, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a tall pale man with long blond hair in a gold-trimmed black coat with white wings on one side and black bat wings on the other"
BASE = {"black": (34, 32, 38), "black_dark": (10, 10, 12), "white": (248, 248, 252), "white_dark": (190, 190, 210),
        "gold": (240, 200, 70), "gold_dark": (160, 120, 20), "red": (190, 30, 40), "skin": (240, 226, 216),
        "skin_dark": (190, 170, 160), "hair": (250, 220, 120), "hair_dark": (200, 160, 60), "eye": (60, 130, 230),
        "membrane": (50, 46, 56)}
SHINY = {"black": (40, 30, 90), "black_dark": (14, 8, 40)}


def P(v):
    return pal(BASE, SHINY, v)


COAT = fabric(P, "black", "black_dark", seam="gold")
WHITE = fabric(P, "white", "white_dark")


def chestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and math.hypot(x, y - 46.0) < 1.8:
        return tone(p["gold"], face), None
    return COAT(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("lucemonfalldownmode")
    mats = {"skin": COAT, "chest": chestf, "abs": COAT, "pelvis": WHITE, "neck": skin(P, "skin", dark="skin_dark"),
            "deltoid": COAT, "upper_arm": COAT, "forearm": fabric(P, "red", "black"), "hand": WHITE, "finger": WHITE,
            "thigh": WHITE, "knee": metal(P, "gold", dark="gold_dark"), "shin": WHITE, "calf": WHITE,
            "foot": WHITE, "toe": WHITE}
    a = humanoid(m, mats, bulk=0.88, arm_bulk=0.9, leg_bulk=0.95, name="lucemonfalldownmode")
    bd = a["body"]
    for sx in (-1, 1):                                                               # coat tails
        rod(m, bd, (sx * 3.0, 34.0, 2.0), (sx * 4.6, 18.0, 5.0), 2, COAT, extend=0.4, t2=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 60.0, skin(P, "skin", dark="skin_dark"), cut=1)
    m.box(hd, -1.4, 57.4, -2.9, -0.4, 58.0, -2.8, solid(P, "eye"))
    m.box(hd, 0.4, 57.4, -2.9, 1.4, 58.0, -2.8, solid(P, "eye"))
    for i in range(11):
        ang = math.radians(-110 + i * 22)
        rod(m, hd, (2.2 * math.sin(ang), 59.6, 0.8 + 1.2 * math.cos(ang)), (3.4 * math.sin(ang), 46.0, 3.6), 1,
            strands(P, "hair", "hair_dark"), extend=0.3, t2=2)
    wl = m.bone("wing_left", bd, (2.6, 48.0, 3.4))                                   # white angel wings
    for j, (dr, sw) in enumerate(((16, 30), (0, 10), (-18, -10))):
        feather_wing(m, wl, (2.6, 48.0, 3.4 + j * 0.4), 24.0 - j * 2, 7.0, 2, feathers(P, "white", "white_dark"), side=1,
                     sweep=sw, droop=dr)
    wr = m.bone("wing_right", bd, (-2.6, 48.0, 3.4))                                 # black bat wings
    for j, sw in enumerate((10, 30, 50)):
        bat_wing(m, wr, (-2.6, 48.0 - j * 4.0, 3.4 + j * 0.4), 22.0 - j * 3, 14.0, 3, solid(P, "black"),
                 solid(P, "membrane"), side=-1, sweep=sw)
    return m
