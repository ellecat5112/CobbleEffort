"""Torikara Ballmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a little round golden-brown fried-chicken bird: a crumbly crust body with dot eyes and a
puckered beak, a three-lobed crest, stubby rounded wings and a tiny dark tail tuft. 0.5 blocks.

Front is -z, y is up. Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fbm, plane, solid
from _route import pal, tone

HEIGHT = 17
SCALE, HITBOX = sized(0.5, HEIGHT, 1.8)
KIND = "floater"
K = 4
LOOK = "a little round golden-brown fried-chicken bird with a crumbly crust, dot eyes, a three-lobed crest and stubby wings"
BASE = {"crust": (200, 160, 80), "crust_dark": (150, 104, 40), "eye": (24, 16, 10), "beak": (120, 80, 40),
        "tail": (60, 40, 30)}
SHINY = {"crust": (220, 200, 160), "crust_dark": (170, 140, 100)}


def P(v):
    return pal(BASE, SHINY, v)


def crustf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            if math.hypot(a - sx * 2.0, b - 9.0) < 0.6:
                return p["eye"], None
        if math.hypot(a, b - 7.4) < 0.7:
            return p["beak"], None
    t = fbm(x * 0.9, y * 0.9, z * 0.9, seed=3)
    c = tuple(int(p["crust"][i] * (1 - t * 0.5) + p["crust_dark"][i] * t * 0.5) for i in range(3))
    return tone(c, face), None


def build():
    m = Model("torikaraballmon")
    top = m.bone("torikaraballmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 8.0, 0), 6.0, crustf, layers=6, squash=0.9)
    for j in range(3):                                                                 # three-lobed crest
        ball(m, bd, ((j - 1) * 1.6, 14.6 + (1 - abs(j - 1)) * 0.8, 0), 1.6, crustf, layers=2)
    for sx in (-1, 1):                                                                 # stubby wings
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 5.0, 9.0, 0))
        for j in range(3):
            ball(m, wb, (sx * (6.6 + j * 1.6), 9.0 + j * 1.0, 0), 2.2 - j * 0.3, crustf, layers=1)
    spike(m, bd, (0, 3.6, 4.0), (0, -0.6, 1), 1.0, 2.0, solid(P, "tail"), tip=0.8)
    return m
