"""Orochimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the eight-headed serpent: a coiled mass of black scaled serpent bodies, eight snake heads armoured
in silver helms with red eyes rising and lunging in every direction, a shaggy straw-yellow mane at their roots, and a
long black tail ending in a ringed tip. 25 blocks long.

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, scales, solid, strands
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = ("a coiled mass of black serpent bodies with eight silver-helmed snake heads rising in every direction, a straw-"
        "yellow mane at their roots and a long ringed tail")
BASE = {"black": (50, 50, 56), "black_dark": (16, 16, 20), "silver": (200, 204, 216), "silver_dark": (100, 104, 116),
        "straw": (230, 200, 100), "straw_dark": (170, 130, 40), "red": (220, 40, 40), "belly": (150, 140, 120),
        "tooth": (250, 250, 240)}
SHINY = {"black": (200, 200, 210), "black_dark": (130, 130, 140), "silver": (230, 190, 80), "silver_dark": (160, 120, 30)}


def P(v):
    return pal(BASE, SHINY, v)


SC = scales(P, "black", "black_dark", size=1.4)
HELM = armour(P, "silver", "silver_dark", trim="red", trim_w=0.2)


def build():
    m = Model("orochimon")
    top = m.bone("orochimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    for i in range(10):                                                                  # coiled mass
        ang = 2 * math.pi * i / 10
        ball(m, bd, (6.0 * math.cos(ang), 6.0 + (i % 3) * 2.0, 6.0 * math.sin(ang)), 4.0, SC, layers=3)
    for i in range(12):                                                                  # straw mane
        ang = 2 * math.pi * i / 12
        spike(m, bd, (3.0 * math.cos(ang), 14.0, 3.0 * math.sin(ang)), (math.cos(ang), 0.6, math.sin(ang)), 2.0, 6.0,
              strands(P, "straw", "straw_dark"), tip=0.8)
    for i in range(8):                                                                   # eight helmed heads
        ang = 2 * math.pi * i / 8 + 0.2
        hb = m.bone("head_%d" % i, bd, (2.0 * math.cos(ang), 14.0, 2.0 * math.sin(ang)))
        reach = 14.0 + (i % 3) * 3.0
        rise = 14.0 + (i % 4) * 4.0
        p0 = (2.0 * math.cos(ang), 14.0, 2.0 * math.sin(ang))
        p1 = (reach * 0.6 * math.cos(ang), rise, reach * 0.6 * math.sin(ang) - 2.0)
        p2 = (reach * math.cos(ang), rise + 4.0, reach * math.sin(ang) - 4.0)
        rod(m, hb, p0, p1, 3, SC, extend=0.5)
        rod(m, hb, p1, p2, 3, SC, extend=0.5)
        m.round_box(hb, p2[0], p2[2] - 1.6, 2.0, 3.0, p2[1] - 1.0, p2[1] + 1.8, HELM, cut=1)
        for sx in (-1, 1):
            m.box(hb, p2[0] + min(sx * 2.0, sx * 2.2), p2[1] + 0.6, p2[2] - 3.0, p2[0] + max(sx * 2.0, sx * 2.2),
                  p2[1] + 1.2, p2[2] - 2.2, solid(P, "red", glow=True))
        spike(m, hb, (p2[0], p2[1] - 1.0, p2[2] - 4.4), (0, -1, 0), 0.8, 1.2, solid(P, "tooth"), tip=0.8)
    tb = m.bone("tail", bd, (0, 4, 8))
    pts = [(0, 4.0, 8.0), (4.0, 2.0, 16.0), (10.0, 2.0, 22.0), (16.0, 4.0, 26.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 2, SC, extend=0.4)
    for j in range(4):                                                                   # ringed tail tip
        e = pts[-1]
        m.round_box(tb, e[0] + j * 0.8, e[2] + j * 0.6, 1.2 - j * 0.2, 1.2 - j * 0.2, e[1] + j * 0.6, e[1] + j * 0.6 + 0.5,
                    solid(P, "black_dark"), cut=0)
    return m
