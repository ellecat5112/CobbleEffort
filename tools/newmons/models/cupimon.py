"""Cupimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a little cupid. A plump white creature with a tall curling pointed head, big round golden eyes with
black dot freckles, a tiny fanged smile, a heart mark on its cheek, little golden wings and stubby arms and feet.
Baby II.

Front is -z, y is up. 26 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, feathers, skin, solid
from _route import pal, tone

HEIGHT = 26
SCALE, HITBOX = sized(0.5, HEIGHT, 0.55)
KIND = "floater"
K = 4
LOOK = "a plump white cupid with a tall curling pointed head, big golden eyes, a heart on its cheek and little golden wings"
BASE = {"white": (250, 250, 252), "white_dark": (200, 204, 220), "eye": (220, 170, 60), "pupil": (40, 30, 10),
        "black": (30, 30, 36), "heart": (230, 90, 120), "gold": (250, 210, 100), "gold_dark": (210, 160, 50)}
SHINY = {"white": (250, 220, 236), "white_dark": (220, 170, 200), "gold": (180, 220, 250), "gold_dark": (120, 170, 220)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "white", dark="white_dark", var=0.02)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            c = eye(p, x - sx * 2.6, y - 12.0, 1.6, "eye")
            if c is not None:
                return c, None
            for j in range(3):
                if math.hypot(x - sx * (4.6 + j * 0.2), y - 13.4 + j * 1.0) < 0.35:
                    return tone(p["black"], face), None                     # dot freckles
        if math.hypot(x - 3.6, y - 9.4) < 0.7:
            return tone(p["heart"], face), None
        if abs(y - 9.0 - 0.15 * x * x) < 0.2 and abs(x) < 1.2:
            return tone(p["black"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("cupimon")
    top = m.bone("cupimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    ball(m, bd, (0, 10.0, 0), 6.4, bodyf, layers=6)
    hd = m.bone("head", bd, (0, 15, 0))
    pts = [(0, 15.0, 0), (0, 19.0, 0.4), (0.6, 23.0, 0.8), (2.4, 25.0, 1.0), (3.6, 24.0, 1.0)]  # curling point
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, hd, p0, p1, max(1, 5 - j), SKIN, extend=0.4)
    for sx in (-1, 1):                                                       # little golden wings
        ab = m.bone("arm_left" if sx > 0 else "arm_right", bd, (sx * 6.0, 11.0, 2.0))
        m.box(ab, min(sx * 5.0, sx * 11.0), 9.0, 2.6, max(sx * 5.0, sx * 11.0), 13.0, 2.6,
              feathers(P, "gold", "gold_dark", size=(0.8, 1.6)), rotation=(0, sx * 20, sx * 15),
              pivot=(sx * 5.0, 11.0, 2.6))
        lg = m.bone("leg_left" if sx > 0 else "leg_right", top, (sx * 2.4, 3.0, 0))
        m.box(lg, sx * 2.4 - 1.4, 0.0, -1.6, sx * 2.4 + 1.4, 4.0, 1.4, SKIN)
    return m
