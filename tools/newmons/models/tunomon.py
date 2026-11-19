"""Tunomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a fluffy orange ball with a white face, narrow red eyes and pink cheeks, and one big grey horn
curving up from its head. 0.5 blocks.

Front is -z, y is up. Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, fur, metal, plane, solid
from _route import pal, tone

HEIGHT = 15
SCALE, HITBOX = sized(0.5, HEIGHT, 1.2)
KIND = "biped"
K = 4
LOOK = "a fluffy orange ball with a white face, narrow red eyes, pink cheeks and one big grey horn"
BASE = {"orange": (250, 150, 40), "orange_dark": (200, 90, 20), "white": (252, 252, 252), "eye": (210, 40, 40),
        "pupil": (30, 10, 10), "pink": (250, 170, 180), "horn": (130, 130, 140), "horn_dark": (40, 40, 50)}
SHINY = {"orange": (120, 200, 90), "orange_dark": (60, 140, 40)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if z < -1.6 and y < 8.0:
        if face == "north":
            a, b = plane(x, y, z, face)
            for sx in (-1, 1):
                c = eye(p, a - sx * 2.0, b - 5.6, 0.9, "eye", slit=True)
                if c is not None:
                    return c, None
                if math.hypot(a - sx * 3.4, b - 4.2) < 0.8:
                    return p["pink"], None
        return tone(p["white"], face), None
    return fur(P, "orange", "orange_dark", length=1.0)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("tunomon")
    top = m.bone("tunomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 6.0, 0), 5.4, bodyf, layers=5, squash=0.85)
    spike(m, bd, (0, 10.0, -0.6), (0, 1, -0.25), 2.6, 9.0, metal(P, "horn", dark="horn_dark"), tip=0.8)
    return m
