"""Tuchidarumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a lumbering clay doll shaped like a teddy bear: a round brown head with little round ears, dot
eyes and a button nose, two brass buttons down its chest, stubby rounded arms and short heavy legs fringed with
straggly clay fur. 15 blocks.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, metal, plane, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a lumbering brown clay teddy-bear doll with round ears, dot eyes, a button nose and two brass buttons"
BASE = {"clay": (150, 100, 56), "clay_dark": (90, 56, 26), "eye": (20, 16, 12), "brass": (220, 170, 70)}
SHINY = {"clay": (140, 140, 150), "clay_dark": (80, 80, 90)}


def P(v):
    return pal(BASE, SHINY, v)


CLAY = skin(P, "clay", dark="clay_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            if math.hypot(a - sx * 2.0, b - 25.4) < 0.6:
                return p["eye"], None
        if math.hypot(a, b - 23.6) < 0.8:
            return p["eye"], None
    return CLAY(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("tuchidarumon")
    top = m.bone("tuchidarumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7, 0))
    ball(m, bd, (0, 13.0, 0), 7.0, CLAY, layers=5, ry=7.6)
    for j in range(2):
        ball(m, bd, (0, 13.0 + j * 3.0, -6.6), 0.9, metal(P, "brass"), layers=1)
    hd = m.bone("head", bd, (0, 20, 0))
    ball(m, hd, (0, 24.6, -0.6), 4.8, headf, layers=4)
    for sx in (-1, 1):
        m.round_box(hd, sx * 3.8, 0, 1.4, 1.0, 27.6, 30.0, CLAY, cut=0)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 6.0, 17.0, 0))
        rod(m, ab, (sx * 6.0, 17.0, 0), (sx * 9.0, 12.0 if sx < 0 else 19.0, -2.0), 3, CLAY, extend=0.6)
        ball(m, ab, (sx * 9.2, 11.4 if sx < 0 else 19.6, -2.2), 2.4, CLAY, layers=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.4, 7.0, 0))
        m.round_box(lg, sx * 3.6, 0, 3.0, 3.4, 0.0, 7.0, fur(P, "clay", "clay_dark", length=1.6), cut=1)
    return m
