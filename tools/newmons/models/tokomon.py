"""Tokomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little white puffball with dot eyes, pink cheeks, a cat mouth with two little fangs, a pair of
wispy feelers on top and four stubby feet. 0.5 blocks.

Front is -z, y is up. Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _digi import sized
from _digibeast import ball
from _digidetail import fur, plane, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.5, HEIGHT, 1.0)
KIND = "biped"
K = 4
LOOK = "a little white puffball with dot eyes, pink cheeks, two little fangs, wispy feelers and four stubby feet"
BASE = {"white": (250, 248, 250), "white_dark": (210, 200, 214), "eye": (20, 20, 24), "pink": (250, 180, 190),
        "fang": (255, 255, 255), "mouth": (180, 60, 70)}
SHINY = {"white": (250, 230, 170), "white_dark": (210, 180, 110)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            if math.hypot(a - sx * 1.8, b - 7.0) < 0.7:
                return p["eye"], None
            if math.hypot(a - sx * 3.2, b - 5.6) < 0.8:
                return p["pink"], None
        if abs(b - 5.4) < 0.25 and abs(a) < 1.2:
            return p["mouth"], None
        if 4.4 < b < 5.2 and 0.4 < abs(a) < 0.9:
            return p["fang"], None
    return fur(P, "white", "white_dark", length=0.6)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("tokomon")
    top = m.bone("tokomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 6.4, 0), 5.0, bodyf, layers=5, squash=0.85)
    for sx in (-1, 1):                                                                 # wispy feelers
        pts = [(sx * 1.2, 10.6, 0), (sx * 2.0, 13.0, 0.4), (sx * 1.0, 15.0, 0.8), (sx * 2.0, 17.6, 1.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, bd, p0, p1, 1, solid(P, "white_dark"), extend=0.3)
    for i, (sx, sz) in enumerate(((1, -1), (-1, -1), (1, 1), (-1, 1))):
        m.round_box(top, sx * 2.6, sz * 2.0, 1.0, 1.0, 0.0, 2.0, solid(P, "white"), cut=0)
    return m
