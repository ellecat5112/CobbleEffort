"""Tyumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a gangly hot-pink mouse prankster: big round stitched ears, a cross-eyed grin full of bucked teeth, long
thin arms ending in big black-clawed hands, a skinny tail curling into a spiral, and a little golden imp with a
grinning face bobbing over its shoulder. 1 block.

Front is -z, y is up. Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import plane, skin, solid
from _route import pal, tone

HEIGHT = 35
SCALE, HITBOX = sized(1.0, HEIGHT, 2.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 14}
LOOK = "a gangly hot-pink mouse prankster with big stitched ears, a bucked-tooth grin, long black-clawed hands and a little golden imp"
BASE = {"pink": (240, 120, 190), "pink_dark": (190, 70, 140), "white": (255, 255, 255), "eye": (30, 20, 30),
        "red": (220, 60, 60), "claw": (30, 30, 34), "gold": (240, 200, 60), "gold_dark": (180, 130, 20),
        "mouth": (150, 20, 40), "stitch": (60, 30, 50)}
SHINY = {"pink": (120, 200, 240), "pink_dark": (60, 140, 190)}


def P(v):
    return pal(BASE, SHINY, v)


PINK = skin(P, "pink", dark="pink_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx, col in ((-1, "eye"), (1, "red")):
            d = math.hypot(a - sx * 1.6, b - 25.4)
            if d < 1.2:
                return (p[col] if d < 0.5 else p["white"]), None
        if 20.6 < b < 23.0 and abs(a) < 2.6:
            if b > 21.8 and abs(a) < 1.4:
                return p["white"], None
            return p["mouth"], None
    return PINK(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("tyumon")
    top = m.bone("tyumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 0, 3.4, 3.0, 8.0, 18.0, PINK, cut=1)
    hd = m.bone("head", bd, (0, 18, 0))
    ball(m, hd, (0, 23.6, -0.6), 4.0, headf, layers=4)
    for sx in (-1, 1):                                                                 # big stitched ears
        m.round_box(hd, sx * 4.4, 0, 2.6, 1.0, 26.0, 31.0, PINK, cut=1)
        for j in range(3):
            m.box(hd, sx * 4.4 + (j - 1) * 1.2 - 0.15, 30.6, -0.4, sx * 4.4 + (j - 1) * 1.2 + 0.15, 32.0, 0.4,
                  solid(P, "stitch"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.4, 16.0, 0))
        rod(m, ab, (sx * 3.4, 16.0, 0), (sx * 9.0, 18.0, -2.0), 1, PINK, extend=0.3)
        rod(m, ab, (sx * 9.0, 18.0, -2.0), (sx * 11.0, 14.0, -3.0), 1, PINK, extend=0.3)
        ball(m, ab, (sx * 11.4, 13.0, -3.2), 1.6, PINK, layers=2)
        for f in range(3):
            spike(m, ab, (sx * 11.4 + (f - 1) * 0.8, 11.6, -4.4), (0, -0.6, -1), 0.8, 1.8, solid(P, "claw"), tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.8, 8.0, 0))
        rod(m, lg, (sx * 1.8, 8.0, 0), (sx * 2.6, 1.6, 0), 1, PINK, extend=0.3)
        m.round_box(lg, sx * 2.6, -1.4, 1.4, 2.4, 0.0, 1.6, PINK, cut=0)
    tl = m.bone("tail", bd, (0, 9, 3))
    for i in range(10):                                                                # spiral tail
        ang = i * 0.7
        r = 3.6 - i * 0.3
        p0 = (4.0 + r * math.cos(ang), 9.0 + r * math.sin(ang), 4.0)
        ang2 = (i + 1) * 0.7
        r2 = 3.6 - (i + 1) * 0.3
        p1 = (4.0 + r2 * math.cos(ang2), 9.0 + r2 * math.sin(ang2), 4.0)
        rod(m, tl, p0, p1, 1, PINK, extend=0.2)
    ib = m.bone("imp", bd, (7, 32, 0))                                                 # golden imp
    ball(m, ib, (7.0, 33.0, 0), 1.8, solid(P, "gold"), layers=2)
    for sx in (-1, 1):
        spike(m, ib, (7.0 + sx * 1.6, 34.0, 0), (sx, 0.6, 0), 0.8, 1.8, solid(P, "gold_dark"), tip=0.8)
    return m
