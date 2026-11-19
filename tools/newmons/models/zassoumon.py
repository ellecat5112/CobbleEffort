"""Zassoumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a wild weed flytrap: a green bulb head veined darker with a gaping fanged red mouth, a crown of ragged
lime leaves, a long whip of a vine body ending in a curling tail, and thin black tendrils. 15 blocks.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 33
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "a wild green weed flytrap with a veined bulb head, a gaping fanged red mouth, a crown of ragged lime leaves and a vine body"
BASE = {"green": (100, 160, 60), "green_dark": (40, 90, 30), "vein": (30, 70, 24), "lime": (190, 230, 80),
        "mouth": (190, 40, 50), "tooth": (250, 250, 240), "black": (24, 24, 20)}
SHINY = {"green": (170, 120, 60), "green_dark": (100, 60, 20), "lime": (240, 180, 90)}


def P(v):
    return pal(BASE, SHINY, v)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(math.sin(x * 1.3 + y * 0.7) * math.cos(z * 1.1 - y * 0.5)) < 0.1:
        return tone(p["vein"], face), None
    return skin(P, "green", dark="green_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("zassoumon")
    top = m.bone("zassoumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    pts = [(-6.0, 2.0, 0), (-2.0, 1.0, 2.0), (2.0, 3.0, 3.0), (3.0, 8.0, 2.0), (1.0, 14.0, 0.0), (0, 18.0, 0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, bd, p0, p1, 2, skin(P, "green", dark="green_dark"), extend=0.5)
    for i in range(8):
        ang = i * 0.8
        r = 2.6 - i * 0.25
        rod(m, bd, (-6.0 - r * math.cos(ang), 2.0 + r * math.sin(ang), 0),
            (-6.0 - (r - 0.25) * math.cos(ang + 0.8), 2.0 + (r - 0.25) * math.sin(ang + 0.8), 0), 1,
            skin(P, "green", dark="green_dark"), extend=0.2)
    hd = m.bone("head", bd, (0, 24, 0))
    ball(m, hd, (0, 24.0, 0.6), 6.0, headf, layers=5)
    m.box(hd, -4.0, 19.6, -6.6, 4.0, 23.6, -2.6, solid(P, "mouth"))
    for j in range(6):
        x = -3.4 + j * 1.36
        spike(m, hd, (x, 23.6, -6.0), (0, -1, 0), 0.9, 2.2, solid(P, "tooth"), tip=0.8)
        spike(m, hd, (x, 19.6, -6.0), (0, 1, 0), 0.9, 1.6, solid(P, "tooth"), tip=0.8)
    for j in range(9):
        ang = (j - 4) * 0.36
        spike(m, hd, (math.sin(ang) * 3.4, 29.0, 1.0), (math.sin(ang) * 1.0, 1, 0.3), 1.6, 6.0, solid(P, "lime"), tip=0.8)
    for sx in (-1, 1):
        pts = [(sx * 1.0, 16.0, 0), (sx * 7.0, 18.0, -1.0), (sx * 10.0, 14.0, 0), (sx * 8.0, 10.0, 1.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, bd, p0, p1, 1, solid(P, "black"), extend=0.2)
    return m
