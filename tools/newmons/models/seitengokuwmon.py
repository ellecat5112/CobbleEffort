"""Seiten Gokuwmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the Great Sage Equal to Heaven: a monkey king warrior in red-and-gold lacquered armour
with black trim, a blazing golden mane of fire and a golden circlet, a long golden staff, a red sash and prayer beads,
a golden flame-tipped tail, and a little pink pig companion riding on its shoulder. 35 blocks.

Front is -z, y is up. 68 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, fur, metal, solid, strands
from _route import pal, tone

HEIGHT = 68
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a monkey king warrior in red-and-gold lacquered armour with a blazing golden fire mane, a golden staff and a little pig companion"
BASE = {"red": (190, 30, 30), "red_dark": (100, 10, 10), "gold": (250, 210, 70), "gold_dark": (170, 120, 20),
        "black": (30, 28, 30), "fur": (200, 140, 60), "fur_dark": (130, 80, 30), "flame": (255, 220, 90),
        "pink": (240, 160, 180), "bead": (120, 70, 40), "face": (230, 190, 150), "eye": (220, 40, 40)}
SHINY = {"red": (40, 80, 170), "red_dark": (14, 30, 100), "flame": (180, 230, 255)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "red", "red_dark", trim="gold", trim_w=0.3)
GOLD = metal(P, "gold", dark="gold_dark")
FUR = fur(P, "fur", "fur_dark", length=1.2)


def build():
    m = Model("seitengokuwmon")
    mats = {"skin": ARM, "neck": FUR, "hand": armour(P, "black", "black"), "finger": armour(P, "black", "black"),
            "upper_arm": FUR, "thigh": armour(P, "black", "black")}
    a = humanoid(m, mats, bulk=1.0, arm_bulk=1.0, leg_bulk=1.0, name="seitengokuwmon")
    bd = a["body"]
    m.round_box(bd, 0, 0, 5.2, 4.0, 31.0, 33.4, GOLD, cut=1)                               # gold belt
    for j in range(12):                                                                  # prayer beads
        ang = 2 * math.pi * j / 12
        m.round_box(bd, 5.0 * math.cos(ang), 3.6 * math.sin(ang) - 0.4, 0.7, 0.7, 50.0 + 1.6 * math.sin(ang * 2),
                    51.4 + 1.6 * math.sin(ang * 2), solid(P, "bead"), cut=0)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.6, 2.8, 54.0, 60.0, FUR, cut=1)
    m.round_box(hd, 0, -2.8, 2.0, 0.8, 54.4, 58.6, solid(P, "face"), cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.8), 57.2, -3.7, max(sx * 0.6, sx * 1.8), 57.8, -3.5, solid(P, "eye"))
    m.round_box(hd, 0, -0.4, 2.9, 3.0, 58.6, 59.6, GOLD, cut=1)                             # golden circlet
    for j in range(14):                                                                  # blazing fire mane
        ang = math.radians(-110 + j * 17)
        spike(m, hd, (2.6 * math.sin(ang), 58.0 + 2.0 * math.cos(ang), 1.0), (math.sin(ang), math.cos(ang) + 0.3, 0.6),
              2.0, 8.0 + (j % 3) * 3.0, solid(P, "flame", glow=True), tip=0.8)
    w = a["arm_right"]["wrist"]                                                          # golden staff
    rod(m, a["arm_right"]["bone"], (w[0], w[1] - 30.0, w[2] - 1.0), (w[0], w[1] + 34.0, w[2] - 1.0), 1, GOLD, extend=0.2)
    for yy in (w[1] - 30.0, w[1] + 34.0):
        m.round_box(a["arm_right"]["bone"], w[0], w[2] - 1.0, 1.2, 1.2, yy - 1.0, yy + 1.0, solid(P, "red"), cut=0)
    ball(m, bd, (7.0, 54.0, 2.0), 2.6, solid(P, "pink"), layers=2)                          # little pig companion
    m.round_box(bd, 7.0, -0.6, 1.2, 0.6, 53.0, 54.4, solid(P, "pink"), cut=0)
    tl = m.bone("tail", bd, (0, 32, 3))
    pts = [(0, 32.0, 3.0), (3.0, 24.0, 10.0), (8.0, 28.0, 16.0), (10.0, 36.0, 18.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, FUR, extend=0.2, t2=2)
    spike(m, tl, pts[-1], (0.2, 1, 0.2), 1.6, 5.0, solid(P, "flame", glow=True), tip=0.8)
    return m
