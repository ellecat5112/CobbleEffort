"""Raptor Sparrowmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a mechanical bird of prey: a slim black-and-steel body, a gold-plated head and breast
with a sharp grey beak and a single blade crest, two great swept wings of steel feather-blades edged in gold and set
with green lenses, and long black talons trailing thin cable tails. 15 blocks.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a mechanical bird of prey with a gold head and breast, great swept wings of steel feather-blades with green lenses and long black talons"
BASE = {"black": (36, 36, 44), "black_dark": (12, 12, 16), "steel": (200, 204, 216), "steel_dark": (100, 104, 120),
        "gold": (230, 200, 90), "gold_dark": (150, 110, 30), "green": (90, 230, 120), "eye": (60, 200, 250)}
SHINY = {"gold": (220, 120, 200), "gold_dark": (140, 50, 120), "green": (250, 160, 60)}


def P(v):
    return pal(BASE, SHINY, v)


STEEL = metal(P, "steel", dark="steel_dark")
GOLD = armour(P, "gold", "gold_dark")
BLACK = armour(P, "black", "black_dark")


def build():
    m = Model("raptorsparrowmon")
    top = m.bone("raptorsparrowmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    m.round_box(bd, 0, 1.0, 3.0, 4.0, 18.0, 28.0, BLACK, cut=1)
    m.round_box(bd, 0, -2.6, 2.6, 1.6, 22.0, 30.0, GOLD, cut=1)                             # gold breast
    hd = m.bone("head", bd, (0, 30, -1))
    m.round_box(hd, 0, -1.4, 2.4, 2.8, 29.6, 35.0, GOLD, cut=1)
    spike(m, hd, (0, 32.0, -4.0), (0, -0.3, -1), 1.4, 4.0, STEEL, tip=0.8)
    spike(m, hd, (0, 35.0, -0.6), (0, 1, 0.5), 1.2, 6.0, STEEL, tip=0.8)                    # blade crest
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.3, sx * 2.5), 32.6, -3.0, max(sx * 2.3, sx * 2.5), 33.4, -1.8, solid(P, "eye", glow=True))
    for sx in (-1, 1):                                                                   # swept blade wings
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 3.0, 27.0, 1.0))
        rod(m, wb, (sx * 3.0, 27.0, 1.0), (sx * 14.0, 34.0, 4.0), 2, GOLD, extend=0.4)
        rod(m, wb, (sx * 14.0, 34.0, 4.0), (sx * 26.0, 42.0, 6.0), 1, GOLD, extend=0.4)
        ball(m, wb, (sx * 14.0, 34.0, 3.0), 1.2, solid(P, "green", glow=True), layers=1)
        for j in range(7):
            t = (j + 0.5) / 7
            p = (sx * (3.0 + 23.0 * t), 27.0 + 15.0 * t, 1.0 + 5.0 * t)
            spike(m, wb, p, (sx * 0.2, -1, 0.3), 1.6, 8.0 + 6.0 * t, STEEL, tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                                  # talons + cable tails
        lg = m.bone(nm, bd, (sx * 1.6, 18.0, 1.0))
        rod(m, lg, (sx * 1.6, 18.0, 1.0), (sx * 2.4, 10.0, -1.0), 1, BLACK, extend=0.2, t2=2)
        for f in range(3):
            spike(m, lg, (sx * 2.4 + (f - 1) * 0.8, 9.6, -1.4), ((f - 1) * 0.3, -0.6, -1), 0.8, 3.0, BLACK, tip=0.8)
    for j in range(3):
        pts = [(0, 18.0, 4.0), ((j - 1) * 2.0, 10.0, 10.0), ((j - 1) * 4.0, 3.0, 14.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, bd, p0, p1, 1, solid(P, "black"), extend=0.2, t2=1)
    return m
