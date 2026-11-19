"""Suzumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little golden bell of a baby: a round tan-gold body with two pointed ears, one big green eye under a
dark band, and a fluffy white-and-red ringed tail curling up behind it. 0.5 blocks.

Front is -z, y is up. 16 units tall; Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, metal, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.5, HEIGHT, 1.8)
KIND = "floater"
K = 4
LOOK = "a little round tan-gold bell of a baby with pointed ears, one big green eye under a dark band and a fluffy ringed tail"
BASE = {"tan": (210, 180, 100), "tan_dark": (150, 120, 50), "green": (60, 180, 80), "black": (30, 26, 24),
        "white": (250, 250, 250), "white_dark": (200, 200, 206), "red": (200, 50, 40)}
SHINY = {"tan": (200, 204, 220), "tan_dark": (130, 134, 156)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        d = math.hypot(x, y - 5.0)
        if d < 2.0:
            if d < 0.7:
                return tone(p["black"], face), None
            if math.hypot(x + 0.6, y - 5.6) < 0.4:
                return tone(p["white"], face), None
            return tone(p["green"], face), None
    if abs(y - 7.4 - 0.2 * abs(x)) < 0.3:
        return tone(p["black"], face), None
    return metal(P, "tan", dark="tan_dark")(x, y, z, face, variant, box=box, **k)


def tailf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (y % 3.0) < 0.8:
        return tone(p["red"], face), None
    return fur(P, "white", "white_dark", length=1.0)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("suzumon")
    top = m.bone("suzumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 5.0, 0), 4.4, bodyf, layers=4)
    for sx in (-1, 1):
        spike(m, bd, (sx * 2.6, 8.0, 0), (sx * 0.4, 1, 0), 1.8, 3.0, bodyf, tip=0.8)
    tl = m.bone("tail", bd, (0, 4, 4))
    pts = [(0, 4.0, 4.0), (3.0, 7.0, 7.0), (4.0, 11.0, 7.0), (2.6, 14.0, 5.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 2 + (i > 0), tailf, extend=0.4)
    return m
