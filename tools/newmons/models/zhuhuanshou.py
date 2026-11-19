"""Zhuhuanshou (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after an anime
still on wikimon.net): a crested bird of the Shou: a pale grey-white bird with great fanned wings edged black, a long
pale beak with a red crest stripe, small clawed orange feet, and two long ribbon tail feathers of black tipped red. 15
blocks.

Front is -z, y is up. Adult stage (by analogy: wikimon gives no level).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing
from _digidetail import eye, feathers, metal, solid
from _route import pal, tone

HEIGHT = 41
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a pale grey-white crested bird with great black-edged fanned wings, a long pale beak with a red stripe and two long ribbon tail feathers"
BASE = {"white": (230, 228, 222), "white_dark": (170, 166, 156), "black": (40, 40, 44), "red": (200, 40, 40),
        "beak": (230, 220, 200), "orange": (230, 150, 60), "eye": (80, 60, 50), "pupil": (10, 10, 10)}
SHINY = {"white": (220, 200, 240), "white_dark": (160, 130, 190), "red": (60, 140, 220)}


def P(v):
    return pal(BASE, SHINY, v)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(x) > 20.0:
        return tone(p["black"], face), None
    return feathers(P, "white", "white_dark")(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 6.4, y - 28.0, 0.7, "eye")
        if c is not None:
            return c, None
    if face == "up" and abs(x) < 0.6:
        return tone(p["red"], face), None
    return feathers(P, "white", "white_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("zhuhuanshou")
    top = m.bone("zhuhuanshou", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    ball(m, bd, (0, 21.0, 0), 4.6, feathers(P, "white", "white_dark"), layers=4, ry=6.0)
    hd = m.bone("head", bd, (0, 26, -3))
    ball(m, hd, (0, 28.0, -4.0), 2.8, headf, layers=3)
    spike(m, hd, (0, 27.6, -6.6), (0, -0.6, -1), 1.4, 7.0, metal(P, "beak"), tip=0.8)
    spike(m, hd, (0, 30.4, -3.0), (0, 1, 0.8), 0.9, 5.0, solid(P, "red"), tip=0.8)
    for sx in (-1, 1):
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 3.0, 24.0, 0))
        feather_wing(m, wb, (sx * 3.0, 24.0, 0), 26.0, 12.0, 3, wingf, side=sx, sweep=-20, droop=-14.0)
        lg = m.bone("leg_" + ("left" if sx > 0 else "right"), bd, (sx * 1.6, 16.0, 0))
        rod(m, lg, (sx * 1.6, 16.0, 0), (sx * 2.0, 10.0, -1.0), 1, solid(P, "orange"), extend=0.3)
        for t in range(3):
            spike(m, lg, (sx * 2.0, 10.0, -1.0), ((t - 1) * 0.5, -0.6, -1), 0.8, 2.0, solid(P, "orange"), tip=0.8)
    tl = m.bone("tail", bd, (0, 17, 4))
    for sx in (-1, 1):                                                                  # ribbon tail feathers
        pts = [(sx * 0.6, 17.0, 4.0), (sx * 3.0, 10.0, 8.0), (sx * 6.0, 4.0, 8.0), (sx * 8.0, 1.0, 6.0)]
        for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, tl, p0, p1, 1, solid(P, "red" if i == 2 else "black"), extend=0.2, t2=2)
    return m
