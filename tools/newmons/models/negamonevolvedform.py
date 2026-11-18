"""Negamon (Evolved Form) (a Digimon of the CobbleEffort: Digital crossover; after the official magazine art on
wikimon.net): Negamon grown into a vast dark-blue horror: a heaving mass of navy flesh dotted with red-orange suckers,
an enormous gaping mouth lined with huge square teeth, and smaller toothy mouths opening along its trailing tentacles.
25 blocks long.

Front is -z, y is up. 30 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "a vast dark-blue horror of navy flesh dotted with red suckers, an enormous mouth of huge square teeth and toothy tentacles"
BASE = {"blue": (40, 60, 120), "blue_dark": (14, 20, 60), "red": (220, 90, 60), "mouth": (130, 30, 40),
        "tooth": (240, 236, 220)}
SHINY = {"blue": (110, 40, 100), "blue_dark": (50, 10, 50)}


def P(v):
    return pal(BASE, SHINY, v)


BODY0 = skin(P, "blue", dark="blue_dark")


def fleshf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face != "down" and math.sin(x * 1.6) * math.sin(y * 1.6 + z * 1.4) > 0.8:
        return tone(p["red"], face), None
    return BODY0(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("negamonevolvedform")
    top = m.bone("negamonevolvedform", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    ball(m, bd, (0, 16.0, 4.0), 12.0, fleshf, layers=6, ry=12.0, squash=1.1)
    hd = m.bone("head", bd, (0, 16, -8))
    m.round_box(hd, 0, -10.0, 9.0, 4.0, 18.0, 24.0, fleshf, cut=2)                        # upper lip
    jb = m.bone("jaw", hd, (0, 14, -8))
    m.round_box(jb, 0, -10.0, 8.6, 4.0, 6.0, 12.0, fleshf, cut=2)                         # lower jaw
    m.box(hd, -7.6, 12.0, -14.2, 7.6, 18.0, -8.0, solid(P, "mouth"))
    for j in range(6):                                                                   # huge square teeth
        m.box(hd, -7.0 + j * 2.4, 15.0, -14.6, -5.2 + j * 2.4, 18.0, -13.0, solid(P, "tooth"))
        m.box(jb, -7.0 + j * 2.4, 12.0, -14.6, -5.2 + j * 2.4, 14.4, -13.0, solid(P, "tooth"))
    tb = m.bone("tentacles", bd, (0, 10, 12))
    for i in range(4):                                                                   # toothy tentacles
        ang = math.radians(-60 + i * 40)
        pts = [(6.0 * math.sin(ang), 10.0, 12.0), (14.0 * math.sin(ang), 6.0, 20.0), (20.0 * math.sin(ang), 4.0, 26.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, tb, p0, p1, 4, fleshf, extend=0.6)
        e = pts[-1]
        m.box(tb, e[0] - 1.6, e[1] - 0.6, e[2] + 1.6, e[0] + 1.6, e[1] + 0.6, e[2] + 2.2, solid(P, "mouth"))
        for f in range(3):
            spike(m, tb, (e[0] + (f - 1) * 1.0, e[1] + 0.6, e[2] + 2.0), (0, -1, 0), 0.8, 1.0, solid(P, "tooth"), tip=0.8)
    return m
