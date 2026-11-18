"""Minomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little bagworm: a pale green round head with two pointed leafy ears, tiny black eyes, a pink
mouth patch and two long thin antennae, hanging out of a shaggy cocoon of red and brown leaves. 0.5 blocks tall.

Front is -z, y is up. 18 units tall; Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.5, HEIGHT, 1.2)
KIND = "floater"
K = 3
LOOK = "a little bagworm with a pale green head, leafy ears, long antennae and a shaggy cocoon of red and brown leaves"
BASE = {"green": (200, 236, 160), "green_dark": (130, 180, 100), "leaf": (200, 70, 40), "leaf_dark": (120, 50, 30),
        "leaf_b": (170, 110, 50), "pink": (240, 150, 170), "black": (20, 20, 24)}
SHINY = {"green": (240, 220, 140), "green_dark": (190, 160, 80), "leaf": (90, 140, 210), "leaf_dark": (40, 70, 140)}


def P(v):
    return pal(BASE, SHINY, v)


HEAD = skin(P, "green", dark="green_dark")


def build():
    m = Model("minomon")
    top = m.bone("minomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    for row in range(4):                                                                 # cocoon of leaves
        r = 4.6 - row * 0.9
        for i in range(8):
            ang = 2 * math.pi * (i + row * 0.5) / 8
            spike(m, bd, (r * 0.6 * math.cos(ang), 8.0 - row * 2.0, r * 0.6 * math.sin(ang)),
                  (math.cos(ang) * 0.6, -1, math.sin(ang) * 0.6), 2.2, 4.0,
                  solid(P, "leaf" if (i + row) % 2 else "leaf_b"), tip=0.8)
    ball(m, bd, (0, 6.0, 0), 3.4, solid(P, "leaf_dark"), layers=3, ry=4.0)
    hd = m.bone("head", bd, (0, 11, 0))
    ball(m, hd, (0, 12.0, -0.4), 3.6, HEAD, layers=4, ry=3.2)
    for sx in (-1, 1):
        m.box(hd, sx * 1.2 - 0.4, 12.4, -3.95, sx * 1.2 + 0.4, 13.2, -3.8, solid(P, "black"))
        spike(m, hd, (sx * 2.6, 14.0, 0), (sx * 1, 0.6, 0), 2.0, 3.6, HEAD, tip=0.8)          # leafy ears
        pts = [(sx * 0.6, 15.0, 0), (sx * 1.6, 17.0, 0.6), (sx * 3.0, 18.4, 1.0)]
        for p0, p1 in zip(pts, pts[1:]):                                                # long antennae
            rod(m, hd, p0, p1, 1, solid(P, "black"), extend=0.1)
    m.round_box(hd, 0, -3.6, 1.0, 0.4, 10.4, 11.8, solid(P, "pink"), cut=0)
    return m
