"""Guidemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net, a
line drawing): the guide: a round white floating head like an old television set with a screen face, two long rabbit
ears tipped black, a little propeller on top, a black bow tie with a numbered clock-badge, and two little round hands
with stubby fingers. 1 block tall.

Front is -z, y is up. 28 units tall (no level on wikimon: sized as a Child).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import metal, skin, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1.0, HEIGHT, 1.6)
KIND = "floater"
K = 4
LOOK = "a round white floating television-set head with a screen face, long black-tipped rabbit ears and a bow tie"
BASE = {"white": (246, 246, 250), "white_dark": (190, 192, 206), "black": (30, 28, 32), "screen": (200, 230, 240),
        "screen_dark": (130, 170, 190), "gold": (240, 200, 70), "blue": (90, 140, 220)}
SHINY = {"white": (250, 220, 230), "white_dark": (210, 170, 190), "screen": (230, 210, 140)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = skin(P, "white", dark="white_dark")


def screenf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 4.4 and 9.0 < y < 15.6:
        return tone(p["screen"] if (y * 2.0) % 1.0 > 0.2 else p["screen_dark"], face), None
    return WHITE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("guidemon")
    top = m.bone("guidemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 6.0, 5.0, 7.0, 18.0, screenf, cut=2)
    hd = m.bone("head", bd, (0, 18, 0))
    for sx in (-1, 1):                                                                  # long rabbit ears
        pts = [(sx * 2.6, 18.0, 0.4), (sx * 5.0, 23.0, 1.0), (sx * 7.0, 26.0, 1.4)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 1, WHITE if j == 0 else solid(P, "black"), extend=0.3, t2=3)
    rod(m, hd, (0, 18.0, 0), (0, 20.0, 0), 1, solid(P, "black"), extend=0, t2=1)
    m.box(hd, -2.6, 20.0, -0.3, 2.6, 20.4, 0.3, metal(P, "white", dark="white_dark"))       # propeller
    m.box(bd, -2.4, 5.6, -5.2, -0.4, 7.2, -4.8, solid(P, "black"))                          # bow tie
    m.box(bd, 0.4, 5.6, -5.2, 2.4, 7.2, -4.8, solid(P, "black"))
    m.round_box(bd, 0, -5.4, 1.0, 0.3, 4.4, 6.4, metal(P, "gold", dark="black"), cut=0)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 6.0, 6.0, 0))
        m.round_box(ab, sx * 7.4, -1.0, 1.6, 1.6, 3.0, 6.0, WHITE, cut=1)
        for j in range(3):
            spike(m, ab, (sx * 7.4 + (j - 1) * 0.8, 3.0, -1.0), (0, -1, -0.2), 0.8, 1.4, WHITE)
    return m
