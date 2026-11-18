"""Fluffymon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
Baby II puffball bird. A round ball of soft green down with a pale-yellow face, two big black eyes, a tiny beak, a
tuft of crest feathers on top and two stubby wing-tufts. Half a block tall.

Front is -z, y is up. 16 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.5, HEIGHT, 1.0)
KIND = "floater"
K = 4
LOOK = "a round ball of green down with a pale-yellow face, big black eyes, a tiny beak, a crest tuft and stubby wings"
BASE = {"green": (110, 200, 100), "green_dark": (50, 130, 50), "green_light": (200, 250, 180), "face": (250, 240, 170),
        "eye": (20, 20, 24), "shine": (250, 250, 250), "beak": (250, 170, 50)}
SHINY = {"green": (250, 170, 200), "green_dark": (200, 100, 140), "green_light": (255, 220, 240)}


def P(v):
    return pal(BASE, SHINY, v)


DOWN = fur(P, "green", "green_dark", tip="green_light", length=0.8, density=2.0)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and math.hypot(x, (y - 7.0) * 1.2) < 4.4:
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.8, y - 8.0)
            if d < 0.4:
                return tone(p["shine"], face), None
            if d < 1.2:
                return tone(p["eye"], face), None
        return tone(p["face"], face), None
    return DOWN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("fluffymon")
    top = m.bone("fluffymon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7, 0))
    ball(m, bd, (0, 7.0, 0), 6.4, bodyf, layers=5)
    hd = m.bone("head", bd, (0, 12, 0))
    spike(m, hd, (0, 6.4, -6.4), (0, -0.3, -1), 1.4, 1.6, solid(P, "beak"), tip=0.3)
    for j in range(3):
        spike(m, hd, ((j - 1) * 1.2, 13.0, 0.2), ((j - 1) * 0.4, 1, 0.3), 1.2, 3.6 - abs(j - 1), DOWN, tip=0.3)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 6.0, 7.0, 0))
        spike(m, ab, (sx * 5.8, 7.0, 0.4), (sx, -0.4, 0.3), 2.0, 2.6, DOWN, tip=0.6)
    return m
