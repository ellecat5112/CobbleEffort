"""Lekismon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
moon rabbit fighter: a lithe white rabbit-girl with long swept-back blue-and-pink ear streamers, a pale face with a
dark visor stripe, a white body with a yellow crescent on the chest, long blue ribbon sashes, black boxing-style gloves,
dark ankle bands and long digitigrade rabbit legs. 15 blocks tall.

Front is -z, y is up. 48 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fabric, leather, skin, solid, strands
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a lithe white moon rabbit fighter with long blue-and-pink ear streamers, a yellow crescent, blue ribbon sashes and black gloves"
BASE = {"white": (246, 246, 252), "white_dark": (176, 180, 200), "blue": (110, 150, 230), "blue_dark": (50, 80, 170),
        "pink": (240, 170, 200), "yellow": (250, 220, 70), "black": (30, 30, 36), "black_dark": (10, 10, 14),
        "eye": (60, 60, 80), "claw": (60, 80, 150)}
SHINY = {"white": (250, 220, 230), "white_dark": (210, 160, 180), "blue": (230, 150, 60), "blue_dark": (160, 90, 20)}


def P(v):
    return pal(BASE, SHINY, v)


SK = skin(P, "white", dark="white_dark")


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(math.hypot(x + 0.6, y - 28.0) - 2.0) < 0.6 and x < 0.4:
        return tone(p["yellow"], face), None
    return SK(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("lekismon")
    top = m.bone("lekismon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    m.round_box(bd, 0, 0.6, 4.0, 4.4, 18.0, 26.0, SK, cut=2)                           # round hips
    m.round_box(bd, 0, 0.2, 3.0, 2.6, 25.0, 32.0, bodyf, cut=1)
    hd = m.bone("head", bd, (0, 32, 0))
    m.round_box(hd, 0, 0, 2.6, 2.8, 32.0, 38.0, SK, cut=1)
    m.round_box(hd, 0, -2.8, 2.2, 0.3, 35.0, 36.0, solid(P, "black"), cut=0)               # visor stripe
    for sx in (-1, 1):                                                               # ear streamers
        for j, key in enumerate(("blue", "pink", "white")):
            pts = [(sx * 1.4, 37.6, 0), (sx * (4.0 + j * 1.4), 44.0 - j * 1.6, 3.0), (sx * (8.0 + j * 1.6), 46.0 - j * 3.0, 6.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, hd, p0, p1, 1, strands(P, key, "blue_dark"), extend=0.3, t2=2)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.0, 31.0, 0))
        rod(m, ab, (sx * 3.0, 31.0, 0), (sx * 6.0, 26.0, -2.0), 1, SK, extend=0.3, t2=2)
        m.round_box(ab, sx * 6.6, -2.6, 1.8, 1.8, 22.6, 26.0, leather(P, "black", "black_dark"), cut=1)   # gloves
        pts = [(sx * 2.0, 26.0, 2.0), (sx * 8.0, 22.0, 5.0), (sx * 10.0, 16.0, 4.0)]        # ribbon sashes
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 1, fabric(P, "blue", "blue_dark"), extend=0.3, t2=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                              # long rabbit legs
        lg = m.bone(nm, top, (sx * 2.6, 18.0, 0))
        rod(m, lg, (sx * 2.6, 19.0, 0), (sx * 3.0, 10.0, -2.0), 2, SK, extend=0.4)
        rod(m, lg, (sx * 3.0, 10.0, -2.0), (sx * 3.0, 3.0, 1.0), 1, SK, extend=0.3, t2=2)
        m.round_box(lg, sx * 3.0, 1.0, 1.2, 1.2, 3.0, 4.4, solid(P, "black"), cut=0)
        m.round_box(lg, sx * 3.0, -1.4, 1.4, 3.0, 0.0, 2.6, SK, cut=1)
        spike(m, lg, (sx * 3.0, 0.6, -4.2), (0, -0.2, -1), 0.9, 1.6, solid(P, "claw"), tip=0.8)
    return m
