"""Panimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the sketch art on wikimon.net): a wild
goat-god of panic: a grey goat-headed demon with great curled horns, a fanged grimace, a shaggy beard and mane, a
broad bat wing, clawed hands and goat legs. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing
from _digibody import humanoid
from _digidetail import fabric, fur, metal, skin, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a grey goat-headed demon with great curled horns, a fanged grimace, a shaggy beard and mane, a broad bat wing and goat legs"
BASE = {"grey": (170, 170, 176), "grey_dark": (90, 90, 98), "fur": (220, 220, 214), "fur_dark": (150, 150, 144),
        "horn": (110, 104, 96), "black": (30, 30, 34), "eye": (230, 40, 40), "tooth": (250, 250, 240),
        "wing": (70, 66, 80), "hoof": (60, 56, 60)}
SHINY = {"grey": (150, 110, 170), "grey_dark": (80, 50, 100), "wing": (120, 40, 40)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "grey", dark="grey_dark")
FUR = fur(P, "fur", "fur_dark", length=1.6)


def build():
    m = Model("panimon")
    mats = {"skin": SKIN, "pelvis": FUR, "thigh": FUR, "knee": FUR, "shin": SKIN, "foot": solid(P, "hoof"),
            "toe": solid(P, "hoof"), "claw": solid(P, "black")}
    a = humanoid(m, mats, bulk=1.1, arm_bulk=1.1, leg_bulk=1.05, claws=True, digitigrade=True, toes=2, name="panimon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, -1))
    m.round_box(hd, 0, -1.6, 2.6, 3.6, 53.6, 60.0, SKIN, cut=1)                            # goat head
    m.round_box(hd, 0, -5.4, 1.8, 1.8, 53.0, 56.4, SKIN, cut=1)
    m.box(hd, -1.6, 53.4, -7.3, 1.6, 54.4, -7.1, solid(P, "black"))
    for j in range(4):
        spike(m, hd, (-1.2 + j * 0.8, 54.4, -7.2), (0, -1, 0), 0.8, 1.2, solid(P, "tooth"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.4), 57.6, -5.3, max(sx * 1.0, sx * 2.4), 58.4, -5.1, solid(P, "eye", glow=True))
        pts = [(sx * 2.2, 59.6, -1.0), (sx * 6.0, 62.0, 1.0), (sx * 8.0, 59.0, 2.0), (sx * 7.0, 55.0, 1.0),
               (sx * 5.0, 54.0, 0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):                                 # great curled horns
            rod(m, hd, p0, p1, max(1, 3 - j // 2), metal(P, "horn", dark="black"), extend=0.3)
    for i in range(8):                                                                   # shaggy beard + mane
        spike(m, hd, ((i - 3.5) * 0.7, 53.4, -4.0 + abs(i - 3.5) * 0.4), (0, -1, -0.3), 1.2, 5.0, FUR, tip=0.8)
        spike(m, hd, ((i - 3.5) * 0.8, 59.0, 1.6), ((i - 3.5) * 0.2, 0.2, 1), 1.4, 6.0, FUR, tip=0.8)
    wb = m.bone("wing_left", bd, (3.0, 48.0, 3.0))                                       # broad bat wing
    bat_wing(m, wb, (3.0, 48.0, 3.0), 28.0, 24.0, 5, solid(P, "black"), fabric(P, "wing", "black"), side=1, sweep=15)
    return m
