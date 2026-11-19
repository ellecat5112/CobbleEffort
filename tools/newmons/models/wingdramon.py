"""Wingdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a sky dragon: a sleek blue-scaled dragon with a pale chest, violet bands down its flanks, a
horned head crowned with a white feather crest and a gold horn-spear, wide pale-blue wings with scalloped edges, gold
claws, and a long black whip of a tail. 25 blocks.

Front is -z, y is up. Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, bat_wing
from _digidetail import feathers, metal, scales, skin, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(25, HEIGHT, 10.0)
KIND = "floater"
K = 3
LOOK = "a sleek blue sky dragon with a white feather crest, a gold horn-spear, wide pale-blue wings and a long black whip tail"
BASE = {"blue": (50, 90, 190), "blue_dark": (20, 40, 110), "pale": (210, 220, 240), "violet": (130, 70, 170),
        "wing": (120, 190, 240, 230), "bar": (40, 70, 150), "white": (246, 246, 250), "white_dark": (190, 194, 210),
        "gold": (240, 196, 60), "gold_dark": (170, 120, 20), "black": (30, 30, 36), "eye": (250, 220, 60)}
SHINY = {"blue": (40, 140, 110), "blue_dark": (14, 80, 60), "wing": (150, 230, 190, 230)}


def P(v):
    return pal(BASE, SHINY, v)


def hidef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and (z % 3.0) < 0.8 and y < 17.0:
        return tone(p["violet"], face), None
    if face == "down" or (face == "north" and abs(x) < 2.0):
        return tone(p["pale"], face), None
    return scales(P, "blue", "blue_dark", size=1.0)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("wingdramon")
    top = m.bone("wingdramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    ball(m, bd, (0, 16.0, 0), 4.4, hidef, layers=4, ry=5.0)
    nk = m.bone("neck", bd, (0, 20, -4))
    rod(m, nk, (0, 19.0, -4.0), (0, 23.0, -8.0), 2, hidef, extend=0.6)
    hd = m.bone("head", nk, (0, 24, -9))
    m.round_box(hd, 0, -11.0, 2.0, 3.6, 22.4, 26.0, hidef, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.1), 24.6, -13.0, max(sx * 1.0, sx * 2.1), 25.4, -12.4, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 1.4, 25.6, -9.0), (sx * 0.3, 0.6, 1), 0.9, 4.0, metal(P, "gold"), tip=0.8)
    spike(m, hd, (0, 26.0, -11.0), (0, 0.8, -0.8), 1.2, 7.0, metal(P, "gold", dark="gold_dark"), tip=0.8)
    for j in range(5):
        spike(m, hd, ((j - 2) * 0.6, 26.0, -9.0), ((j - 2) * 0.3, 0.7, 1), 1.0, 5.0, feathers(P, "white", "white_dark"),
              tip=0.8)
    for sx in (-1, 1):
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 3.0, 19.0, 0))
        bat_wing(m, wb, (sx * 3.0, 19.0, 0), 30.0, 18.0, 4, solid(P, "bar"), solid(P, "wing"), side=sx, sweep=15)
        for nm, y0 in (("arm", 14.0), ("leg", 11.0)):
            lb = m.bone("%s_%s" % (nm, "left" if sx > 0 else "right"), bd, (sx * 2.6, y0, -1.0))
            rod(m, lb, (sx * 2.6, y0, -1.0), (sx * 3.4, y0 - 4.0, -2.0), 1, hidef, extend=0.3)
            for t in range(3):
                spike(m, lb, (sx * 3.4, y0 - 4.0, -2.0), ((t - 1) * 0.5, -0.6, -1), 0.8, 2.0, metal(P, "gold"), tip=0.8)
    tl = m.bone("tail", bd, (0, 14, 4))
    pts = [(0, 14.0, 4.0), (-2.0, 9.0, 9.0), (-6.0, 5.0, 12.0), (-11.0, 4.0, 12.0), (-15.0, 6.0, 9.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 2 if i == 0 else 1, hidef if i == 0 else solid(P, "black"), extend=0.3)
    return m
