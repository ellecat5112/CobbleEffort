"""Choromon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little chrome mouse-machine baby. A shiny silver egg-shaped body with two little pointed ears, two
small red eyes, and a long zigzag wire tail ending in a spark. Baby I.

Front is -z, y is up. 18 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.35, HEIGHT, 0.45)
KIND = "floater"
K = 4
LOOK = "a shiny silver egg-shaped baby with pointed ears, small red eyes and a zigzag wire tail ending in a spark"
BASE = {"silver": (210, 214, 226), "silver_dark": (110, 114, 128), "silver_light": (255, 255, 255), "eye": (220, 40, 40),
        "pupil": (60, 10, 10), "wire": (40, 40, 46), "spark": (255, 240, 80)}
SHINY = {"silver": (230, 190, 90), "silver_dark": (160, 110, 30), "silver_light": (255, 240, 180)}


def P(v):
    return pal(BASE, SHINY, v)


SILVER = metal(P, "silver", dark="silver_dark", light="silver_light")


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.4, y - 7.0)
            if d < 1.0:
                return tone(p["pupil"] if d < 0.4 else p["eye"], face), None
    return SILVER(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("choromon")
    top = m.bone("choromon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 7.0, 0.6), 6.0, bodyf, layers=6, squash=0.85)
    for sx in (-1, 1):
        spike(m, bd, (sx * 2.6, 11.6, 1.0), (sx * 0.3, 1, 0.5), 1.8, 3.6, SILVER, tip=0.3)
    tl = m.bone("tail", bd, (2, 9, 5))
    pts = [(2.0, 9.0, 5.0), (4.0, 12.0, 6.0), (5.0, 11.0, 7.0), (6.0, 15.0, 7.4), (7.0, 14.0, 7.6), (8.0, 18.0, 7.8)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, solid(P, "wire"), extend=0.2)
    for i in range(6):
        ang = math.radians(i * 60)
        spike(m, tl, pts[-1], (math.cos(ang), math.sin(ang), 0.3), 0.8, 2.0, solid(P, "spark", glow=True))
    return m
