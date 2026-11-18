"""Kyaromon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a Baby
II cream fluff-ball with one big blue eye on each side marked by a red streak, two very long pointed ears, a tiny
mouth, two little claw-feet and a big curling tail banded violet and white. Half a block tall.

Front is -z, y is up. 18 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, skin, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.5, HEIGHT, 1.2)
KIND = "floater"
K = 4
LOOK = "a cream fluff-ball with big blue eyes marked by red streaks, very long pointed ears and a curling violet-banded tail"
BASE = {"cream": (246, 236, 220), "cream_dark": (200, 186, 160), "blue": (60, 150, 230), "pupil": (16, 16, 24),
        "red": (220, 50, 50), "violet": (140, 110, 190), "claw": (230, 230, 230)}
SHINY = {"cream": (250, 220, 230), "cream_dark": (210, 160, 180), "violet": (90, 180, 140)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "cream", "cream_dark", length=0.8)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.8, y - 5.6)
            if d < 0.5:
                return tone(p["pupil"], face), None
            if d < 1.2:
                return tone(p["blue"], face), None
            if abs(y - 7.2 - (sx * x - 1.4) * 0.6) < 0.2 and 1.0 < sx * x < 3.0:
                return tone(p["red"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def tailf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["violet"] if (y + z) % 2.4 < 1.0 else p["cream"], face), None


def build():
    m = Model("kyaromon")
    top = m.bone("kyaromon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 5.0, 0), 4.6, bodyf, layers=4, squash=0.9)
    hd = m.bone("head", bd, (0, 9, 0))
    for sx in (-1, 1):                                                               # very long ears
        spike(m, hd, (sx * 2.0, 8.6, 0.6), (sx * 0.4, 1, 0.2), 2.0, 9.0, FUR, tip=0.8)
        spike(m, bd, (sx * 1.6, 1.0, -2.6), (0, -0.6, -1), 0.8, 1.4, solid(P, "claw"), tip=0.8)
    tb = m.bone("tail", bd, (0, 5, 4))
    pts = [(0, 5.0, 4.0), (2.0, 8.0, 7.0), (3.0, 12.0, 6.0), (2.0, 14.0, 3.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 2, tailf, extend=0.4)
    return m
