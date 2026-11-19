"""Yatagaramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the three-legged crow of legend: a sleek black crow with glossy violet-sheened feathers, a
mask-like beak, a golden ringed staff-crest rising from its head, great black wings, three taloned legs, and a cloud
of violet mist curling round it. 25 blocks.

Front is -z, y is up. Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing
from _digidetail import feathers, metal, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(25, HEIGHT, 8.0)
KIND = "floater"
K = 3
LOOK = "a sleek black three-legged crow with violet sheen, a golden ringed crest, great black wings and a cloud of violet mist"
BASE = {"black": (34, 30, 44), "black_dark": (10, 8, 16), "violet": (150, 110, 220), "gold": (240, 196, 60),
        "gold_dark": (170, 120, 20), "mist": (190, 170, 240, 150), "eye": (255, 60, 60), "beak": (60, 56, 70),
        "talon": (110, 80, 160)}
SHINY = {"black": (230, 230, 240), "black_dark": (170, 170, 190), "mist": (240, 200, 160, 150)}


def P(v):
    return pal(BASE, SHINY, v)


def featherf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "up" and (abs(x) + z) % 4.0 < 0.5:
        return tone(p["violet"], face), None
    return feathers(P, "black", "black_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("yatagaramon")
    top = m.bone("yatagaramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 22, 0))
    ball(m, bd, (0, 22.0, 0), 5.0, featherf, layers=4, ry=6.4)
    hd = m.bone("head", bd, (0, 28, -5))
    ball(m, hd, (0, 30.0, -6.0), 3.2, featherf, layers=3)
    spike(m, hd, (0, 29.6, -8.6), (0, -0.3, -1), 1.8, 4.0, metal(P, "beak"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.4, sx * 2.8), 30.6, -8.4, max(sx * 1.4, sx * 2.8), 31.4, -8.0, solid(P, "eye", glow=True))
    rod(m, hd, (0, 32.6, -5.0), (0, 40.0, -4.0), 1, metal(P, "gold", dark="gold_dark"), extend=0.0)   # ringed crest
    for k in range(3):
        m.round_box(hd, 0, -4.2, 1.2 + k * 0.4, 1.2 + k * 0.4, 36.0 + k * 1.2, 36.6 + k * 1.2, metal(P, "gold"), cut=0)
    for sx in (-1, 1):
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 3.0, 26.0, 0))
        feather_wing(m, wb, (sx * 3.0, 26.0, 0), 28.0, 14.0, 3, featherf, side=sx, sweep=15, droop=-14.0)
    for i, x in enumerate((-2.4, 0.0, 2.4)):                                            # three legs
        lg = m.bone("leg_%d" % i, bd, (x, 18.0, -1.0))
        rod(m, lg, (x, 18.0, -1.0), (x * 1.3, 9.0, -2.0), 1, solid(P, "talon"), extend=0.3)
        for t in range(3):
            spike(m, lg, (x * 1.3, 9.0, -2.0), ((t - 1) * 0.5, -0.6, -1), 0.9, 3.0, solid(P, "talon"), tip=0.8)
    ms = m.bone("mist", bd, (0, 16, 0))
    for i in range(8):
        ang = i * 2 * math.pi / 8
        ball(m, ms, (10.0 * math.cos(ang), 14.0 + 3.0 * math.sin(ang * 2), 10.0 * math.sin(ang)), 3.4, solid(P, "mist"),
             layers=1)
    for j in range(5):
        spike(m, bd, ((j - 2) * 1.0, 19.0, 5.0), ((j - 2) * 0.2, -0.3, 1), 1.4, 10.0, featherf, tip=0.8)
    return m
