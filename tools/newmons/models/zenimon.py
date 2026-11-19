"""Zenimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a living gold coin: a round brass coin body stamped with a big S and solar panels round a square hole,
jointed brass arms, one ending in a telescoping coin-launcher, and little round copper feet. 1 block.

Front is -z, y is up. Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, plane, solid
from _route import pal, tone

HEIGHT = 20
SCALE, HITBOX = sized(1.0, HEIGHT, 2.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a living gold coin stamped with an S around a square hole, with jointed brass arms, a coin-launcher and copper feet"
BASE = {"gold": (230, 190, 80), "gold_dark": (160, 120, 30), "panel": (60, 70, 130), "black": (30, 26, 20),
        "copper": (190, 110, 60), "copper_dark": (120, 60, 30)}
SHINY = {"gold": (200, 204, 216), "gold_dark": (120, 124, 140)}


def P(v):
    return pal(BASE, SHINY, v)


def coinf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        if abs(a) < 1.0 and abs(b - 12.0) < 1.0:
            return p["black"], None
        for sx in (-1, 1):
            if abs(a - sx * 3.0) < 1.0 and abs(b - 12.0) < 0.6:
                return p["panel"], None
        if abs(a) < 1.6 and 14.0 < b < 17.0 and (abs(b - 14.2) < 0.3 or abs(b - 15.5) < 0.3 or abs(b - 16.8) < 0.3 or
                                                (b > 15.5 and a < -1.1) or (b < 15.5 and a > 1.1)):
            return p["black"], None
    return metal(P, "gold", dark="gold_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("zenimon")
    top = m.bone("zenimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 6.0, 1.6, 6.0, 18.0, coinf, cut=0)
    for j in range(16):
        ang = j * 2 * math.pi / 16
        m.box(bd, 6.0 * math.cos(ang) - 1.0, 12.0 + 6.0 * math.sin(ang) - 1.0, -1.6, 6.0 * math.cos(ang) + 1.0,
              12.0 + 6.0 * math.sin(ang) + 1.0, 1.6, metal(P, "gold", dark="gold_dark"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 6.0, 13.0, 0))
        rod(m, ab, (sx * 6.0, 13.0, 0), (sx * 10.0, 15.0, -1.0), 1, metal(P, "gold"), extend=0.2)
        if sx > 0:
            for j in range(3):
                m.round_box(ab, sx * (11.0 + j * 2.0), -1.0, 1.4 - j * 0.2, 1.4 - j * 0.2, 14.0 + j * 1.2, 15.6 + j * 1.2,
                            metal(P, "gold", dark="gold_dark"), cut=0)
            m.round_box(ab, sx * 17.0, -1.0, 2.6, 0.8, 16.0, 20.0, metal(P, "gold", dark="gold_dark"), cut=0)
        else:
            ball(m, ab, (sx * 10.6, 15.0, -1.0), 1.2, metal(P, "gold"), layers=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.0, 6.0, 0))
        rod(m, lg, (sx * 2.0, 6.0, 0), (sx * 2.4, 2.4, 0), 1, metal(P, "gold"), extend=0.2)
        ball(m, lg, (sx * 2.4, 1.8, -0.6), 1.8, metal(P, "copper", dark="copper_dark"), layers=2)
    return m
