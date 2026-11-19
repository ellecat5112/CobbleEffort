"""Zerimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a tiny pale-green droplet with a dark horn-tip on its head, shiny black eyes, a little fang, and a long
tail ending in a three-pointed fin. 0.35 blocks.

Front is -z, y is up. Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import plane, skin, solid
from _route import pal, tone

HEIGHT = 12
SCALE, HITBOX = sized(0.35, HEIGHT, 2.0)
KIND = "floater"
K = 4
LOOK = "a tiny pale-green droplet with a dark horn-tip, shiny black eyes, a little fang and a long three-pointed tail"
BASE = {"green": (210, 236, 190), "green_dark": (150, 190, 130), "horn": (60, 60, 70), "eye": (20, 20, 24),
        "white": (255, 255, 255)}
SHINY = {"green": (250, 220, 190), "green_dark": (210, 170, 130)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            d = math.hypot(a - sx * 1.8, b - 5.0)
            if d < 0.9:
                return (p["white"] if math.hypot(a - sx * 1.8 + 0.3, b - 5.3) < 0.3 else p["eye"]), None
        if abs(b - 3.4) < 0.25 and abs(a) < 0.8:
            return p["eye"], None
    return skin(P, "green", dark="green_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("zerimon")
    top = m.bone("zerimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 5.0, 0), 4.2, bodyf, layers=4, squash=0.85)
    spike(m, bd, (0, 8.0, 0), (0, 1, 0), 2.4, 4.0, bodyf, tip=0.8)
    spike(m, bd, (0, 10.6, 0), (0, 1, 0), 1.0, 1.6, solid(P, "horn"), tip=0.8)
    pts = [(0, 4.0, 3.6), (2.0, 6.0, 7.0), (4.0, 10.0, 9.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, bd, p0, p1, 1, skin(P, "green", dark="green_dark"), extend=0.3)
    for j in range(3):
        spike(m, bd, pts[-1], ((j - 1) * 0.6, 1, 0.3), 1.2, 3.0, skin(P, "green", dark="green_dark"), tip=0.8)
    return m
