"""Bokomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the little scholar. A round cream body with a tall egg-shaped head rising to a point, big round
black eyes under arched brows, a grey duck bill with an orange mouth, pointed little ears, short arms held out with
tiny clawed fingers, a pink ribbed waistband and stubby legs with dark toe claws. Child stage.

Front is -z, y is up. 34 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fabric, local, skin, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(1.0, HEIGHT, 0.9)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 16}
LOOK = ("a round cream scholar with a tall egg-shaped head, big black eyes, a grey duck bill, short outstretched "
        "arms, a pink ribbed waistband and stubby clawed feet")
BASE = {"cream": (252, 244, 210), "cream_dark": (220, 200, 150), "bill": (130, 140, 150), "bill_dark": (80, 88, 96),
        "mouth": (240, 140, 40), "eye": (20, 20, 24), "white": (255, 255, 255), "brow": (180, 150, 100),
        "pink": (236, 120, 180), "pink_dark": (180, 60, 120), "claw": (110, 100, 96)}
SHINY = {"cream": (230, 236, 255), "cream_dark": (170, 180, 220), "pink": (100, 200, 140), "pink_dark": (40, 140, 80)}


def P(v):
    return pal(BASE, SHINY, v)


CREAM = skin(P, "cream", dark="cream_dark", var=0.03)
BAND = fabric(P, "pink", "pink_dark", axis="x", period=2.6)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 3.0, y - 23.4)
            if d < 1.3:
                return tone(p["white"] if math.hypot(x - sx * 3.0 + 0.4, y - 23.8) < 0.4 else p["eye"], face), None
            if 26.0 < y < 26.7 and abs(x - sx * 3.0) < 1.8 - 0.4 * abs(y - 26.3):
                return tone(p["brow"], face), None
    return CREAM(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("bokomon")
    top = m.bone("bokomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 5.4, 4.6, 5.0, 15.0, CREAM, cut=2)                              # round body
    m.round_box(bd, 0, 0, 5.9, 5.1, 6.0, 10.4, BAND, cut=2)                               # pink waistband
    hd = m.bone("head", bd, (0, 15, 0))
    for i, (r, y0, y1) in enumerate(((6.6, 15.0, 21.0), (6.4, 21.0, 26.0), (5.4, 26.0, 29.0), (3.8, 29.0, 31.0),
                                     (2.0, 31.0, 33.0))):
        m.round_box(hd, 0, 0, r, r * 0.86, y0, y1, headf, cut=max(1, round(r * 0.35)))
    m.box(hd, -0.8, 33.0, -0.7, 0.8, 34.4, 0.7, headf)                                     # the point
    m.box(hd, -3.4, 18.6, -8.2, 3.4, 21.6, -4.6, solid(P, "bill"))                        # duck bill
    m.box(hd, -3.0, 18.2, -7.8, 3.0, 19.2, -4.6, solid(P, "bill_dark"))
    m.box(hd, -1.8, 19.0, -8.25, 1.8, 20.0, -8.15, solid(P, "mouth"))
    for sx in (-1, 1):                                                                    # pointed ears
        spike(m, hd, (sx * 6.2, 22.0, 0.4), (sx, 0.5, 0.2), 2.0, 2.6, CREAM, tip=0.6)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 5.0, 13.0, 0))
        rod(m, ab, (sx * 4.6, 13.0, 0), (sx * 10.0, 11.0, -0.6), 3, CREAM, extend=0.4)
        for j in range(3):
            spike(m, ab, (sx * 10.2, 11.0, -1.0 + j), (sx, -0.2, 0), 0.6, 1.2, solid(P, "claw"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.4, 6.0, 0))
        rod(m, lg, (sx * 2.4, 6.4, 0), (sx * 2.6, 1.0, -0.4), 3, CREAM, extend=0.4)
        m.box(lg, sx * 2.6 - 1.8, 0.0, -2.8, sx * 2.6 + 1.8, 1.6, 1.4, CREAM)
        for j in range(3):
            spike(m, lg, (sx * 2.6 + (j - 1) * 1.1, 0.6, -2.8), (0, -0.2, -1), 0.6, 1.0, solid(P, "claw"))
    return m
