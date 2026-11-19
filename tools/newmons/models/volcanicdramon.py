"""Volcanicdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): an earth dragon of erupting fire: a lean charcoal-black dragon with glowing magma cracks,
a horned head, huge ragged wings of black and flame-orange feathers, fiery plumes streaming behind, and a long whip
tail ending in a burning cross blade. 35 blocks.

Front is -z, y is up. Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing
from _digidetail import feathers, metal, scales, solid
from _route import pal, tone

HEIGHT = 35
SCALE, HITBOX = sized(35, HEIGHT, 10.0)
KIND = "floater"
K = 3
LOOK = "a lean charcoal dragon with glowing magma cracks, huge ragged black-and-flame wings and a burning cross-bladed tail"
BASE = {"black": (50, 44, 44), "black_dark": (18, 14, 14), "magma": (255, 120, 30), "flame": (255, 170, 50, 210),
        "orange": (240, 120, 40), "red": (200, 40, 30), "eye": (255, 230, 90), "steel": (200, 204, 214)}
SHINY = {"black": (60, 60, 90), "black_dark": (20, 20, 40), "magma": (90, 200, 255), "flame": (120, 210, 255, 210),
         "orange": (80, 160, 240)}


def P(v):
    return pal(BASE, SHINY, v)


def hidef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(math.sin(x * 0.9 + z * 0.5) * math.cos(y * 0.7 - z * 0.3)) < 0.08:
        return p["magma"], p["magma"]
    return scales(P, "black", "black_dark", size=1.2)(x, y, z, face, variant, box=box, **k)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(x) > 18.0:
        return tone(p["orange"], face), p["orange"]
    return feathers(P, "black", "black_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("volcanicdramon")
    top = m.bone("volcanicdramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    ball(m, bd, (0, 22.0, 0), 4.6, hidef, layers=4, ry=6.0)
    nk = m.bone("neck", bd, (0, 26, -5))
    rod(m, nk, (0, 25.0, -5.0), (0, 30.0, -10.0), 2, hidef, extend=0.6)
    hd = m.bone("head", nk, (0, 30, -11))
    m.round_box(hd, 0, -14.0, 2.0, 3.6, 29.0, 32.4, hidef, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.1), 31.0, -16.4, max(sx * 1.0, sx * 2.1), 31.8, -15.8, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 1.4, 32.0, -11.0), (sx * 0.4, 0.6, 1), 1.0, 5.0, metal(P, "steel"), tip=0.8)
    for sx in (-1, 1):
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 3.0, 25.0, 0))
        feather_wing(m, wb, (sx * 3.0, 25.0, 0), 30.0, 14.0, 3, wingf, side=sx, sweep=20, droop=-4.0)
    fl = m.bone("plumes", bd, (0, 24, 4))
    for j in range(6):
        spike(m, fl, ((j - 2.5) * 1.6, 24.0, 4.0), ((j - 2.5) * 0.3, 0.6, 1), 1.6, 12.0, solid(P, "flame", glow=True),
              tip=0.8)
    tl = m.bone("tail", bd, (0, 19, 4))
    pts = [(0, 19.0, 4.0), (-2.0, 12.0, 4.0), (-6.0, 6.0, 2.0), (-10.0, 4.0, 0.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, hidef, extend=0.3)
    for ang in (0, 90):
        m.box(tl, -13.0, 3.4, -0.4, -7.0, 4.6, 0.4, solid(P, "magma", glow=True), rotation=(0, 0, ang + 45),
              pivot=(-10.0, 4.0, 0))
    return m
