"""Pristimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a red-panda plush puppet stitched together: golden fur with a white muzzle, sleepy blue eyes, a
black stitch seam down its face and chest, a white ruff, two black cannon arms with red claws, and a fat ringed tail
of gold and black. 1 block.

Front is -z, y is up. 28 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, metal, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a stitched golden red-panda plush with sleepy blue eyes, a white ruff, black cannon arms with red claws and a ringed tail"
BASE = {"gold": (240, 170, 40), "gold_dark": (180, 110, 10), "white": (250, 248, 240), "black": (36, 32, 36),
        "black_dark": (12, 10, 12), "eye": (100, 150, 220), "red": (210, 40, 50), "stitch": (60, 40, 30),
        "brown": (110, 70, 40)}
SHINY = {"gold": (220, 220, 230), "gold_dark": (150, 150, 170)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "gold", "gold_dark", length=1.2, density=1.6)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 2.2) < 1.0 and 19.4 < y < 20.4:
                return tone(p["black"] if y > 20.0 else p["eye"], face), None
        if abs(x) < 2.0 and y < 18.6:
            return tone(p["white"], face), None
        if abs(x + 0.8 - (y - 19) * 0.2) < 0.18:
            return tone(p["stitch"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def tailf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (y % 3.0) < 1.0:
        return tone(p["black"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("pristimon")
    top = m.bone("pristimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 11.0, 0), 4.4, FUR, layers=4, ry=5.0)
    m.box(bd, -0.2, 7.0, -4.6, 0.2, 15.0, -4.3, solid(P, "stitch"))
    hd = m.bone("head", bd, (0, 16, 0))
    ball(m, hd, (0, 20.0, -0.4), 5.0, headf, layers=4, ry=4.4)
    m.round_box(hd, 0, -4.4, 2.0, 1.2, 16.6, 19.0, headf, cut=0)
    m.box(hd, -0.6, 18.0, -5.8, 0.6, 18.8, -5.5, solid(P, "black"))
    m.round_box(hd, 0, 0, 4.4, 4.0, 15.0, 16.6, fur(P, "white", "white", length=1.0), cut=1)    # ruff
    for sx in (-1, 1):
        spike(m, hd, (sx * 3.2, 23.4, 0), (sx * 0.4, 1, 0), 2.2, 3.6, FUR, tip=0.8)
        spike(m, hd, (0.6, 24.0, -0.4), (0.2, 1, -0.1), 0.8, 3.0, FUR, tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                   # cannon arms
        ab = m.bone(nm, bd, (sx * 4.0, 14.0, 0))
        rod(m, ab, (sx * 4.0, 14.0, 0), (sx * 10.0, 16.0, -1.0), 4, metal(P, "black", dark="black_dark"), extend=0.4)
        m.round_box(ab, sx * 10.4, -1.0, 1.0, 1.0, 15.0, 17.0, solid(P, "black_dark"), cut=0)
        for f in range(3):
            ang = 2 * math.pi * f / 3
            spike(m, ab, (sx * 10.4, 16.0 + 1.6 * math.sin(ang), -1.0 + 1.6 * math.cos(ang)),
                  (sx * 1, 0.4 * math.sin(ang), 0.4 * math.cos(ang)), 0.9, 2.4, solid(P, "red"), tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.2, 7.0, 0))
        m.round_box(lg, sx * 2.2, -0.4, 1.8, 2.2, 0.0, 7.4, FUR, cut=1)
        m.round_box(lg, sx * 2.2, -1.6, 1.4, 0.6, 0.4, 2.4, solid(P, "brown"), cut=0)
    tl = m.bone("tail", bd, (0, 8, 4))
    pts = [(0, 8.0, 4.0), (0, 4.0, 8.0), (0, 2.0, 12.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 5, tailf, extend=0.8)
    return m
