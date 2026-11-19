"""Tsubumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a tiny cream droplet with shiny black eyes, pink cheeks and an open fanged smile, and one long
leaf-like ear-sprout sweeping up from its head. 0.35 blocks.

Front is -z, y is up. Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import plane, skin, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.35, HEIGHT, 1.2)
KIND = "floater"
K = 4
LOOK = "a tiny cream droplet with shiny black eyes, pink cheeks, a fanged smile and one long leaf-like ear-sprout"
BASE = {"cream": (252, 248, 210), "cream_dark": (220, 210, 150), "eye": (20, 20, 24), "white": (255, 255, 255),
        "pink": (250, 180, 190), "mouth": (220, 90, 120)}
SHINY = {"cream": (210, 240, 250), "cream_dark": (150, 200, 230)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            d = math.hypot(a - sx * 1.8, b - 6.6)
            if d < 0.9:
                return (p["white"] if math.hypot(a - sx * 1.8 + 0.3, b - 6.9) < 0.3 else p["eye"]), None
            if math.hypot(a - sx * 3.0, b - 5.0) < 0.8:
                return p["pink"], None
        if 3.6 < b < 5.0 and abs(a) < 1.4 - (5.0 - b) * 0.6:
            return p["mouth"], None
    return skin(P, "cream", dark="cream_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("tsubumon")
    top = m.bone("tsubumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 6.0, 0), 4.6, bodyf, layers=5, squash=0.85)
    pts = [(0, 9.6, 0.6), (1.6, 13.0, 1.0), (4.0, 17.0, 1.0), (7.0, 21.0, 0.6)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, bd, p0, p1, 2 if i < 2 else 1, skin(P, "cream", dark="cream_dark"), extend=0.4, t2=3 - i)
    spike(m, bd, (2.0, 13.0, 1.0), (1, 0.6, 0), 1.4, 4.0, skin(P, "cream", dark="cream_dark"), tip=0.8)
    return m
