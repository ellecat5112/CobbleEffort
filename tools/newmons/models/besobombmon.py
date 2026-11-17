"""Beso Bombmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the art on wikimon.net, which shows
only a silhouette with a question mark): a small unrevealed Digimon known only by its shape. A round head with a
bumpy crown, stubby arms flung wide, a plump body and big three-toed feet, built as the black silhouette itself with a
white question mark on its chest. 1 block tall.

Front is -z, y is up. 32 units tall; level unknown (Child used).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import local, plane, solid
from _route import pal, tone

HEIGHT = 32
SCALE, HITBOX = sized(1.0, HEIGHT, 0.9)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 18}
LOOK = "an unrevealed Digimon known only as a black silhouette with a white question mark"
BASE = {"black": (20, 20, 24), "black_l": (60, 60, 70), "mark": (250, 250, 250)}
SHINY = {"black": (240, 240, 246), "black_l": (200, 200, 210), "mark": (20, 20, 24)}


def P(v):
    return pal(BASE, SHINY, v)


def silf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        r = math.hypot(a, b - 15.0)
        ang = math.degrees(math.atan2(b - 15.0, a))
        if abs(r - 1.6) < 0.4 and (ang > -60 or ang < -160):
            return p["mark"], None                               # the curl of the "?"
        if abs(a) < 0.4 and 11.4 < b < 13.6:
            return p["mark"], None
        if abs(a) < 0.4 and 9.4 < b < 10.4:
            return p["mark"], None
    return tone(p["black"], face), None


def build():
    m = Model("besobombmon")
    top = m.bone("besobombmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, (0, 14.0, 0), 6.0, silf, layers=5)
    hd = m.bone("head", bd, (0, 20, 0))
    ball(m, hd, (0, 24.0, 0), 5.4, silf, layers=5)
    for i in range(5):
        ball(m, hd, (-3.6 + i * 1.8, 29.0 + (i % 2), 0), 1.4, silf, layers=2)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 5.0, 16.0, 0))
        rod(m, ab, (sx * 5.0, 16.0, 0), (sx * 11.0, 18.0, 0), 3, silf, extend=0.3)
        for f in range(3):
            spike(m, ab, (sx * 11.0, 18.0, 0), (sx, (f - 1) * 0.6, 0), 1.2, 2.0, silf)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.6, 9.0, 0))
        rod(m, lg, (sx * 2.6, 9.0, 0), (sx * 3.0, 2.0, 0), 3, silf, extend=0.3)
        for f in range(3):
            spike(m, lg, (sx * 3.0, 1.0, -1.0), ((f - 1) * 0.6, -0.2, -1), 1.2, 2.6, silf)
    return m
