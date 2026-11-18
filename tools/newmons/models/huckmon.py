"""Huckmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
little dragon knight-to-be: a lean white-and-black dragon cub in white armour plates with a sharp-nosed helm, yellow
eyes, a long tattered red scarf streaming behind like wings, a steel ring on its arm and dark claws. Child stage,
1 block tall.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import theropod
from _digidetail import armour, fabric, metal, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.8)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 12}
LOOK = "a lean white-and-black dragon cub in white armour plates with a sharp helm and a long tattered red scarf"
BASE = {"white": (240, 240, 246), "white_dark": (170, 172, 190), "black": (40, 40, 46), "red": (210, 30, 40),
        "red_dark": (130, 10, 16), "steel": (200, 204, 214), "steel_dark": (100, 104, 116), "eye": (250, 220, 60),
        "claw": (40, 40, 80), "mouth": (110, 20, 30), "tooth": (250, 250, 240)}
SHINY = {"white": (60, 60, 70), "white_dark": (24, 24, 30), "red": (40, 140, 200), "red_dark": (14, 70, 120)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "white", "white_dark", trim="black", trim_w=0.3)


def build():
    m = Model("huckmon")
    mats = {"skin": ARM, "belly": skin(P, "black", dark="black"), "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"),
            "claw": solid(P, "claw"), "talon": solid(P, "claw")}
    a = theropod(m, mats, "huckmon", hip_y=9.0, chest=(0, 15.0, -1.0), body_r=3.4, chest_r=3.4,
                 neck_top=(0, 19.0, -3.0), head_len=7.0, head_w=2.6, head_h=2.8, mouth_open=10, teeth=3, arm_len=5.0,
                 leg_bulk=0.7, tail=((0, 9, 4), (0, 7, 9), (0, 6, 14)), tail_r=(2.0, 1.4, 0.8))
    hd, bd = a["head"], a["body"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.6,
              solid(P, "eye"))
        spike(m, hd, (sx * 1.6, ey + 1.6, ez + 1.6), (sx * 0.3, 0.6, 1), 1.0, 3.6, ARM, tip=0.8)
    spike(m, hd, (0, ey + 1.0, a["snout_front"]), (0, 0.6, -1), 1.2, 2.6, ARM, tip=0.8)
    for side in (1, -1):                                                              # tattered red scarf
        pts = [(side * 1.0, 18.6, 2.0), (side * 6.0, 22.0, 6.0), (side * 12.0, 24.0, 8.0), (side * 16.0, 20.0, 10.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, bd, p0, p1, 1, fabric(P, "red", "red_dark"), extend=0.4, t2=4 - j)
    arm = a["arm_left"]
    m.round_box(arm["bone"], arm["hand"][0], arm["hand"][2], 1.4, 1.4, arm["hand"][1] + 1.0, arm["hand"][1] + 2.0,
                metal(P, "steel", dark="steel_dark"), cut=0)
    return m
