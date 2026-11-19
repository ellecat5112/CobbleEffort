"""Velgrmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the beast spirit of wind turned dark: a crimson demon bird with a horned beaked head and a ragged
gold crest, great black wings banded with red, a skeletal segmented tail, and long taloned crimson legs. 15 blocks.

Front is -z, y is up. Adult stage (Hybrid).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing
from _digidetail import armour, feathers, metal, solid, strands
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a crimson demon bird with a horned beaked head, a gold crest, black wings banded with red and a skeletal tail"
BASE = {"crimson": (170, 30, 40), "crimson_dark": (90, 10, 16), "black": (40, 36, 44), "black_dark": (12, 10, 14),
        "gold": (240, 200, 70), "gold_dark": (180, 130, 30), "eye": (250, 230, 60), "horn": (230, 200, 140)}
SHINY = {"crimson": (40, 110, 170), "crimson_dark": (16, 50, 100)}


def P(v):
    return pal(BASE, SHINY, v)


CRIMSON = armour(P, "crimson", "crimson_dark", panel=(2.4, 2.4))


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(x) % 6.0 < 1.2:
        return tone(p["crimson"], face), None
    return feathers(P, "black", "black_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("velgrmon")
    top = m.bone("velgrmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    ball(m, bd, (0, 19.0, 0), 4.4, CRIMSON, layers=4, ry=5.4)
    hd = m.bone("head", bd, (0, 23, -5))
    m.round_box(hd, 0, -6.0, 2.4, 3.0, 22.0, 26.0, CRIMSON, cut=1)
    spike(m, hd, (0, 23.0, -9.0), (0, -0.4, -1), 1.8, 4.0, metal(P, "horn"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.5), 24.6, -8.4, max(sx * 1.0, sx * 2.5), 25.4, -8.0, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.0, 26.0, -4.0), (sx * 0.4, 0.6, 1), 1.0, 4.0, metal(P, "horn"), tip=0.8)
    for j in range(6):
        spike(m, hd, ((j - 2.5) * 0.7, 26.0, -5.0), ((j - 2.5) * 0.3, 0.8, 0.8), 1.0, 5.0, strands(P, "gold", "gold_dark"),
              tip=0.8)
    for sx in (-1, 1):
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 3.0, 21.0, 0))
        feather_wing(m, wb, (sx * 3.0, 21.0, 0), 26.0, 11.0, 3, wingf, side=sx, sweep=15, droop=-8.0)
    tl = m.bone("tail", bd, (0, 17, 4))
    for i in range(7):                                                                 # skeletal tail
        c = (0, 17.0 - i * 1.0, 5.0 + i * 2.2)
        ball(m, tl, c, 1.0, CRIMSON, layers=1)
        for sx in (-1, 1):
            spike(m, tl, c, (sx, 0.2, 0), 0.8, 1.6, CRIMSON, tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, bd, (sx * 2.0, 15.0, 0))
        rod(m, lg, (sx * 2.0, 15.0, 0), (sx * 3.0, 8.0, 1.0), 1, CRIMSON, extend=0.3)
        rod(m, lg, (sx * 3.0, 8.0, 1.0), (sx * 3.4, 2.0, -1.0), 1, CRIMSON, extend=0.3)
        for t in range(3):
            spike(m, lg, (sx * 3.4, 1.6, -1.0), ((t - 1) * 0.6, -0.4, -1), 0.8, 3.0, CRIMSON, tip=0.8)
    return m
