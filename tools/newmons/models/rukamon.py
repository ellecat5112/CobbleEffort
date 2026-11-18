"""Rukamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a blue dolphin-shark: a sleek blue body streaked darker, a white belly and jaw, a toothy grin with a
red scar, a green eye, a tall jagged dorsal fin, ragged pectoral fins and a forked tail fin. 15 blocks.

Front is -z, y is up. 30 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import slab_z
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "a sleek blue dolphin-shark streaked darker with a white belly, a toothy scarred grin, a green eye and jagged fins"
BASE = {"blue": (60, 120, 200), "blue_dark": (24, 60, 140), "white": (246, 248, 252), "white_dark": (200, 206, 220),
        "eye": (90, 200, 120), "mouth": (180, 50, 60), "tooth": (250, 250, 240), "scar": (220, 60, 60)}
SHINY = {"blue": (200, 90, 160), "blue_dark": (130, 30, 100)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "down" or (y < 12.0 and face == "north"):
        return skin(P, "white", dark="white_dark", var=0.02)(x, y, z, face, variant, box=box, **k)
    if abs(math.sin(z * 0.6 + y * 0.8)) > 0.9:
        return tone(p["blue_dark"], face), None
    return skin(P, "blue", dark="blue_dark", var=0.03)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("rukamon")
    top = m.bone("rukamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    for i in range(8):                                                                   # body slices, head to tail
        t = (i + 0.5) / 8
        r = 5.6 * math.sin(math.pi * (0.25 + 0.65 * t)) + 0.8
        slab_z(m, bd, 0, 16.0 - (t - 0.3) * 6.0 * (t > 0.3), -12.0 + i * 3.4, -12.0 + (i + 1) * 3.4 + 0.2, r * 0.8, r,
               bodyf)
    hd = m.bone("head", bd, (0, 16, -10))
    m.round_box(hd, 0, -15.0, 2.8, 3.0, 11.4, 16.6, bodyf, cut=1)                           # snout
    m.box(hd, -2.4, 12.6, -18.2, 2.4, 13.6, -10.0, solid(P, "mouth"))
    for j in range(5):
        for sx in (-1, 1):
            spike(m, hd, (sx * 2.2, 13.6, -17.4 + j * 1.6), (0, -1, 0), 0.8, 1.2, solid(P, "tooth"), tip=0.8)
    m.box(hd, 1.6, 13.8, -18.1, 3.0, 14.4, -17.8, solid(P, "scar"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 3.9, sx * 4.2), 17.0, -11.0, max(sx * 3.9, sx * 4.2), 18.0, -9.6, solid(P, "eye"))
    spike(m, bd, (0, 22.0, -2.0), (0, 1, 0.6), 2.6, 10.0, bodyf, tip=0.8)                   # tall dorsal fin
    spike(m, bd, (0, 24.0, 2.0), (0, 0.8, 1), 1.2, 4.0, bodyf, tip=0.8)
    for sx in (-1, 1):
        spike(m, bd, (sx * 4.0, 12.0, -4.0), (sx * 0.8, -0.6, 0.4), 2.0, 7.0, bodyf, tip=0.8)   # pectoral fins
        spike(m, bd, (0, 12.0, 14.0), (0, sx * 0.9, 0.6), 2.0, 7.0, bodyf, tip=0.8)          # forked tail fin
    return m
