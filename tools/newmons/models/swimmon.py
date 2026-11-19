"""Swimmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a tropical piranha-fish: a deep-bodied green fish splashed with red and orange marks and yellow spots,
a big yellow eye, a gaping red-lipped mouth of fangs with a pink tongue, a dark strap round its snout, and long
translucent rainbow-tinted fins. 1 block. Child stage.

Front is -z, y is up. 24 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import slab_z
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(1, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "a deep-bodied green tropical piranha splashed red and orange with a big yellow eye, a fanged red-lipped mouth and rainbow fins"
BASE = {"green": (80, 170, 100), "green_dark": (30, 100, 50), "red": (210, 50, 40), "orange": (250, 150, 40),
        "yellow": (250, 220, 60), "black": (30, 26, 24), "pink": (240, 140, 160), "tooth": (250, 250, 240),
        "fin": (200, 230, 180, 170), "strap": (60, 50, 50)}
SHINY = {"green": (80, 120, 210), "green_dark": (30, 60, 150)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        if math.hypot(z + 4.0, y - 14.0) < 1.6:
            return tone(p["black"] if math.hypot(z + 4.0, y - 14.0) < 0.7 else p["yellow"], face), None
        if abs(math.sin(z * 0.9 + y * 0.5)) > 0.94:
            return tone(p["red"], face), None
        if math.sin(z * 1.7) * math.sin(y * 1.6) > 0.85:
            return tone(p["yellow"], face), None
    return skin(P, "green", dark="green_dark", var=0.03)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("swimmon")
    top = m.bone("swimmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    for i in range(6):                                                                   # deep body
        t = (i + 0.5) / 6
        h = 7.0 * math.sin(math.pi * (0.2 + 0.7 * t)) + 1.0
        slab_z(m, bd, 0, 12.0, -6.0 + i * 2.6, -6.0 + (i + 1) * 2.6 + 0.2, 2.6, h, bodyf)
    m.box(bd, -2.4, 9.0, -7.6, 2.4, 12.0, -5.6, solid(P, "red"))                              # gaping mouth
    for j in range(4):
        spike(m, bd, (-1.6 + j * 1.1, 12.0, -7.4), (0, -1, 0), 0.8, 1.4, solid(P, "tooth"), tip=0.8)
        spike(m, bd, (-1.6 + j * 1.1, 9.0, -7.4), (0, 1, 0), 0.8, 1.2, solid(P, "tooth"), tip=0.8)
    m.box(bd, -2.6, 12.6, -6.4, 2.6, 13.6, -4.6, solid(P, "strap"))
    spike(m, bd, (0, 19.0, 0), (0, 1, 0.8), 1.6, 8.0, solid(P, "fin"), tip=0.8)              # long fins
    for sx in (-1, 1):
        spike(m, bd, (sx * 2.4, 8.0, 0), (sx * 0.4, -1, 0.6), 1.4, 10.0, solid(P, "fin"), tip=0.8)
        spike(m, bd, (0, 12.0, 9.0), (0, sx * 0.6, 1), 1.6, 8.0, solid(P, "fin"), tip=0.8)
    return m
