"""Yakiimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a roasted sweet-potato boxer: a big wine-red sweet-potato head with a yellow-ringed eye and a wide
toothy grin, a ragged grey tunic, thin red limbs, big red boxing gloves, baggy grey leg-warmers and red sneakers. 15
blocks.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, leather, plane, skin, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a wine-red sweet-potato boxer with a yellow-ringed eye and a wide grin, a ragged grey tunic, big red boxing gloves and red sneakers"
BASE = {"potato": (140, 50, 70), "potato_dark": (80, 20, 36), "yellow": (250, 220, 80), "tooth": (255, 250, 230),
        "mouth": (60, 14, 20), "grey": (130, 130, 136), "grey_dark": (70, 70, 76), "red": (210, 40, 40),
        "red_dark": (130, 14, 14), "white": (250, 250, 250), "eye": (200, 40, 40)}
SHINY = {"potato": (220, 160, 60), "potato_dark": (150, 90, 20)}


def P(v):
    return pal(BASE, SHINY, v)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            d = math.hypot(a - sx * 2.4, b - 27.0)
            if d < 0.6:
                return p["eye"], None
            if d < 1.4:
                return p["yellow"], None
        if 21.6 < b < 24.4 and abs(a) < 4.0 - (24.4 - b) * 0.6:
            if (a * 1.3) % 1.0 < 0.55 and abs(b - 23.0) > 0.4:
                return p["tooth"], None
            return p["mouth"], None
    return skin(P, "potato", dark="potato_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("yakiimon")
    top = m.bone("yakiimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0, 3.6, 2.6, 10.0, 18.0, fabric(P, "grey", "grey_dark"), cut=1)
    for j in range(5):
        spike(m, bd, (-3.0 + j * 1.5, 10.4, -2.4), (0, -1, -0.2), 1.0, 1.8, fabric(P, "grey", "grey_dark"), tip=0.8)
    hd = m.bone("head", bd, (0, 18, 0))
    ball(m, hd, (0, 25.0, -0.4), 5.4, headf, layers=5, ry=7.6)
    spike(m, hd, (0, 32.0, 0), (0.2, 1, 0), 2.0, 4.0, skin(P, "potato", dark="potato_dark"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.4, 16.0, 0))
        rod(m, ab, (sx * 3.4, 16.0, 0), (sx * 7.0, 18.0 if sx > 0 else 14.0, -3.0), 1, skin(P, "potato", dark="potato_dark"),
            extend=0.3)
        ball(m, ab, (sx * 7.6, 19.0 if sx > 0 else 14.0, -4.0), 3.0, leather(P, "red", "red_dark"), layers=3)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.8, 10.0, 0))
        rod(m, lg, (sx * 1.8, 10.0, 0), (sx * 2.6, 3.0, 0), 1, skin(P, "potato", dark="potato_dark"), extend=0.3)
        m.round_box(lg, sx * 2.6, 0, 2.0, 2.0, 2.0, 7.0, fabric(P, "grey", "grey_dark", axis="x", period=1.2), cut=1)
        m.round_box(lg, sx * 2.6, -1.4, 1.8, 3.0, 0.0, 2.0, leather(P, "red", "red_dark"), cut=1)
    return m
