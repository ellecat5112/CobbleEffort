"""Curimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a little cream blob baby with a broad flat-topped head swept up to one side, three red streaks along its
top edge, a red mark on its brow, two shiny black eyes and a tiny "w" mouth with a fang. Baby I.

Front is -z, y is up. 18 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.35, HEIGHT, 0.5)
KIND = "floater"
K = 4
LOOK = "a little cream blob baby with a broad head swept up to one side, red streaks along its top and shiny black eyes"
BASE = {"cream": (252, 246, 220), "cream_dark": (216, 204, 170), "red": (220, 60, 60), "eye": (24, 24, 30),
        "white": (255, 255, 255)}
SHINY = {"cream": (220, 236, 255), "cream_dark": (170, 190, 230), "red": (70, 120, 230)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "cream", dark="cream_dark", var=0.02)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.8, y - 5.6)
            if d < 1.2:
                return tone(p["white"] if math.hypot(x - sx * 2.8 + 0.4, y - 6.0) < 0.35 else p["eye"], face), None
        if abs(y - 3.6 - 0.25 * abs(math.sin(x * 2.2))) < 0.15 and abs(x) < 1.4:
            return tone(p["eye"], face), None
        if abs(x + 0.6) < 0.6 and 8.2 < y < 9.4:
            return tone(p["red"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("curimon")
    top = m.bone("curimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    for r, y0, y1 in ((7.6, 0.0, 1.6), (7.0, 1.6, 6.0), (6.0, 6.0, 8.6), (4.4, 8.6, 10.0)):
        m.round_box(bd, 0, 0, r, r * 0.84, y0, y1, bodyf, cut=max(1, round(r * 0.35)))
    hd = m.bone("head", bd, (2, 10, 0))                                      # the swept-up flat top
    for j in range(4):
        m.box(hd, -1.0 + j * 1.6, 9.0 + j * 2.0, -2.6, 4.0 + j * 1.6, 11.4 + j * 2.0, 2.6, SKIN)
    for j in range(3):                                                       # three red streaks
        spike(m, hd, (1.6 + j * 1.8, 12.6 + j * 2.0, 0), (0.4, 1, 0), 1.0, 2.0, solid(P, "red"), tip=0.3)
    return m
