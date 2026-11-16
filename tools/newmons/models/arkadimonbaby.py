"""Arkadimon Baby (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
a glossy grey droplet with a long curled tail-tip, cruel slanted red eyes and four jointed steel spider legs.
Tiny.

Front is -z, y is up. 26 units tall; Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _digi import sized
from _digibeast import ball
from _arkadi import GREY, P
from _digidetail import plane
from _route import tone

HEIGHT = 26
SCALE, HITBOX = sized(0.5, HEIGHT, 0.45)
KIND = "floater"
K = 4
LOOK = "a glossy grey droplet with a curled tail-tip, slanted red eyes and four jointed steel spider legs"


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            du, dv = a - sx * 2.6, (b - 10.0) + 0.5 * sx * (a - sx * 2.6)
            if abs(du) < 1.8 and abs(dv) < 0.55 - 0.2 * abs(du):
                return p["red"], p["red"]
    return GREY(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("arkadimonbaby")
    top = m.bone("arkadimonbaby", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, (0, 10.0, 0), 6.4, bodyf, layers=6, squash=0.9)
    tl = m.bone("tail", bd, (0, 15, 1))                          # the curled tail-tip
    pts = [(0, 15.0, 1.0), (0.6, 19.0, 2.4), (0.4, 22.0, 1.0), (-0.6, 24.0, -1.4), (-2.6, 24.6, -2.4),
           (-4.0, 23.0, -2.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, max(1, 5 - j), GREY, extend=0.4)
    for i, (sx, sz) in enumerate(((1, -1), (-1, -1), (1, 1), (-1, 1))):
        nm = f"leg_{'front' if sz < 0 else 'back'}_{'left' if sx > 0 else 'right'}"
        lg = m.bone(nm, top, (sx * 4.6, 7.0, sz * 3.0))
        knee = (sx * 9.0, 9.0, sz * 4.6)
        foot = (sx * 10.0, 0.6, sz * 6.0)
        rod(m, lg, (sx * 4.6, 7.0, sz * 3.0), knee, 1, GREY, extend=0.3)
        rod(m, lg, knee, foot, 1, GREY, extend=0.3)
        rod(m, lg, foot, (foot[0] + sx * 1.2, 0.2, foot[2] + sz * 1.2), 1, GREY, extend=0.2)
    return m
