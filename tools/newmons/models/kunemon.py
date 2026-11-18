"""Kunemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
electric larva: a plump yellow caterpillar with black lightning-bolt stripes, a big blue beak-like snout, red segmented
underside with little blue claw-feet, a blue stinger at its tail and two long wavy yellow antennae. Child stage,
1 block long.

Front is -z, y is up. 20 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 20
SCALE, HITBOX = sized(1.0, HEIGHT, 2.0)
KIND = "quadruped"
K = 4
LOOK = "a plump yellow caterpillar with black lightning stripes, a big blue snout, a red underside, a blue stinger and wavy antennae"
BASE = {"yellow": (250, 220, 50), "yellow_dark": (200, 160, 10), "black": (30, 30, 34), "blue": (60, 140, 230),
        "blue_dark": (20, 70, 160), "red": (210, 50, 50), "red_dark": (130, 20, 20)}
SHINY = {"yellow": (120, 220, 120), "yellow_dark": (50, 150, 50)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if y < 3.6:
        return tone(p["red"], face), None
    if face in ("east", "west", "up") and abs(((z + y * 0.6) % 4.0) - 2.0 - 0.6 * math.copysign(1, ((z * 2.0) % 2.0) - 1)) < 0.4:
        return tone(p["black"], face), None
    return skin(P, "yellow", dark="yellow_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("kunemon")
    top = m.bone("kunemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    for i in range(5):                                                               # segmented body, front to back
        r = 5.6 - i * 0.7
        ball(m, bd, (0, r, -4.0 + i * 3.4), r, bodyf, layers=3)
    hd = m.bone("head", bd, (0, 10, -6))
    m.round_box(hd, 0, -8.6, 3.0, 2.4, 3.0, 8.0, skin(P, "blue", dark="blue_dark"), cut=1)       # blue snout
    for sx in (-1, 1):                                                               # wavy antennae
        pts = [(sx * 1.6, 10.0, -5.0), (sx * 3.0, 15.0, -6.0), (sx * 2.0, 18.0, -3.0), (sx * 4.0, 20.0, -1.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "yellow"), extend=0.3, t2=1)
    for i in range(4):                                                               # little blue claw-feet
        for sx in (-1, 1):
            spike(m, bd, (sx * 2.0, 1.0, -3.0 + i * 3.0), (sx * 0.4, -1, -0.3), 0.8, 1.4, solid(P, "blue"), tip=0.8)
    tb = m.bone("tail", bd, (0, 4, 12))
    spike(m, tb, (0, 4.0, 12.0), (0, 0.8, 1), 1.6, 5.0, skin(P, "blue", dark="blue_dark"), tip=0.8)
    return m
