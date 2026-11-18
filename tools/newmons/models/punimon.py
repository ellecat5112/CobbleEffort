"""Punimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a glossy red jelly blob with three stubby horn-ears on top and two big round black-and-white eyes
low on its face. 0.35 blocks.

Front is -z, y is up. 12 units tall; Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin
from _route import pal, tone

HEIGHT = 12
SCALE, HITBOX = sized(0.35, HEIGHT, 1.4)
KIND = "floater"
K = 4
LOOK = "a glossy red jelly blob with three stubby horn-ears and two big round black-and-white eyes"
BASE = {"red": (220, 40, 40), "red_dark": (150, 14, 14), "red_light": (250, 110, 110), "white": (255, 255, 255),
        "black": (20, 20, 24)}
SHINY = {"red": (60, 140, 220), "red_dark": (20, 80, 160), "red_light": (130, 190, 250)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "red", dark="red_dark", light="red_light", var=0.02)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.2, y - 4.6)
            if d < 0.55:
                return tone(p["black"], face), None
            if d < 1.0:
                return tone(p["white"], face), None
            if d < 1.3:
                return tone(p["black"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("punimon")
    top = m.bone("punimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    ball(m, bd, (0, 5.0, 0), 5.0, bodyf, layers=4, ry=4.4, squash=0.85)
    spike(m, bd, (0, 8.4, 0), (0, 1, 0), 2.0, 2.6, SKIN, tip=0.8)
    for sx in (-1, 1):
        spike(m, bd, (sx * 3.0, 7.6, 0), (sx * 0.5, 1, 0), 2.0, 2.6, SKIN, tip=0.8)
    return m
