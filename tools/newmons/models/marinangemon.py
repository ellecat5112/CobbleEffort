"""Marin Angemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the sea angel: a tiny pink-white sea-angel spirit with big green eyes and a cat smile, two long wavy pink feelers,
wide pink-white feathered wings, a golden collar and a red heart on its chest, and a wispy ghostlike tail. 35 blocks
tall.

Front is -z, y is up. 26 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing
from _digidetail import feathers, metal, skin, solid
from _route import pal, tone

HEIGHT = 26
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
KIND = "floater"
K = 4
LOOK = "a tiny pink-white sea-angel spirit with big green eyes, long wavy feelers, wide feathered wings, a gold collar and a red heart"
BASE = {"pink": (250, 226, 236), "pink_dark": (220, 170, 196), "eye": (60, 180, 100), "pupil": (20, 30, 24),
        "red": (220, 40, 50), "gold": (230, 190, 70), "gold_dark": (160, 120, 20), "mouth": (60, 40, 50)}
SHINY = {"pink": (220, 240, 255), "pink_dark": (160, 190, 230), "eye": (230, 140, 40)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.0, y - 16.0)
            if d < 0.6:
                return tone(p["pupil"], face), None
            if d < 1.4:
                return tone(p["eye"], face), None
        if abs(y - 13.6 - 0.3 * abs(math.sin(x * 2.4))) < 0.2 and abs(x) < 1.0:
            return tone(p["mouth"], face), None
        if abs(x) < 1.6 - abs(y - 7.6) * 0.8 and y < 8.6 and y > 6.0:
            return tone(p["red"], face), None
    return skin(P, "pink", dark="pink_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("marinangemon")
    top = m.bone("marinangemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 13.0, 0), 5.0, bodyf, layers=4)
    m.round_box(bd, 0, 0, 4.0, 3.6, 8.0, 12.0, bodyf, cut=1)
    m.round_box(bd, 0, 0, 3.4, 3.0, 10.4, 11.4, metal(P, "gold", dark="gold_dark"), cut=1)
    for j in range(3):                                                               # wispy tail
        spike(m, bd, ((j - 1) * 1.6, 8.0, 0), ((j - 1) * 0.6, -1, 0.3), 1.4, 6.0, skin(P, "pink", dark="pink_dark"), tip=0.8)
    hd = m.bone("head", bd, (0, 18, 0))
    for sx in (-1, 1):                                                               # wavy feelers
        pts = [(sx * 1.6, 17.6, 0), (sx * 4.0, 22.0, 0.6), (sx * 2.0, 24.0, 1.0), (sx * 5.0, 26.0, 1.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, skin(P, "pink", dark="pink_dark"), extend=0.2, t2=1)
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 4.0, 12.0, 1.0))
        feather_wing(m, wb, (side * 4.0, 12.0, 1.0), 12.0, 5.0, 2, feathers(P, "pink", "pink_dark"), side=side, sweep=5,
                     droop=4.0)
    return m
