"""V-mon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a little blue dragon boy: a big head with a yellow V on its brow, a short horn on its nose, swept fin
ears, red eyes and a fanged grin, a white belly and muzzle, fists up ready to fight, clawed feet and a long tail. 1
block.

Front is -z, y is up. Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, plane, skin, solid
from _route import pal, tone

HEIGHT = 26
SCALE, HITBOX = sized(1.0, HEIGHT, 1.6)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 14}
LOOK = "a little blue dragon boy with a yellow V on its brow, a nose horn, fin ears, a white belly and fists up"
BASE = {"blue": (60, 150, 230), "blue_dark": (24, 80, 160), "white": (250, 250, 252), "white_dark": (200, 200, 214),
        "yellow": (250, 210, 40), "eye": (200, 30, 30), "pupil": (40, 6, 6), "claw": (250, 240, 200),
        "mouth": (150, 30, 40)}
SHINY = {"blue": (90, 190, 110), "blue_dark": (30, 120, 50)}


def P(v):
    return pal(BASE, SHINY, v)


BLUE = skin(P, "blue", dark="blue_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        if 23.0 < b < 24.6 and abs(abs(a) - (b - 23.0) * 1.0) < 0.45 and abs(a) < 1.8:
            return p["yellow"], None
        for sx in (-1, 1):
            c = eye(p, a - sx * 1.8, b - 21.6, 1.0, "eye")
            if c is not None:
                return c, None
        if b < 20.0:
            if abs(b - 18.6) < 0.25 and abs(a) < 1.6:
                return p["mouth"], None
            return tone(p["white"], face), None
    return BLUE(x, y, z, face, variant, box=box, **k)


def bellyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 2.4:
        return tone(p["white"], face), None
    return BLUE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("vmon")
    top = m.bone("vmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7, 0))
    m.round_box(bd, 0, 0, 3.4, 2.8, 7.0, 16.0, bellyf, cut=1)
    hd = m.bone("head", bd, (0, 16, 0))
    m.round_box(hd, 0, -0.4, 4.0, 3.8, 16.6, 25.0, headf, cut=2)
    spike(m, hd, (0, 20.0, -4.0), (0, 0.6, -1), 1.2, 2.2, solid(P, "claw"), tip=0.8)
    for sx in (-1, 1):                                                                 # fin ears
        spike(m, hd, (sx * 3.6, 24.0, 0.6), (sx * 0.8, 0.8, 0.5), 2.4, 4.0, BLUE, tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.4, 14.0, 0))
        rod(m, ab, (sx * 3.4, 14.0, 0), (sx * 5.0, 12.0, -3.0), 2, BLUE, extend=0.4)
        ball(m, ab, (sx * 5.0, 13.4, -4.0), 1.8, BLUE, layers=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.0, 7.0, 0))
        rod(m, lg, (sx * 2.0, 7.0, 0), (sx * 2.4, 1.6, 0.4), 2, BLUE, extend=0.4)
        m.round_box(lg, sx * 2.4, -0.8, 1.6, 2.4, 0.0, 1.8, BLUE, cut=0)
        for t in range(3):
            spike(m, lg, (sx * 2.4 + (t - 1) * 1.0, 0.8, -3.0), (0, -0.2, -1), 0.8, 1.4, solid(P, "claw"), tip=0.8)
    tl = m.bone("tail", bd, (0, 8, 2.6))
    pts = [(0, 8.0, 2.6), (2.0, 5.0, 7.0), (5.0, 4.0, 11.0), (8.0, 5.0, 13.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 2 if i < 1 else 1, BLUE, extend=0.4)
    return m
