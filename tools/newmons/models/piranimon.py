"""Piranimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the pirate piranha: a black-and-red fish with a huge jaw of jagged teeth, spiny red fins, a green
pirate's coat with a skull-and-crossbones, and a bone-and-barbed-wire tail ending in a hook. 25 blocks long.

Front is -z, y is up. 34 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, metal, scales, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "a black-and-red pirate piranha with a huge jaw of jagged teeth, spiny red fins, a green skull-marked coat and a bone hook tail"
BASE = {"black": (44, 42, 48), "black_dark": (14, 14, 18), "red": (180, 30, 30), "red_dark": (100, 10, 10),
        "green": (60, 130, 70), "green_dark": (24, 70, 30), "bone": (236, 230, 214), "tooth": (250, 250, 240),
        "eye": (250, 220, 40), "mouth": (110, 20, 30), "steel": (180, 184, 196)}
SHINY = {"black": (60, 90, 160), "black_dark": (20, 34, 90), "red": (240, 190, 60)}


def P(v):
    return pal(BASE, SHINY, v)


SC = scales(P, "black", "black_dark", size=1.4)


def build():
    m = Model("piranimon")
    top = m.bone("piranimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    ball(m, bd, (0, 17.0, 2.0), 8.0, SC, layers=6, ry=8.0, squash=1.3)
    m.round_box(bd, 0, 5.0, 8.4, 6.0, 12.0, 22.0, fabric(P, "green", "green_dark"), cut=2)   # pirate coat
    m.box(bd, 4.0, 15.0, -1.2, 6.0, 19.0, -0.9, solid(P, "bone"), rotation=(0, -40, 0), pivot=(5.0, 17.0, -1.0))
    hd = m.bone("head", bd, (0, 18, -8))
    m.round_box(hd, 0, -10.0, 6.0, 5.0, 18.0, 26.0, SC, cut=2)                              # upper jaw
    jb = m.bone("jaw", hd, (0, 14, -8))
    m.round_box(jb, 0, -10.0, 5.6, 5.0, 9.0, 15.0, SC, cut=2)                               # lower jaw
    m.box(hd, -5.0, 15.0, -14.6, 5.0, 18.0, -8.0, solid(P, "mouth"))
    for j in range(7):                                                                   # jagged teeth
        for sx in (-1, 1):
            spike(m, hd, (sx * 4.6, 18.0, -14.0 + j * 1.6), (0, -1, 0), 1.2, 2.4, solid(P, "tooth"), tip=0.8)
            spike(m, jb, (sx * 4.4, 15.0, -13.4 + j * 1.6), (0, 1, 0), 1.0, 2.0, solid(P, "tooth"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 6.0, sx * 6.2), 22.0, -8.0, max(sx * 6.0, sx * 6.2), 23.6, -6.4, solid(P, "eye", glow=True))
    for j in range(6):                                                                   # spiny red fins
        spike(m, bd, (0, 24.0 - j * 0.4, -4.0 + j * 2.4), (0, 1, 0.3), 1.6, 8.0 - abs(j - 2) * 1.0,
              scales(P, "red", "red_dark", size=1.0), tip=0.8)
    for sx in (-1, 1):
        spike(m, bd, (sx * 7.0, 14.0, 2.0), (sx * 1, -0.4, 0.4), 1.6, 6.0, solid(P, "red"), tip=0.8)
    tb = m.bone("tail", bd, (0, 17, 12))                                                 # bone-and-wire tail
    pts = [(0, 17.0, 12.0), (0, 20.0, 18.0), (2.0, 26.0, 22.0), (4.0, 30.0, 20.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 2, solid(P, "bone"), extend=0.3)
    spike(m, tb, pts[-1], (0.4, -1, -0.6), 1.4, 4.0, metal(P, "steel"), tip=0.8)
    return m
