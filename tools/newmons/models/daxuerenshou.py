"""Daxuerenshou (a Digimon of the CobbleEffort: Digital crossover; after the manga art on wikimon.net): the great snow
man. A huge pear-shaped white snow beast, its little domed head topped by a ring of round bumps, a wide simple smile,
heavy rounded arms with big mitt fists hanging low, and thick stubby legs; its pale fur is shaded blue-grey in the
creases. 15 blocks tall.

Front is -z, y is up. 50 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _digi import sized
from _digibeast import ball
from _digidetail import fur, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a huge pear-shaped white snow beast with a bumpy domed head, a wide smile, heavy mitt fists and stubby legs"
BASE = {"snow": (244, 246, 250), "snow_dark": (170, 186, 210), "mouth": (40, 40, 50), "eye": (40, 40, 50)}
SHINY = {"snow": (250, 230, 200), "snow_dark": (210, 170, 130)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "snow", "snow_dark", length=1.6, density=2.0)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and 43.0 < y < 47.0:
        if abs(y - (44.2 + 0.08 * x * x)) < 0.3 and abs(x) < 3.2:
            return tone(p["mouth"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("daxuerenshou")
    top = m.bone("daxuerenshou", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    for i in range(9):                                                           # pear-shaped body
        t = i / 8
        r = 6.0 + 7.6 * (1 - t ** 1.8)
        y0 = 10.0 + i * 4.0
        m.round_box(bd, 0, 0, r, r * 0.8, y0, y0 + 4.4, bodyf, cut=max(1, round(r * 0.25)))
    hd = m.bone("head", bd, (0, 46, 0))
    ball(m, hd, (0, 47.0, 0.4), 4.4, bodyf, layers=4, squash=0.9)
    for i in range(6):                                                           # ring of bumps
        ang = math.radians(-60 + i * 24)
        m.round_box(hd, 3.2 * math.sin(ang), -3.2 * math.cos(ang) + 0.4, 0.9, 0.9, 49.6, 51.0, FUR, cut=0)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 10.0, 36.0, 0))
        rod(m, ab, (sx * 9.0, 36.0, 0), (sx * 18.0, 20.0, -2.0), 6, FUR, extend=1.0)
        m.round_box(ab, sx * 18.6, -2.4, 4.2, 4.0, 12.0, 20.0, FUR, cut=2)        # mitt fist
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 6.0, 12.0, 0))
        m.round_box(lg, sx * 6.0, 0, 4.4, 5.0, 0.0, 13.0, FUR, cut=2)
        m.round_box(lg, sx * 6.0, -2.0, 4.6, 5.6, 0.0, 3.0, FUR, cut=1)
    return m
