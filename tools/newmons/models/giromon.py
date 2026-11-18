"""Giromon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
living mine: a floating blue riveted sphere with two curved horns, red eyes and a jagged grin, its arms long chains
ending in a red chainsaw and a big brown glove holding a red spiked mine. 25 blocks tall.

Front is -z, y is up. 34 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import leather, metal, riveted, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(25, HEIGHT, 3.6)
KIND = "floater"
K = 3
LOOK = ("a floating blue riveted sphere with curved horns, red eyes and a jagged grin, chain arms ending in a chainsaw "
        "and a glove holding a red spiked mine")
BASE = {"blue": (70, 80, 170), "blue_dark": (30, 34, 90), "horn": (150, 120, 220), "eye": (220, 30, 40),
        "white": (250, 250, 250), "mouth": (20, 16, 24), "tooth": (250, 250, 246), "steel": (190, 196, 210),
        "steel_dark": (90, 96, 110), "red": (210, 40, 40), "red_dark": (130, 14, 18), "glove": (170, 110, 60),
        "glove_dark": (110, 66, 30)}
SHINY = {"blue": (200, 60, 60), "blue_dark": (120, 20, 20), "red": (60, 90, 200)}


def P(v):
    return pal(BASE, SHINY, v)


SPH = riveted(P, "blue", "blue_dark")
STEEL = metal(P, "steel", dark="steel_dark")


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if 16.0 < y < 19.0 and abs(x) < 6.0:
            if (y > 18.0 or y < 17.0) and abs((x * 0.8) % 1.6 - 0.8) < 0.5:
                return tone(p["tooth"], face), None
            return tone(p["mouth"], face), None
        for sx in (-1, 1):
            if math.hypot(x - sx * 3.0, y - 23.0) < 1.6:
                return tone(p["eye"] if math.hypot(x - sx * 3.0, y - 23.0) < 0.9 else p["white"], face), None
    return SPH(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("giromon")
    top = m.bone("giromon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    ball(m, bd, (0, 21.0, 0), 9.0, facef, layers=6)
    hd = m.bone("head", bd, (0, 28, 0))
    for sx in (-1, 1):                                                                 # curved horns
        pts = [(sx * 6.0, 27.0, 0), (sx * 10.0, 31.0, 0), (sx * 11.0, 36.0, 1.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 2, solid(P, "horn"), extend=0.4)
    al = m.bone("arm_left", bd, (8.0, 20.0, 0))                                          # chain + glove + mine
    for j in range(6):
        m.round_box(al, 9.0 + j * 2.0, -1.0, 0.8, 0.8, 19.0 - j * 1.4, 20.6 - j * 1.4, STEEL, cut=0)
    m.round_box(al, 22.0, -2.0, 3.0, 3.0, 7.0, 12.0, leather(P, "glove", "glove_dark"), cut=1)
    ball(m, al, (22.0, 13.0, -3.0), 3.0, solid(P, "red"), layers=3)
    for ang in range(0, 360, 72):
        r_ = math.radians(ang)
        spike(m, al, (22.0 + 3.0 * math.cos(r_), 13.0 + 3.0 * math.sin(r_), -3.0), (math.cos(r_), math.sin(r_), 0), 1.0,
              1.6, STEEL)
    ar = m.bone("arm_right", bd, (-8.0, 20.0, 0))                                         # chain + chainsaw
    for j in range(6):
        m.round_box(ar, -9.0 - j * 2.0, -1.0, 0.8, 0.8, 19.0 - j * 1.6, 20.6 - j * 1.6, STEEL, cut=0)
    m.round_box(ar, -21.0, -2.0, 2.0, 2.0, 8.0, 12.0, solid(P, "red"), cut=1)
    m.box(ar, -22.0, -2.0, -2.6, -20.0, 8.0, -1.4, STEEL)
    rod(m, ar, (-21.0, 8.0, -2.0), (-25.0, -2.0, -2.0), 2, STEEL, extend=0, t2=1)
    for j in range(6):
        spike(m, ar, (-21.4 - j * 0.6, 6.0 - j * 1.6, -2.0), (-1, -0.2, 0), 0.6, 1.0, solid(P, "steel_dark"))
    return m
