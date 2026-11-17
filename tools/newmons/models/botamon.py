"""Botamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the first baby. A soft round blob of shaggy black fur with two little rounded ears and two bright
yellow eyes. Baby I.

Front is -z, y is up. 18 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model
from _digi import sized
from _digidetail import fur
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.35, HEIGHT, 0.45)
KIND = "floater"
K = 4
LOOK = "a soft round blob of shaggy black fur with two little rounded ears and bright yellow eyes"
BASE = {"black": (40, 40, 46), "black_dark": (12, 12, 16), "black_tip": (120, 120, 130), "eye": (255, 210, 40),
        "eye_core": (255, 250, 200)}
SHINY = {"black": (200, 200, 216), "black_dark": (130, 130, 150), "black_tip": (250, 250, 255), "eye": (240, 60, 80)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "black", "black_dark", tip="black_tip", length=1.0)


def blobf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 3.6, y - 7.4)
            if d < 1.3:
                c = p["eye_core"] if d < 0.5 else p["eye"]
                return c, c
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("botamon")
    top = m.bone("botamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    for i, (r, y0, y1) in enumerate(((7.0, 0.0, 2.0), (9.0, 2.0, 5.0), (9.6, 5.0, 9.0), (9.0, 9.0, 11.6),
                                     (7.4, 11.6, 13.4), (5.0, 13.4, 14.6))):
        m.round_box(bd, 0, 0, r, r * 0.8, y0, y1, blobf, cut=max(1, round(r * 0.35)))
    hd = m.bone("head", bd, (0, 13, 0))
    for sx in (-1, 1):                                                       # little rounded ears
        m.round_box(hd, sx * 5.4, 0, 2.6, 2.2, 13.0, 17.4, FUR, cut=1)
    return m
