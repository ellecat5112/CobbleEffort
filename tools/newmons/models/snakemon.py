"""Snakemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little purple snake coiled up, banded darker violet with pale scales on its belly, a hooded head
with a flicking red forked tongue, and a little bell on a cord round its neck. 1 block.

Front is -z, y is up. 16 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import scales, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(1, HEIGHT, 1.6)
KIND = "floater"
K = 3
LOOK = "a little purple snake coiled up, banded violet, with a hooded head, a flicking red forked tongue and a little bell"
BASE = {"purple": (140, 100, 190), "purple_dark": (70, 40, 120), "belly": (220, 200, 240), "red": (220, 40, 60),
        "eye": (250, 220, 60), "black": (24, 20, 28), "bell": (240, 200, 70)}
SHINY = {"purple": (80, 170, 110), "purple_dark": (30, 100, 50)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "down":
        return tone(p["belly"], face), None
    if (math.atan2(z, x) * 3 + y) % 2.4 < 0.7:
        return tone(p["purple_dark"], face), None
    return scales(P, "purple", "purple_dark", size=1.0)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("snakemon")
    top = m.bone("snakemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    for i in range(3):                                                                   # coils
        r = 4.0 - i * 1.0
        for j in range(12):
            ang = 2 * math.pi * j / 12
            m.round_box(bd, r * math.cos(ang), r * math.sin(ang) + 1.0, 1.4, 1.4, i * 2.4, i * 2.4 + 2.6, bodyf, cut=0)
    hd = m.bone("head", bd, (0, 8, -1))
    rod(m, hd, (0, 7.0, 0), (0, 11.0, -2.0), 2, bodyf, extend=0.4)
    m.round_box(hd, 0, -3.0, 2.4, 2.2, 10.6, 14.0, bodyf, cut=1)                             # hooded head
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 1.8), 12.6, -5.3, max(sx * 0.8, sx * 1.8), 13.4, -5.1, solid(P, "eye"))
    rod(m, hd, (0, 11.0, -5.0), (0, 10.0, -8.0), 1, solid(P, "red"), extend=0.1, t2=1)        # forked tongue
    for sx in (-1, 1):
        spike(m, hd, (0, 10.0, -8.0), (sx * 0.6, -0.2, -1), 0.8, 1.2, solid(P, "red"), tip=0.8)
    ball(m, hd, (0, 8.6, -2.6), 0.9, solid(P, "bell"), layers=1)
    return m
