"""Zurumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a little glossy yellow slime with sly slanted red eyes and a smirk, dripping into a trailing puddle of
goo and droplets behind it. 0.35 blocks.

Front is -z, y is up. Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model
from _digi import sized
from _digibeast import ball
from _digidetail import plane, skin, solid
from _route import pal, tone

HEIGHT = 11
SCALE, HITBOX = sized(0.35, HEIGHT, 1.8)
KIND = "biped"
K = 4
LOOK = "a little glossy yellow slime with slanted red eyes and a smirk, trailing a puddle of goo"
BASE = {"yellow": (250, 230, 60), "yellow_dark": (210, 170, 20), "eye": (200, 30, 30), "black": (40, 30, 10)}
SHINY = {"yellow": (150, 230, 90), "yellow_dark": (90, 170, 40)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            if 0.8 < sx * a < 3.0 and abs(b - 7.4 + (sx * a - 0.8) * 0.35) < 0.7:
                return p["eye"], p["eye"]
        if abs(b - 4.8 - 0.1 * (a + 1.0) ** 2) < 0.25 and -2.4 < a < 1.6:
            return p["black"], None
    return skin(P, "yellow", dark="yellow_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("zurumon")
    top = m.bone("zurumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 0, 0))
    ball(m, bd, (0, 6.2, 0), 5.0, bodyf, layers=5, squash=0.8)
    for j in range(4):
        ball(m, bd, (0.6 * math.sin(j), 2.6, 5.0 + j * 2.0), 2.4 - j * 0.5, skin(P, "yellow", dark="yellow_dark"),
             layers=1, squash=0.4)
    return m
