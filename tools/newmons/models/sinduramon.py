"""Sinduramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the rooster of the Twelve Devas: a golden armoured cockerel with a round violet body-orb marked
with characters and tied with a red cord, a golden head with a red comb and wattle, great golden blade-feather wings,
long golden legs with red talons, curved golden horn-arms, and a long rainbow tail. 25 blocks.

Front is -z, y is up. 44 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(25, HEIGHT, 7.0)
KIND = "floater"
K = 3
LOOK = "a golden armoured cockerel with a violet body-orb, a red comb, great golden blade-feather wings, red talons and a rainbow tail"
BASE = {"gold": (230, 190, 80), "gold_dark": (150, 110, 30), "violet": (90, 60, 140), "violet_dark": (40, 24, 80),
        "red": (210, 40, 40), "black": (30, 26, 30), "white": (250, 250, 250)}
SHINY = {"gold": (210, 214, 226), "gold_dark": (120, 124, 140), "violet": (180, 60, 60), "violet_dark": (100, 20, 20)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = metal(P, "gold", dark="gold_dark")


def orbf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(math.sin(x * 1.6) * math.cos(y * 1.4)) > 0.9:
        return tone(p["black"], face), None
    return armour(P, "violet", "violet_dark")(x, y, z, face, variant, box=box, **k)


def rainbowf(x, y, z, face, variant, box=None, **k):
    cols = [(240, 60, 60), (250, 160, 40), (250, 230, 60), (80, 200, 90), (60, 130, 230), (150, 80, 220)]
    return tone(cols[int(z * 0.8) % 6], face), None


def build():
    m = Model("sinduramon")
    top = m.bone("sinduramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    ball(m, bd, (0, 22.0, 0), 6.0, orbf, layers=5)
    m.round_box(bd, 0, 0, 6.2, 6.2, 22.0, 23.0, solid(P, "red"), cut=2)
    hd = m.bone("head", bd, (0, 28, -2))
    m.round_box(hd, 0, -2.0, 2.4, 2.6, 28.0, 34.0, GOLD, cut=1)
    spike(m, hd, (0, 31.0, -4.4), (0, -0.2, -1), 1.4, 3.0, GOLD, tip=0.8)
    for j in range(4):                                                                   # red comb
        spike(m, hd, (0, 34.0, -3.0 + j * 1.2), (0, 1, 0.2 + j * 0.2), 1.4, 4.0 + (j % 2) * 2.0, solid(P, "red"), tip=0.8)
    m.round_box(hd, 0, -3.6, 0.8, 0.6, 27.0, 29.6, solid(P, "red"), cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.3, sx * 2.5), 31.6, -3.0, max(sx * 2.3, sx * 2.5), 32.4, -2.0, solid(P, "black"))
        for j in range(6):                                                               # great blade-feather wings
            ang = math.radians(-10 + j * 16)
            spike(m, bd, (sx * 5.0, 24.0, 2.0), (sx * math.cos(ang), math.sin(ang), 0.3), 2.4, 18.0 - j, GOLD, tip=0.8)
        pts = [(sx * 5.0, 20.0, -2.0), (sx * 10.0, 14.0, -6.0), (sx * 12.0, 18.0, -10.0)]
        for p0, p1 in zip(pts, pts[1:]):                                                  # curved horn-arms
            rod(m, bd, p0, p1, 2, GOLD, extend=0.3)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, bd, (sx * 2.6, 16.0, 0))
        rod(m, lg, (sx * 2.6, 16.0, 0), (sx * 3.0, 6.0, -1.0), 2, GOLD, extend=0.3)
        for f in range(3):
            spike(m, lg, (sx * 3.0 + (f - 1) * 1.0, 5.6, -1.6), ((f - 1) * 0.3, -1, -0.6), 0.9, 3.6, solid(P, "red"),
                  tip=0.8)
    tl = m.bone("tail", bd, (0, 20, 5))                                                  # rainbow tail
    pts = [(0, 20.0, 5.0), (0, 14.0, 12.0), (-2.0, 8.0, 20.0), (-6.0, 8.0, 26.0), (-8.0, 12.0, 28.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, max(1, 4 - i), rainbowf, extend=0.4)
    return m
