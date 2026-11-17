"""Cotsucomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a baby under a helmet. A little round yellow blob with a zigzag grin peeking out from under a
big brown riveted round helmet with stitched seams, a steel knob on top and a chin strap. Baby I.

Front is -z, y is up. 18 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model
from _digi import sized
from _digibeast import ball
from _digidetail import leather, metal, skin, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.35, HEIGHT, 0.5)
KIND = "floater"
K = 4
LOOK = "a little round yellow blob with a zigzag grin peeking out from under a big brown riveted round helmet"
BASE = {"yellow": (250, 210, 60), "yellow_dark": (210, 160, 20), "brown": (150, 100, 50), "brown_dark": (90, 56, 24),
        "steel": (210, 214, 226), "steel_dark": (110, 114, 128), "mouth": (40, 30, 20), "strap": (40, 34, 30)}
SHINY = {"yellow": (180, 230, 250), "yellow_dark": (110, 180, 220), "brown": (70, 110, 70), "brown_dark": (30, 60, 30)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and 3.0 < y < 4.6 and abs(x) < 3.4:
        zig = 3.8 + 0.5 * abs(((x * 0.9) % 2) - 1)
        if abs(y - zig) < 0.25:
            return tone(p["mouth"], face), None
    return skin(P, "yellow", dark="yellow_dark", var=0.03)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("cotsucomon")
    top = m.bone("cotsucomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 5.0, 0), 4.6, bodyf, layers=4)
    hd = m.bone("head", bd, (0, 8, 0))
    HELM = leather(P, "brown", "brown_dark", stitch="steel")
    for r, y0, y1 in ((9.0, 7.0, 8.4), (7.4, 8.4, 11.0), (6.2, 11.0, 13.4), (4.4, 13.4, 15.0)):   # the helmet
        m.round_box(hd, 0, 0, r, r, y0, y1, HELM, cut=max(1, round(r * 0.35)))
    m.round_box(hd, 0, 0, 1.4, 1.4, 15.0, 16.6, metal(P, "steel", dark="steel_dark"), cut=1)   # knob
    for sx in (-1, 1):                                                                         # chin strap
        m.box(hd, min(sx * 4.4, sx * 4.8), 2.0, -0.6, max(sx * 4.4, sx * 4.8), 7.6, 0.6, solid(P, "strap"))
    return m
