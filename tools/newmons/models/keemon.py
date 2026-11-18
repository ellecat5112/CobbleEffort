"""Keemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
Baby I glossy purple cat-shaped slime with two pointed ears, grumpy half-lidded eyes and a tiny frown, puffing out
little clouds. A third of a block tall.

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
LOOK = "a glossy purple cat-shaped slime with pointed ears, grumpy half-lidded eyes and a tiny frown"
BASE = {"purple": (100, 70, 200), "purple_dark": (50, 30, 120), "purple_light": (190, 170, 250), "eye": (24, 20, 30),
        "white": (250, 250, 250), "mouth": (30, 20, 40), "cloud": (240, 244, 250)}
SHINY = {"purple": (240, 160, 60), "purple_dark": (170, 90, 20), "purple_light": (255, 230, 170)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 2.0) < 1.0 and 5.0 < y < 6.4:
                return tone(p["eye"] if y < 5.8 else p["purple_dark"], face), None
        if abs(y - 3.6 + 0.2 * abs(x)) < 0.2 and abs(x) < 1.0:
            return tone(p["mouth"], face), None
    return skin(P, "purple", dark="purple_dark", light="purple_light")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("keemon")
    top = m.bone("keemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 5.4, 0), 5.0, bodyf, layers=4, squash=0.85)
    hd = m.bone("head", bd, (0, 9, 0))
    for sx in (-1, 1):
        spike(m, hd, (sx * 3.0, 8.4, 0.4), (sx * 0.6, 1, 0.2), 2.4, 4.0, skin(P, "purple", dark="purple_dark"), tip=0.8)
    m.round_box(hd, -6.4, 0, 1.2, 1.0, 9.0, 11.0, solid(P, "cloud"), cut=0)                    # little puffs
    m.round_box(hd, 6.6, 0, 1.0, 0.8, 4.0, 5.6, solid(P, "cloud"), cut=0)
    return m
