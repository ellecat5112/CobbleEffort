"""Opossummon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Armor Digimon of joy: a little black-and-white opossum with long white ears, a red jester's
collar, big red gloves and shoes, a thin curling tail, drifting along under a bunch of smiling coloured balloons tied
with a red bow. 15 blocks tall.

Front is -z, y is up. 50 units tall (the balloons); Adult (Armor) stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, skin, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "a little black-and-white opossum with long ears, red gloves and shoes, drifting under a bunch of smiling coloured balloons"
BASE = {"black": (44, 42, 48), "black_dark": (16, 16, 20), "white": (246, 246, 246), "red": (220, 40, 40),
        "red_dark": (130, 14, 14), "eye": (60, 160, 90), "b1": (90, 190, 100), "b2": (240, 110, 70), "b3": (90, 120, 230),
        "b4": (250, 220, 70), "b5": (250, 160, 200), "string": (200, 200, 200)}
SHINY = {"black": (210, 190, 160), "black_dark": (150, 130, 100)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "black", "black_dark", length=1.0)


def build():
    m = Model("opossummon")
    top = m.bone("opossummon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 12.0, 0.4), 3.6, FUR, layers=4, ry=4.4)
    hd = m.bone("head", bd, (0, 17, 0))
    ball(m, hd, (0, 19.6, -0.4), 3.2, skin(P, "white", dark="black_dark"), layers=4, ry=2.8)
    for sx in (-1, 1):
        m.box(hd, sx * 1.2 - 0.5, 19.8, -3.65, sx * 1.2 + 0.5, 20.8, -3.5, solid(P, "eye"))
        spike(m, hd, (sx * 1.8, 21.6, 0.4), (sx * 0.5, 1, 0.3), 1.8, 7.0, skin(P, "white", dark="black_dark"), tip=0.8)
    for i in range(6):                                                                   # red jester collar
        ang = 2 * math.pi * i / 6
        spike(m, bd, (2.6 * math.cos(ang), 16.0, 2.6 * math.sin(ang)), (math.cos(ang), -0.4, math.sin(ang)), 1.2, 2.0,
              solid(P, "red"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.2, 14.0, 0))
        rod(m, ab, (sx * 3.2, 14.0, 0), (sx * 5.0, 18.0, -1.0) if sx > 0 else (sx * 6.0, 12.0, -1.0), 1, FUR, extend=0.2,
            t2=1)
        ball(m, ab, (sx * 5.2, 18.6, -1.2) if sx > 0 else (sx * 6.4, 11.4, -1.2), 1.4, skin(P, "red", dark="red_dark"),
             layers=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.6, 8.0, 0))
        rod(m, lg, (sx * 1.6, 9.0, 0), (sx * 2.0, 4.0, 0), 1, FUR, extend=0.2, t2=1)
        m.round_box(lg, sx * 2.0, -0.8, 1.2, 1.8, 2.4, 4.0, skin(P, "red", dark="red_dark"), cut=0)
    tb = m.bone("tail", bd, (0, 9, 3))
    pts = [(0, 9.0, 3.0), (1.0, 5.0, 4.0), (2.0, 3.0, 3.0), (3.0, 4.0, 2.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 1, solid(P, "black"), extend=0.1)
    bb = m.bone("balloons", bd, (5.2, 19.0, -1.2))                                       # balloon bunch
    m.box(bb, 4.6, 19.4, -1.8, 6.0, 20.4, -0.6, solid(P, "red"))
    for i, key in enumerate(("b1", "b2", "b3", "b4", "b5")):
        ang = math.radians(-60 + i * 30)
        c = (5.2 + 7.0 * math.sin(ang), 40.0 + 3.0 * math.cos(ang * 2), -1.2 + (i % 2) * 2.0)
        rod(m, bb, (5.2, 20.4, -1.2), (c[0], c[1] - 3.6, c[2]), 1, solid(P, "string"), extend=0.0, t2=1)
        ball(m, bb, c, 3.6, solid(P, key), layers=3, ry=4.0)
        m.box(bb, c[0] - 1.4, c[1] - 1.0, c[2] - 3.65, c[0] + 1.4, c[1] - 0.6, c[2] - 3.5, solid(P, "black"))
    return m
