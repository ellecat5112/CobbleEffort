"""Pile Volcamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the volcanic champion: a hulking cyborg brawler in black-and-red armour with a heavy riveted
helmet and visor, a white scarf, a gold champion's belt, enormous steel pile-driver fists, and volcanic smoke and
sparks bursting from the vents on its shoulders. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, fabric, metal, riveted, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("a hulking cyborg brawler in black-and-red armour with a riveted helmet, a white scarf, a gold champion's belt, "
        "enormous pile-driver fists and volcanic smoke bursting from its shoulders")
BASE = {"black": (40, 40, 46), "black_dark": (12, 12, 16), "red": (210, 40, 30), "steel": (200, 204, 214),
        "steel_dark": (100, 104, 116), "gold": (240, 200, 60), "gold_dark": (160, 120, 20), "white": (240, 240, 236),
        "white_dark": (180, 180, 176), "smoke": (130, 130, 136, 170), "spark": (255, 190, 60), "visor": (240, 60, 40)}
SHINY = {"black": (200, 200, 210), "black_dark": (120, 120, 130), "red": (60, 120, 230)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "black", "black_dark", trim="red", trim_w=0.3)
STEEL = riveted(P, "steel", "steel_dark", spacing=2.0)


def build():
    m = Model("pilevolcamon")
    mats = {"skin": ARM, "neck": solid(P, "black_dark")}
    a = humanoid(m, mats, bulk=1.35, arm_bulk=1.4, leg_bulk=1.3, hand_pose="fist", name="pilevolcamon")
    bd = a["body"]
    m.round_box(bd, 0, 0.4, 6.0, 4.6, 31.0, 35.0, metal(P, "gold", dark="gold_dark"), cut=1)   # champion's belt
    m.round_box(bd, 0, -4.4, 2.6, 0.6, 31.4, 34.6, metal(P, "gold"), cut=0)
    for j in range(4):                                                                   # white scarf
        m.box(bd, 2.0 + j * 2.4, 50.0 - j * 0.6, 2.0 + j * 1.6, 4.4 + j * 2.4, 52.0 - j * 0.6, 2.2 + j * 1.6,
              fabric(P, "white", "white_dark"), rotation=(0, -15, 0), pivot=(3.2 + j * 2.4, 51.0, 2.1 + j * 1.6))
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 3.0, 3.2, 54.0, 61.0, STEEL, cut=1)                           # riveted helmet
    m.box(hd, -2.4, 57.0, -3.75, 2.4, 58.4, -3.5, solid(P, "visor", glow=True))
    for nm in ("arm_left", "arm_right"):                                                 # pile-driver fists
        w = a[nm]["wrist"]
        m.round_box(a[nm]["bone"], w[0], w[2] - 1.0, 4.6, 4.6, w[1] - 7.0, w[1] + 2.0, STEEL, cut=1)
        for f in range(4):
            m.round_box(a[nm]["bone"], w[0] + (f - 1.5) * 2.2, w[2] - 5.8, 1.0, 1.0, w[1] - 6.0, w[1] - 1.0, STEEL, cut=0)
    for sx in (-1, 1):                                                                   # volcanic shoulder vents
        rod(m, bd, (sx * 7.0, 52.0, 2.0), (sx * 8.0, 56.0, 3.0), 3, metal(P, "steel", dark="steel_dark"), extend=0.3)
        for j in range(3):
            ball(m, bd, (sx * (9.0 + j * 2.0), 59.0 + j * 2.6, 3.0 + j), 2.6 + j * 0.6, solid(P, "smoke"), layers=2)
            ball(m, bd, (sx * (8.0 + j * 2.4), 58.0 + j * 2.0, 1.0), 0.6, solid(P, "spark", glow=True), layers=1)
    return m
