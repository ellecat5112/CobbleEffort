"""Ketomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
Baby I glossy blue teardrop of a fish with two big round yellow eyes, yellow diamond marks on its brow and dorsal
peak, and a little forked tail fin. A third of a block tall.

Front is -z, y is up. 14 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 14
SCALE, HITBOX = sized(0.35, HEIGHT, 1.0)
KIND = "floater"
K = 4
LOOK = "a glossy blue teardrop fish with big round yellow eyes, yellow diamond marks and a little forked tail"
BASE = {"blue": (80, 120, 230), "blue_dark": (30, 60, 160), "blue_light": (170, 200, 255), "yellow": (250, 220, 60),
        "eye": (20, 20, 24), "white": (255, 255, 255)}
SHINY = {"blue": (230, 100, 120), "blue_dark": (160, 40, 60), "blue_light": (255, 190, 200)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.2, y - 4.4)
            if math.hypot(x - sx * 2.2 + 0.4, y - 5.0) < 0.35:
                return tone(p["white"], face), None
            if d < 0.8:
                return tone(p["eye"], face), None
            if d < 1.5:
                return tone(p["yellow"], face), None
        if abs(x - 0.6) + abs(y - 7.8) * 0.7 < 1.0:
            return tone(p["yellow"], face), None
    return skin(P, "blue", dark="blue_dark", light="blue_light")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("ketomon")
    top = m.bone("ketomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 5.0, 0), 4.8, bodyf, layers=4, squash=0.85)
    hd = m.bone("head", bd, (0, 9, 0))
    spike(m, hd, (0.6, 8.0, 1.0), (0.3, 1, 0.5), 3.0, 6.0, skin(P, "blue", dark="blue_dark"), tip=0.8)   # dorsal peak
    spike(m, hd, (0.9, 10.0, 1.8), (0.3, 1, 0.5), 1.2, 2.0, solid(P, "yellow"), tip=0.8)
    tb = m.bone("tail", bd, (0, 4, 4))
    for sy in (-1, 1):
        spike(m, tb, (0, 3.6, 4.0), (0.3, sy * 0.6, 1), 1.6, 4.0, skin(P, "blue", dark="blue_dark"), tip=0.8)
    return m
