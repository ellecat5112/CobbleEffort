"""Sunamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little mound of grey-green sand with two stubby grey horns, one sleepy yellow eye, a green bubble
blowing from its side and a trickle of sand spilling behind. 0.35 blocks.

Front is -z, y is up. 12 units tall; Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import noise2, solid
from _route import pal, tone

HEIGHT = 12
SCALE, HITBOX = sized(0.35, HEIGHT, 2.2)
KIND = "floater"
K = 4
LOOK = "a little mound of grey-green sand with two stubby grey horns, one sleepy yellow eye and a green bubble"
BASE = {"sand": (180, 180, 150), "sand_dark": (120, 120, 96), "horn": (130, 130, 136), "eye": (250, 210, 40),
        "black": (30, 30, 24), "bubble": (130, 230, 170, 200)}
SHINY = {"sand": (230, 200, 140), "sand_dark": (170, 140, 80)}


def P(v):
    return pal(BASE, SHINY, v)


def sandf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x - 1.0) < 1.6 and abs(y - 6.0) < 0.8:
        if y > 6.3:
            return tone(p["black"], face), None
        return tone(p["eye"], face), None
    return tone(p["sand"] if noise2(x * 0.8 + z * 0.6, y * 0.8, 3) < 0.6 else p["sand_dark"], face), None


def build():
    m = Model("sunamon")
    top = m.bone("sunamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    for i, (r, h) in enumerate(((7.0, 1.6), (5.6, 2.0), (4.4, 2.0), (3.0, 2.0))):          # sand mound
        y0 = sum(hh for _, hh in ((7.0, 1.6), (5.6, 2.0), (4.4, 2.0), (3.0, 2.0))[:i])
        m.round_box(bd, 0, 0.6, r, r * 0.8, y0, y0 + h + 0.2, sandf, cut=max(1, round(r * 0.35)))
    for sx in (-1, 1):
        spike(m, bd, (sx * 2.0, 7.4, 0), (sx * 0.3, 1, 0), 1.4, 2.6, solid(P, "horn"), tip=0.8)
    ball(m, bd, (-3.4, 4.0, -3.4), 1.2, solid(P, "bubble"), layers=1)
    for j in range(3):
        m.box(bd, 6.0 + j * 1.6, 0.0, 2.0, 7.0 + j * 1.6, 0.6, 3.0, sandf)
    return m
