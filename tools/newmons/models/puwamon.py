"""Puwamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a fluffy orange owl-chick puff with a ring of flared feather tips, two huge round eyes under a
stern black brow-plate, a spiky brown crown and a long thin curling tail ending in a red-and-white feather tuft.
0.35 blocks.

Front is -z, y is up. 14 units tall; Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import feathers, solid
from _route import pal, tone

HEIGHT = 14
SCALE, HITBOX = sized(0.35, HEIGHT, 2.2)
KIND = "floater"
K = 4
LOOK = "a fluffy orange owl-chick puff with flared feather tips, huge round eyes under a black brow-plate and a curling feather tail"
BASE = {"orange": (240, 140, 60), "orange_dark": (170, 70, 20), "cream": (250, 220, 180), "brown": (110, 60, 30),
        "black": (24, 24, 28), "eye": (250, 236, 200), "pupil": (20, 16, 14), "red": (200, 30, 40),
        "white": (250, 250, 250)}
SHINY = {"orange": (140, 170, 220), "orange_dark": (70, 100, 160)}


def P(v):
    return pal(BASE, SHINY, v)


FEATH = feathers(P, "orange", "orange_dark", tip="cream", size=(1.0, 1.6))


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.0, y - 6.0)
            if d < 0.8:
                return tone(p["pupil"], face), None
            if d < 1.8:
                return tone(p["eye"], face), None
    return FEATH(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("puwamon")
    top = m.bone("puwamon", None, (0, 2, 0))
    bd = m.bone("body", top, (0, 3, 0))
    ball(m, bd, (0, 6.0, 0), 4.8, bodyf, layers=4, ry=4.0)
    for i in range(10):                                                                  # flared feather ring
        ang = 2 * math.pi * i / 10
        spike(m, bd, (4.4 * math.cos(ang), 6.0 + 0.6 * math.sin(ang * 2), 4.0 * math.sin(ang) + 0.6),
              (math.cos(ang), 0.1, math.sin(ang) * 0.6), 1.4, 3.6, FEATH, tip=0.8)
    m.box(bd, -4.6, 7.6, -4.6, 4.6, 8.6, -3.8, solid(P, "black"), rotation=(0, 0, 0), pivot=(0, 8, -4))  # brow plate
    spike(m, bd, (0, 7.6, -4.4), (0, -1, -0.4), 1.0, 1.6, solid(P, "black"), tip=0.8)
    for j in range(5):
        spike(m, bd, ((j - 2) * 1.2, 9.6, 0.4 + abs(j - 2) * 0.3), ((j - 2) * 0.2, 1, 0.3), 1.0, 2.0, solid(P, "brown"),
              tip=0.8)
    tl = m.bone("tail", bd, (0, 3, 3))
    pts = [(0, 3.0, 3.0), (2.0, 0.6, 6.0), (4.0, 1.4, 8.0), (3.0, 2.6, 8.6)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, solid(P, "black"), extend=0.2, t2=1)
    m.round_box(tl, -1.0, 6.0, 1.0, 1.0, 0.0, 2.0, solid(P, "red"), cut=0)
    spike(m, tl, (-1.0, 1.8, 6.0), (0, 1, 0), 0.8, 1.4, solid(P, "white"), tip=0.8)
    return m
