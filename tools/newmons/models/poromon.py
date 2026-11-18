"""Poromon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a fluffy pale-pink bird head with big blue eyes, a yellow-and-green beak, two feathered wings
sprouting from its sides and a red-and-yellow plume on top. 0.5 blocks.

Front is -z, y is up. 16 units tall; Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, fan
from _digidetail import feathers, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.5, HEIGHT, 1.8)
KIND = "floater"
K = 3
LOOK = "a fluffy pale-pink bird head with big blue eyes, a yellow-green beak, two feathered wings and a red-and-yellow plume"
BASE = {"pink": (246, 210, 226), "pink_dark": (210, 150, 180), "eye": (60, 110, 200), "pupil": (20, 24, 40),
        "white": (255, 255, 255), "yellow": (250, 210, 60), "green": (110, 190, 70), "red": (220, 50, 40)}
SHINY = {"pink": (210, 230, 250), "pink_dark": (150, 180, 220)}


def P(v):
    return pal(BASE, SHINY, v)


FEATH = feathers(P, "pink", "pink_dark", size=(1.0, 1.6))


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot((x - sx * 2.0) * 0.9, y - 6.6)
            if d < 0.5:
                return tone(p["pupil"], face), None
            if d < 0.75 and x * sx > 2.0:
                return tone(p["white"], face), None
            if d < 1.3:
                return tone(p["eye"], face), None
    return FEATH(x, y, z, face, variant, box=box, **k)


def beakf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["green"] if y < 4.4 else p["yellow"], face), None


def build():
    m = Model("poromon")
    top = m.bone("poromon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 6.0, 0), 4.8, headf, layers=4, ry=4.4)
    spike(m, bd, (0, 4.6, -4.4), (0, -0.3, -1), 1.8, 2.4, beakf, tip=0.8)
    for sx in (-1, 1):
        fan(m, bd, (sx * 4.0, 7.0, 0.6), 4, 6.0, 1.6, 10, 60, FEATH, plane="xy", side=sx)
    spike(m, bd, (-0.6, 10.0, 0.4), (-0.2, 1, 0.2), 1.4, 4.0, solid(P, "red"), tip=0.8)
    spike(m, bd, (0.6, 10.0, 0.6), (0.3, 1, 0.3), 1.0, 3.0, solid(P, "yellow"), tip=0.8)
    return m
