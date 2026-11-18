"""Rootmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a parasitic seed: an olive-green teardrop body with one huge red cross-pupilled eye, a little horn on
top, a mouth of tiny fangs, and long curling black root-tentacles striped red trailing beneath. 0.35 blocks.

Front is -z, y is up. 16 units tall; Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.35, HEIGHT, 1.6)
KIND = "floater"
K = 4
LOOK = "an olive-green teardrop seed with one huge red cross-pupilled eye, a little horn and curling black root-tentacles striped red"
BASE = {"olive": (110, 130, 70), "olive_dark": (60, 76, 30), "red": (210, 30, 40), "black": (24, 20, 20),
        "white": (250, 250, 240), "tooth": (250, 250, 240)}
SHINY = {"olive": (150, 90, 160), "olive_dark": (90, 40, 100)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        d = math.hypot(x, y - 9.4)
        if d < 2.4:
            if (abs(x) < 0.3 or abs(y - 9.4) < 0.3) and d < 1.6:
                return tone(p["black"], face), None
            return tone(p["red"] if d < 2.0 else p["black"], face), None
    return skin(P, "olive", dark="olive_dark", var=0.04)(x, y, z, face, variant, box=box, **k)


def rootf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["red"] if (y % 2.0) < 0.5 else p["black"], face), None


def build():
    m = Model("rootmon")
    top = m.bone("rootmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 9.0, 0), 3.8, bodyf, layers=4, ry=3.8)
    spike(m, bd, (0, 12.4, 0.4), (0.2, 1, 0.2), 1.4, 3.0, skin(P, "olive", dark="olive_dark"), tip=0.8)
    for j in range(4):
        spike(m, bd, (-1.2 + j * 0.8, 6.4, -3.0), (0, -1, 0), 0.8, 1.0, solid(P, "tooth"), tip=0.8)
    for sx in (-1, 1):                                                                   # root-tentacles
        pts = [(sx * 1.4, 6.0, 0), (sx * 3.0, 3.0, -0.6), (sx * 2.0, 0.6, -1.0), (sx * 4.0, 0.4, -1.6)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, bd, p0, p1, 1, rootf, extend=0.2, t2=1)
    return m
