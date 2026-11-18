"""Pusurimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a bigger fluffy grey-and-white fur-ball, black behind, winking one big teal eye with its mouth
wide open in a laugh, little paw nubs, cat-like ears, and a crown of yellow lightning-bolt spikes. 0.5 blocks.

Front is -z, y is up. 16 units tall; Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.5, HEIGHT, 1.8)
KIND = "floater"
K = 3
LOOK = "a fluffy grey-and-white fur-ball winking one teal eye with a laughing open mouth, cat ears and yellow bolt spikes"
BASE = {"grey": (210, 212, 222), "grey_dark": (40, 40, 46), "white": (250, 250, 252), "eye": (90, 200, 200),
        "pupil": (20, 30, 40), "yellow": (250, 210, 50), "mouth": (200, 60, 80), "black": (24, 24, 30)}
SHINY = {"grey": (240, 210, 150), "grey_dark": (120, 80, 40)}


def P(v):
    return pal(BASE, SHINY, v)


def furf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        d = math.hypot(x - 2.0, y - 6.6)
        if d < 0.6:
            return tone(p["pupil"], face), None
        if d < 1.3:
            return tone(p["eye"], face), None
        if abs(x + 2.0) < 1.2 and abs(y - 6.6 - 0.3 * abs(x + 2.0)) < 0.2:
            return tone(p["black"], face), None
        if 2.6 < y < 4.6 and abs(x) < 2.0 - (4.6 - y) * 0.6:
            return tone(p["mouth"], face), None
    if z > 2.0:
        return fur(P, "grey_dark", "grey_dark", length=1.0)(x, y, z, face, variant, box=box, **k)
    return fur(P, "grey", "grey_dark", length=1.0, density=1.4)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("pusurimon")
    top = m.bone("pusurimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    ball(m, bd, (0, 5.4, 0.6), 5.6, furf, layers=4, ry=5.0, squash=1.1)
    for sx in (-1, 1):
        spike(m, bd, (sx * 4.4, 8.0, -0.6), (sx * 0.8, 0.8, -0.2), 1.8, 2.6, furf, tip=0.8)
        spike(m, bd, (sx * 3.6, 1.0, -3.6), (sx * 0.3, -0.6, -1), 1.2, 1.6, furf, tip=0.8)
    for j in range(4):
        ang = math.radians(-50 + j * 33)
        spike(m, bd, (4.0 * math.sin(ang), 9.0 + 1.2 * math.cos(ang), 1.6), (math.sin(ang), math.cos(ang), 0.4),
              1.4, 4.0, solid(P, "yellow"), tip=0.8)
    return m
