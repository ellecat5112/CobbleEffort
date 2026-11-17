"""Chikurimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a living naval mine. A round gunmetal ball bristling with long sharp spikes, two round red
lenses for eyes. Child stage.

Front is -z, y is up. 26 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, solid
from _route import pal, tone

HEIGHT = 26
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "floater"
K = 4
LOOK = "a round gunmetal mine ball bristling with long sharp spikes, with two round red lens eyes"
BASE = {"steel": (110, 112, 124), "steel_dark": (50, 52, 60), "steel_light": (190, 194, 206), "lens": (220, 40, 40),
        "lens_ring": (230, 230, 236), "pupil": (40, 10, 10)}
SHINY = {"steel": (200, 170, 90), "steel_dark": (130, 100, 30), "steel_light": (250, 230, 160), "lens": (60, 200, 120)}


def P(v):
    return pal(BASE, SHINY, v)


STEEL = metal(P, "steel", dark="steel_dark", light="steel_light")


def ballf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.4, y - 12.0)
            if d < 1.8:
                c = p["lens_ring"] if d > 1.4 else p["pupil"] if d < 0.5 else p["lens"]
                return tone(c, face), None
    return STEEL(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("chikurimon")
    top = m.bone("chikurimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    ball(m, bd, (0, 12.0, 0), 6.4, ballf, layers=6)
    dirs = [(0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0.7, 0.7, 0.3), (-0.7, 0.7, 0.3),
            (0.7, -0.7, 0.3), (-0.7, -0.7, 0.3), (0.6, 0.3, 0.8), (-0.6, 0.3, 0.8), (0, 0.7, -0.7), (0, -0.7, -0.7),
            (0.9, 0.2, -0.4), (-0.9, 0.2, -0.4)]
    for d in dirs:
        n = math.sqrt(sum(c * c for c in d))
        u = tuple(c / n for c in d)
        spike(m, bd, (u[0] * 5.6, 12.0 + u[1] * 5.6, u[2] * 5.6), u, 2.0, 6.0, STEEL, tip=0.4)
    return m
