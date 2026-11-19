"""Sandiramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the serpent of the Twelve Devas: a great cobra coiled in white rings, its spread hood a dome of
violet plate edged in gold and studded with silver scale-plates, a white horned mask of a face with a gaping red maw
and forked tongue. 25 blocks.

Front is -z, y is up. 44 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, skin, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a great cobra coiled in white rings with a spread violet-and-gold hood studded with silver scales and a white horned mask"
BASE = {"white": (246, 248, 252), "white_dark": (190, 200, 220), "violet": (110, 70, 170), "violet_dark": (50, 26, 100),
        "gold": (230, 190, 70), "gold_dark": (150, 100, 20), "silver": (200, 204, 216), "silver_dark": (110, 114, 130),
        "mouth": (180, 30, 50), "green": (60, 160, 90), "eye": (200, 40, 160)}
SHINY = {"violet": (60, 140, 90), "violet_dark": (20, 80, 40), "white": (240, 230, 200), "white_dark": (190, 170, 130)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = skin(P, "white", dark="white_dark", var=0.02)
HOOD = armour(P, "violet", "violet_dark", trim="gold", trim_w=0.4)


def build():
    m = Model("sandiramon")
    top = m.bone("sandiramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    for i in range(3):                                                                   # white coils
        r = 14.0 - i * 3.4
        for j in range(16):
            ang = 2 * math.pi * j / 16
            m.round_box(bd, r * math.cos(ang), r * math.sin(ang), 3.0, 3.0, i * 5.0, i * 5.0 + 5.6, WHITE, cut=1)
    nk = m.bone("neck", bd, (0, 14, -4))
    pts = [(0, 14.0, -4.0), (0, 24.0, -6.0), (0, 32.0, -4.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, nk, p0, p1, 5, WHITE, extend=0.8)
    m.round_box(nk, 0, -3.2, 2.0, 1.0, 16.0, 30.0, armour(P, "silver", "silver_dark", panel=(2.0, 2.0)), cut=0)
    hd = m.bone("head", nk, (0, 34, -4))
    for i in range(7):                                                                   # spread hood dome
        ang = math.radians(-90 + i * 30)
        cx, cz = 9.0 * math.sin(ang), -2.0 + 4.0 * math.cos(ang) * 0.4
        m.box(hd, cx - 2.6, 26.0, cz, cx + 2.6, 42.0 - abs(i - 3) * 1.4, cz + 1.4, HOOD,
              rotation=(0, -math.degrees(ang) * 0.6, 0), pivot=(cx, 34.0, cz))
    m.round_box(hd, 0, -6.0, 3.0, 3.0, 30.0, 37.0, WHITE, cut=1)                            # horned mask
    spike(m, hd, (0, 37.0, -6.0), (0, 1, 0.2), 1.6, 4.0, WHITE, tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.2), 35.0, -9.1, max(sx * 1.0, sx * 2.2), 35.8, -8.9, solid(P, "eye", glow=True))
    m.box(hd, -2.4, 29.6, -9.6, 2.4, 33.0, -8.4, solid(P, "mouth"))                         # gaping maw
    rod(m, hd, (0, 30.6, -9.0), (0, 26.0, -12.0), 1, solid(P, "mouth"), extend=0.2, t2=1)
    for sx in (-1, 1):
        spike(m, hd, (sx * 0.6, 26.0, -12.0), (sx * 0.4, -1, -0.4), 0.8, 1.6, solid(P, "mouth"), tip=0.8)
    return m
