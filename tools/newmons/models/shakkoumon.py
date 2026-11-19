"""Shakkoumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the fusion of Ankylomon and Angemon, a living dogu clay figure: a round silver body banded with
gold and engraved with swirls, a domed head with huge red-rimmed slit eyes and a little golden cross on top, two small
white angel wings, ball-jointed silver arms with red orbs at the shoulders, and stubby flared legs. 25 blocks.

Front is -z, y is up. 44 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing
from _digidetail import armour, feathers, metal, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 4}
LOOK = "a living dogu clay figure: a round silver body banded gold, a domed head with huge red-rimmed slit eyes, a golden cross and small white wings"
BASE = {"silver": (210, 214, 226), "silver_dark": (120, 124, 140), "gold": (230, 200, 120), "gold_dark": (160, 120, 50),
        "red": (210, 40, 40), "white": (248, 248, 252), "white_dark": (190, 196, 214), "blue": (60, 100, 200),
        "black": (30, 30, 34)}
SHINY = {"silver": (200, 150, 110), "silver_dark": (130, 80, 50)}


def P(v):
    return pal(BASE, SHINY, v)


def clayf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (y % 6.0) < 1.2:
        return tone(p["gold"], face), None
    if face == "north" and abs(math.sin(x * 1.3 + y * 0.7)) > 0.92:
        return tone(p["gold_dark"], face), None
    return metal(P, "silver", dark="silver_dark")(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot((x - sx * 3.0) * 0.8, (y - 34.0) * 1.6)
            if d < 1.0:
                return tone(p["black"], face), None
            if d < 2.2:
                return tone(p["red"], face), None
        if abs(x) < 0.6 and 30.0 < y < 32.0:
            return tone(p["blue"], face), None
    return clayf(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("shakkoumon")
    top = m.bone("shakkoumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, (0, 18.0, 0), 8.0, clayf, layers=6, ry=8.0)
    hd = m.bone("head", bd, (0, 26, 0))
    ball(m, hd, (0, 33.0, 0), 7.0, headf, layers=5, ry=6.0)
    rod(m, hd, (0, 38.6, 0), (0, 43.0, 0), 1, metal(P, "gold", dark="gold_dark"), extend=0.2, t2=2)   # golden cross
    m.box(hd, -2.0, 41.0, -1.0, 2.0, 42.0, 1.0, metal(P, "gold", dark="gold_dark"))
    for sx in (-1, 1):
        feather_wing(m, bd, (sx * 6.0, 24.0, 4.0), 12.0, 7.0, 4, feathers(P, "white", "white_dark"), side=sx, sweep=10,
                     droop=-4.0, layers=1)
        ab = m.bone("arm_left" if sx > 0 else "arm_right", bd, (sx * 8.0, 22.0, 0))
        ball(m, ab, (sx * 9.0, 22.0, 0), 2.6, solid(P, "red"), layers=2)
        rod(m, ab, (sx * 9.0, 22.0, 0), (sx * 12.0, 14.0, -2.0), 4, clayf, extend=0.6)
        ball(m, ab, (sx * 12.6, 12.0, -2.0), 2.6, clayf, layers=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 10.0, 0))
        m.round_box(lg, sx * 4.0, 0, 3.0, 3.0, 4.0, 11.0, clayf, cut=1)
        m.round_box(lg, sx * 4.0, -0.6, 3.6, 4.0, 0.0, 4.0, clayf, cut=1)
    return m
