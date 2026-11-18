"""Machmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
racing machine: a shark-nosed silver motorbike creature with two big red-and-black wheels, a fanged grey shark head
with a green eye, a ribbed spine of silver fins, swept horns and long silver blades thrusting forward from its nose.
15 blocks long.

Front is -z, y is up. 28 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import slab_z
from _digidetail import armour, gem, metal, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
LOOK = "a shark-nosed silver motorbike creature with two big red-and-black wheels, a fanged shark head, silver fins and forward blades"
BASE = {"silver": (210, 214, 226), "silver_dark": (100, 104, 120), "grey": (110, 114, 124), "grey_dark": (50, 52, 60),
        "red": (210, 40, 40), "red_dark": (120, 14, 18), "black": (30, 30, 34), "green": (60, 220, 140),
        "green_light": (200, 255, 220), "tooth": (250, 248, 236), "mouth": (180, 60, 50), "eye": (250, 210, 60)}
SHINY = {"red": (60, 120, 230), "red_dark": (20, 50, 140)}


def P(v):
    return pal(BASE, SHINY, v)


SIL = metal(P, "silver", dark="silver_dark")
GREY = armour(P, "grey", "grey_dark")


def wheel(m, bone, c, r):
    x, y, z = c
    for i in range(6):
        m.box(bone, x - 1.6, y - r, z - 1.2, x + 1.6, y + r, z + 1.2, armour(P, "red", "red_dark") if i % 2 else solid(P, "black"),
              rotation=(i * 30.0, 0, 0), pivot=c)
    m.round_box(bone, x, z, 1.8, 1.8, y - 1.6, y + 1.6, SIL, cut=0)


def build():
    m = Model("machmon")
    top = m.bone("machmon", None, (0, 0, 0))
    lf = m.bone("leg_left", top, (0, 6, -10))
    wheel(m, lf, (0, 6.0, -10.0), 6.0)
    lb = m.bone("leg_right", top, (0, 6, 12))
    wheel(m, lb, (0, 6.0, 12.0), 6.0)
    bd = m.bone("body", top, (0, 12, 0))
    for i in range(7):
        slab_z(m, bd, 0, 12.0, -10.0 + i * 3.4, -6.6 + i * 3.4, 3.0, 3.0, SIL)
    m.round_box(bd, 0, 1.0, 3.2, 3.2, 10.0, 11.4, gem(P, "green", "green_light"), cut=0)
    for i in range(7):                                                               # ribbed spine fins
        spike(m, bd, (0, 15.0, -8.0 + i * 3.4), (0, 1, 0.6), 1.4, 4.0, SIL, tip=0.8)
    hd = m.bone("head", bd, (0, 14, -12))
    m.round_box(hd, 0, -15.0, 3.0, 4.6, 11.0, 17.0, GREY, cut=1)
    m.round_box(hd, 0, -18.4, 2.6, 1.2, 10.4, 12.0, solid(P, "mouth"), cut=0)
    for j in range(5):
        spike(m, hd, (-2.0 + j, 12.0, -19.4), (0, -1, 0), 0.8, 1.4, solid(P, "tooth"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.8, sx * 3.2), 15.0, -17.0, max(sx * 2.8, sx * 3.2), 15.8, -15.6, solid(P, "eye", glow=True))
        pts = [(sx * 2.0, 16.6, -12.0), (sx * 6.0, 20.0, -10.0), (sx * 8.0, 20.0, -6.0)]       # swept horns
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "silver_dark"), extend=0.2, t2=1)
    for j in range(3):                                                               # forward blades
        spike(m, hd, (-2.0 + j * 2.0, 9.0 - j * 0.6, -16.0), ((j - 1) * 0.2, -0.2, -1), 2.0, 14.0 - j * 2.0, SIL, tip=0.8)
    return m
