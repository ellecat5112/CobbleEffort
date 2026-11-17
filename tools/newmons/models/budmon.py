"""Budmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little seed bud. A round pale green bud with a happy closed-eye smile and a tiny fang, three pink
thorns crowning it, dark thorn nubs round its middle and a single broad green leaf for a tail. Baby II.

Front is -z, y is up. 22 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import cutout, local, skin, solid
from _route import pal, tone

HEIGHT = 22
SCALE, HITBOX = sized(0.5, HEIGHT, 0.5)
KIND = "floater"
K = 4
LOOK = "a round pale green bud with a closed-eye smile, three pink thorns, dark thorn nubs and a broad leaf tail"
BASE = {"green": (200, 236, 150), "green_dark": (140, 190, 90), "leaf": (90, 170, 70), "leaf_dark": (40, 110, 30),
        "pink": (240, 150, 190), "pink_dark": (190, 80, 130), "line": (30, 40, 20), "mouth": (220, 80, 50),
        "fang": (255, 255, 250), "nub": (40, 40, 30)}
SHINY = {"green": (250, 220, 150), "green_dark": (200, 160, 80), "leaf": (200, 120, 60), "leaf_dark": (130, 60, 20),
         "pink": (150, 200, 250), "pink_dark": (80, 130, 200)}


def P(v):
    return pal(BASE, SHINY, v)


BUD = skin(P, "green", dark="green_dark", var=0.03)


def budf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(y - 10.8 + 0.25 * (x - sx * 2.6) ** 2) < 0.2 and abs(x - sx * 2.6) < 1.3:   # closed happy eyes
                return tone(p["line"], face), None
        if 7.0 < y < 8.4 and abs(x) < 1.6 - (8.4 - y) * 0.6:
            return tone(p["mouth"], face), None
    return BUD(x, y, z, face, variant, box=box, **k)


def leafin(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    du, t = abs(u / max(W, 1e-6) - 0.5) * 2, v / max(H, 1e-6)
    return du < math.sin(math.pi * min(1.0, t)) ** 0.7


def leaff(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    du = abs(u / max(W, 1e-6) - 0.5)
    col = p["leaf_dark"] if du < 0.04 or ((v / max(H, 1e-6) * 5 - du * 4) % 1) < 0.08 else p["leaf"]
    return tone(col, face), None


def build():
    m = Model("budmon")
    top = m.bone("budmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 9.0, 0), 6.8, budf, layers=6)
    m.box(bd, 0.4, 7.0, -6.9, 1.0, 7.9, -6.5, solid(P, "fang"))
    hd = m.bone("head", bd, (0, 14, 0))
    for d, ln in (((0, 1, 0), 5.0), ((-0.8, 0.7, 0), 3.4), ((0.8, 0.7, 0), 3.4)):
        spike(m, hd, (d[0] * 4.6, 14.4 + d[1] * 0.6 - (1 - d[1]) * 2.0, 0), d, 2.2, ln, solid(P, "pink"), tip=0.5)
    for i in range(6):                                                       # thorn nubs
        ang = math.radians(i * 60 + 30)
        spike(m, bd, (6.4 * math.cos(ang), 7.0, 6.4 * math.sin(ang)), (math.cos(ang), -0.2, math.sin(ang)), 0.8,
              1.2, solid(P, "nub"))
    tl = m.bone("tail", bd, (5, 9, 2))
    m.box(tl, 4.0, 4.0, 2.0, 8.0, 18.0, 2.0, cutout(leafin, leaff), rotation=(0, -40, -70), pivot=(5, 9, 2))
    return m
