"""Pokomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a round golden-yellow blob of a fox kit with two tall pointed ears, blue eyes, a little cat
mouth, tiny paw nubs, and a big fox tail tipped white curling up behind. 0.5 blocks.

Front is -z, y is up. 18 units tall; Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.5, HEIGHT, 1.4)
KIND = "floater"
K = 3
LOOK = "a round golden-yellow fox-kit blob with tall pointed ears, blue eyes, a cat mouth and a white-tipped fox tail"
BASE = {"yellow": (250, 196, 60), "yellow_dark": (210, 140, 30), "white": (252, 250, 244), "eye": (70, 130, 210),
        "pupil": (20, 24, 40), "mouth": (60, 30, 20)}
SHINY = {"yellow": (200, 210, 230), "yellow_dark": (140, 150, 180)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "yellow", "yellow_dark", length=1.0, density=1.4)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.8, (y - 6.4) * 0.8)
            if d < 0.5:
                return tone(p["pupil"], face), None
            if d < 1.0:
                return tone(p["eye"], face), None
        if abs(y - 4.6) < 0.35 and abs(x) < 1.0 and abs(abs(x) - 0.5) < 0.35:
            return tone(p["mouth"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def tailf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if y > 12.0:
        return tone(p["white"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("pokomon")
    top = m.bone("pokomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 5.0, 0), 4.6, facef, layers=4, ry=4.4)
    for sx in (-1, 1):
        spike(m, bd, (sx * 2.6, 8.0, 0), (sx * 0.4, 1, 0), 2.6, 6.0, FUR, tip=0.8)          # tall ears
        spike(m, bd, (sx * 3.0, 1.2, -2.6), (sx * 0.4, -1, -0.6), 1.4, 1.6, FUR, tip=0.8)   # paw nubs
    tl = m.bone("tail", bd, (0, 4, 4))
    pts = [(0, 3.0, 4.0), (1.0, 6.0, 7.0), (2.0, 10.0, 8.0), (2.6, 14.0, 7.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 2 + (1 if i == 1 else 0), tailf, extend=0.4, t2=2 + i % 2)
    spike(m, tl, pts[-1], (0.2, 1, -0.4), 2.0, 3.0, tailf, tip=0.8)
    return m
