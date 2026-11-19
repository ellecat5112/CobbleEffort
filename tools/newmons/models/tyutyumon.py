"""Tyutyumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a little stitched plush mouse in mustard yellow: two huge round ears, a sly half-lidded grin,
patchwork stitches all over, oversized red gloves, black-tipped feet and a frayed rope tail. 1 block.

Front is -z, y is up. Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, leather, plane, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 2.0)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 12}
LOOK = "a little stitched plush mouse in mustard yellow with huge round ears, a sly grin, oversized red gloves and a frayed rope tail"
BASE = {"yellow": (230, 200, 70), "yellow_dark": (170, 140, 30), "stitch": (60, 40, 20), "red": (210, 40, 40),
        "red_dark": (130, 16, 16), "black": (30, 26, 24), "eye": (30, 26, 24), "white": (250, 250, 240)}
SHINY = {"yellow": (180, 180, 200), "yellow_dark": (120, 120, 140)}


def P(v):
    return pal(BASE, SHINY, v)


def plushf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (abs(x - 0.6 * math.sin(y)) < 0.18 or abs(y - 12.0 - 0.3 * x) < 0.18) and int((x + y + z) * 2) % 2:
        return tone(p["stitch"], face), None
    if face == "north":
        a, b = plane(x, y, z, face)
        if 19.0 < b < 23.0:
            for sx in (-1, 1):
                if abs(b - 21.2) < 0.35 and abs(a - sx * 1.4) < 0.8:
                    return p["eye"], None
            if abs(b - 19.6 - 0.08 * a * a) < 0.25 and abs(a) < 2.0:
                return p["black"], None
    return fabric(P, "yellow", "yellow_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("tyutyumon")
    top = m.bone("tyutyumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    m.round_box(bd, 0, 0, 3.4, 3.0, 5.0, 15.0, plushf, cut=1)
    hd = m.bone("head", bd, (0, 15, 0))
    ball(m, hd, (0, 20.0, -0.4), 3.8, plushf, layers=4)
    for sx in (-1, 1):
        m.round_box(hd, sx * 4.4, 0.6, 3.2, 1.2, 23.0, 29.6, plushf, cut=1)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.4, 13.0, 0))
        rod(m, ab, (sx * 3.4, 13.0, 0), (sx * 5.0, 10.0, -2.0), 1, plushf, extend=0.3)
        ball(m, ab, (sx * 5.6, 9.4, -3.0), 2.4, leather(P, "red", "red_dark"), layers=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.8, 5.0, 0))
        m.round_box(lg, sx * 2.0, -0.6, 1.6, 2.4, 0.0, 5.0, plushf, cut=1)
        m.box(lg, sx * 2.0 - 1.6, 0.0, -3.2, sx * 2.0 + 1.6, 1.2, -2.4, solid(P, "black"))
    tl = m.bone("tail", bd, (0, 7, 3))
    pts = [(0, 7.0, 3.0), (3.0, 9.0, 6.0), (6.0, 13.0, 7.0), (8.0, 14.0, 6.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, solid(P, "yellow_dark"), extend=0.3)
    for j in range(4):
        spike(m, tl, pts[-1], (0.6, (j - 1.5) * 0.5, 0), 0.8, 1.8, solid(P, "yellow"), tip=0.8)
    return m
