"""Fufumon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
Baby I wisp. A soft apricot-orange teardrop blob with a curling tail, big round black-green eyes, a little smile and a
red cone horn on top. 0.35 blocks tall.

Front is -z, y is up. 12 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 12
SCALE, HITBOX = sized(0.35, HEIGHT, 1.0)
KIND = "floater"
K = 4
LOOK = "a soft apricot-orange teardrop blob with a curling tail, big round eyes, a little smile and a red cone horn"
BASE = {"orange": (250, 190, 90), "orange_dark": (210, 140, 50), "red": (220, 50, 40), "eye": (20, 40, 30),
        "shine": (250, 250, 250), "mouth": (120, 60, 40)}
SHINY = {"orange": (250, 220, 120), "orange_dark": (210, 170, 70), "red": (80, 120, 230)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "orange", dark="orange_dark")


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.6, y - 7.4)
            if d < 0.35:
                return tone(p["shine"], face), None
            if d < 0.95:
                return tone(p["eye"], face), None
        if abs(y - 5.8 + 0.2 * x * x) < 0.25 and abs(x) < 1.0:
            return tone(p["mouth"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("fufumon")
    top = m.bone("fufumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 6.4, 0), 4.4, bodyf, layers=4)
    hd = m.bone("head", bd, (0, 10, 0))
    spike(m, hd, (-1.0, 10.0, 0), (-0.3, 1, 0), 1.6, 3.0, solid(P, "red"), tip=0.2)
    tb = m.bone("tail", bd, (0, 3, 2))
    pts = [(0, 3.0, 2.0), (1.0, 1.0, 4.0), (2.4, 0.4, 5.6), (3.4, 1.4, 6.4)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tb, p0, p1, 1, SKIN, extend=0.3, t2=max(1, 3 - j))
    return m
