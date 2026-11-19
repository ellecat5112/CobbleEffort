"""Wanyamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a fluffy blue kitten head: shaggy blue fur striped darker, an M-shaped mark on its brow, big glossy
yellow-green eyes, a tiny pink mouth, pointed ears and a long striped tail curling up. 0.5 blocks.

Front is -z, y is up. Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, fur, plane, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.5, HEIGHT, 1.4)
KIND = "biped"
K = 4
LOOK = "a fluffy blue kitten head with an M mark on its brow, big yellow-green eyes and a long striped tail"
BASE = {"blue": (90, 140, 230), "blue_dark": (40, 70, 160), "stripe": (40, 60, 140), "eye": (200, 230, 60),
        "pupil": (20, 20, 10), "white": (255, 255, 255), "mouth": (240, 120, 140)}
SHINY = {"blue": (230, 170, 90), "blue_dark": (170, 110, 40), "stripe": (140, 80, 30)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "blue", "blue_dark", length=1.2)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            c = eye(p, a - sx * 2.2, b - 7.0, 1.5, "eye")
            if c is not None:
                return c, None
        if 9.6 < b < 11.6 and abs(a) < 2.4 and abs(abs(a) - abs(b - 10.6) * 0.0 - (1.2 if b > 10.6 else 2.2)) < 0.4:
            return tone(p["stripe"], face), None
        if math.hypot(a, b - 4.4) < 0.6:
            return p["mouth"], None
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("wanyamon")
    top = m.bone("wanyamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 7.0, 0), 5.6, headf, layers=5)
    for sx in (-1, 1):
        spike(m, bd, (sx * 3.6, 11.0, 0), (sx * 0.6, 1, 0), 2.4, 3.6, FUR, tip=0.8)
        for j in range(3):                                                                # side tufts
            spike(m, bd, (sx * 5.0, 6.0 + j * 1.6, 0), (sx, -0.2 + j * 0.2, 0), 1.2, 2.4, FUR, tip=0.8)
    tl = m.bone("tail", bd, (0, 4, 4))
    pts = [(0, 4.0, 4.6), (3.0, 6.0, 8.0), (6.0, 11.0, 8.0), (6.0, 16.0, 5.0), (4.0, 18.0, 3.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 1, solid(P, "stripe" if i % 2 else "blue"), extend=0.3)
    return m
