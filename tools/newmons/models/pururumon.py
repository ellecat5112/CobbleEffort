"""Pururumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a soft pink blob of a baby bird lying low, with a big yellow beak, small black eyes and a
little rounded tail. 0.35 blocks.

Front is -z, y is up. 10 units tall; Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 10
SCALE, HITBOX = sized(0.35, HEIGHT, 2.0)
KIND = "floater"
K = 4
LOOK = "a soft pink baby-bird blob lying low with a big yellow beak and small black eyes"
BASE = {"pink": (246, 200, 214), "pink_dark": (220, 150, 176), "yellow": (250, 200, 60), "black": (20, 20, 24),
        "white": (255, 255, 255), "blush": (250, 160, 170)}
SHINY = {"pink": (200, 236, 250), "pink_dark": (150, 196, 230)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west"):
        for sx in (-1, 1):
            if math.hypot(x - sx * 2.6, y - 4.6) < 0.7:
                return tone(p["black"], face), None
    return skin(P, "pink", dark="pink_dark", var=0.02)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("pururumon")
    top = m.bone("pururumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 4.0, 1.6), 4.4, bodyf, layers=3, ry=3.6, squash=1.4)
    spike(m, bd, (0, 3.6, -3.6), (0, -0.2, -1), 2.2, 2.6, solid(P, "yellow"), tip=0.8)
    spike(m, bd, (0, 4.0, 7.6), (0, 0.3, 1), 1.6, 1.6, skin(P, "pink", dark="pink_dark"), tip=0.8)
    return m
