"""Bakemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
ghost under a white sheet. A tall rounded white sheet with two black hollow eyes, a gaping red mouth full of crooked
white fangs, ragged sleeves for arms and a tattered hem drifting above the ground. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import cutout, fabric, local, plane, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 2.0)
KIND = "floater"
K = 3
LOOK = "a ghost under a white sheet with hollow black eyes, a gaping red fanged mouth, ragged sleeves and a tattered hem"
BASE = {"sheet": (250, 250, 246), "sheet_dark": (200, 200, 196), "hole": (16, 16, 20), "mouth": (180, 30, 40),
        "mouth_dark": (100, 10, 20), "tooth": (250, 250, 240)}
SHINY = {"sheet": (200, 230, 250), "sheet_dark": (140, 180, 220)}


def P(v):
    return pal(BASE, SHINY, v)


SHEET = fabric(P, "sheet", "sheet_dark", axis="y", period=3.6)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            if (a - sx * 2.6) ** 2 / 1.2 + (b - 34.0) ** 2 / 2.0 < 1:
                return p["hole"], None
        if (a / 4.0) ** 2 + ((b - 28.0) / 3.4) ** 2 < 1:
            jag = abs(((a * 1.1) % 2) - 1) * 1.4
            if b > 31.4 - jag or b < 24.6 + jag:
                return p["tooth"], None
            return (p["mouth_dark"] if abs(a) < 1.6 else p["mouth"]), None
    return SHEET(x, y, z, face, variant, box=box, **k)


def torn(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return v / max(H, 1e-6) > 0.22 * abs(math.sin((box.lo[0] + box.lo[2] + u) * 1.7))


def build():
    m = Model("bakemon")
    top = m.bone("bakemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    ball(m, bd, (0, 32.0, 0), 7.0, facef, layers=6, ry=7.0)
    for i in range(6):                                           # the sheet widening downward
        r = 7.0 + i * 0.5
        m.round_box(bd, 0, 0, r, r * 0.8, 20.0 - i * 2.4, 22.6 - i * 2.4, SHEET, cut=2)
    m.round_box(bd, 0, 0, 7.0, 5.6, 22.0, 30.0, facef, cut=2)
    sk = m.bone("skirt", bd, (0, 8, 0))
    for i in range(12):                                          # tattered hem
        ang = math.radians(i * 30)
        c = (9.0 * math.sin(ang), 8.0, -7.0 * math.cos(ang))
        m.box(sk, c[0] - 2.6, 1.0, c[2], c[0] + 2.6, 8.0, c[2], cutout(torn, SHEET),
              rotation=(0, -math.degrees(ang), 0), pivot=c)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):          # ragged sleeves
        ab = m.bone(nm, bd, (sx * 6.0, 26.0, 0))
        rod(m, ab, (sx * 6.0, 26.0, 0.0), (sx * 12.0, 20.0, -2.0), 5, SHEET, extend=0.6)
        m.box(ab, min(sx * 10.0, sx * 15.0), 13.0, -2.0, max(sx * 10.0, sx * 15.0), 21.0, -2.0, cutout(torn, SHEET))
    return m
