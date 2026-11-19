"""Tia Ludomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a compact royal-blue armoured knight: a visored helm with a shock of white hair and an ice-blue
crest, chunky shoulder and knee plates, a huge square shield-gauntlet on one arm and an ice-blue energy blade on the
other, and blue-white boots. 15 blocks.

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, metal, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a compact royal-blue armoured knight with white hair, a huge square shield-gauntlet and an ice-blue energy blade"
BASE = {"blue": (60, 70, 190), "blue_dark": (24, 28, 100), "white": (240, 242, 250), "white_dark": (180, 186, 204),
        "ice": (150, 220, 255), "steel": (190, 196, 210), "steel_dark": (90, 96, 110), "eye": (120, 230, 255),
        "black": (30, 30, 40)}
SHINY = {"blue": (180, 60, 70), "blue_dark": (100, 20, 30)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "blue", "blue_dark", trim="white", panel=(3.0, 3.0))
STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("tialudomon")
    mats = {"skin": STEEL, "chest": ARM, "abs": STEEL, "pelvis": ARM, "deltoid": ARM, "upper_arm": STEEL,
            "forearm": ARM, "hand": ARM, "thigh": STEEL, "knee": ARM, "shin": ARM, "calf": ARM,
            "foot": armour(P, "white", "white_dark"), "neck": STEEL}
    a = humanoid(m, mats, bulk=1.2, arm_bulk=1.2, leg_bulk=1.25, name="tialudomon")
    bd = a["body"]
    for sx in (-1, 1):
        m.round_box(bd, sx * 7.2, 0, 3.4, 3.8, 47.6, 53.4, ARM, cut=1)
        spike(m, bd, (sx * 8.0, 53.0, 0), (sx * 0.4, 1, 0), 1.4, 3.0, solid(P, "ice"), tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 3.4, 3.6, 54.0, 61.6, ARM, cut=1)
    m.box(hd, -2.6, 57.0, -4.0, 2.6, 58.4, -3.4, solid(P, "eye", glow=True))
    spike(m, hd, (0, 61.0, -2.4), (0, 1, -0.4), 1.6, 4.0, solid(P, "ice"), tip=0.8)
    for j in range(9):                                                                  # white hair shock
        ang = (j - 4) * 0.4
        spike(m, hd, (math.sin(ang) * 3.0, 60.6, 1.6), (math.sin(ang), 0.7, 0.8), 1.6, 6.0,
              strands(P, "white", "white_dark"), tip=0.8)
    h = a["arm_left"]["hand"]                                                           # square shield-gauntlet
    lb = a["arm_left"]["bone"]
    m.box(lb, h[0] - 5.0, h[1] - 6.0, h[2] - 4.0, h[0] + 6.0, h[1] + 8.0, h[2] - 2.4, ARM)
    m.box(lb, h[0] - 2.4, h[1] - 2.0, h[2] - 4.6, h[0] + 3.4, h[1] + 4.0, h[2] - 4.0, solid(P, "ice", glow=True))
    h = a["arm_right"]["hand"]                                                          # energy blade
    rb = a["arm_right"]["bone"]
    m.box(rb, h[0] - 0.5, h[1] - 1.0, h[2] - 16.0, h[0] + 0.5, h[1] + 1.6, h[2] - 1.0, solid(P, "ice", glow=True),
          rotation=(30, 0, 0), pivot=h)
    return m
