"""Yarmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a little round brown head with a sly grin and narrowed green eyes, wearing a glossy purple hood with two
pointed ears. 0.5 blocks.

Front is -z, y is up. Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, plane, skin, solid
from _route import pal, tone

HEIGHT = 14
SCALE, HITBOX = sized(0.5, HEIGHT, 1.6)
KIND = "floater"
K = 4
LOOK = "a little round brown head with a sly grin and narrowed green eyes under a glossy purple hood with pointed ears"
BASE = {"brown": (120, 80, 50), "brown_dark": (70, 44, 24), "purple": (110, 90, 200), "purple_dark": (60, 40, 140),
        "eye": (110, 210, 70), "pupil": (20, 30, 10), "white": (255, 255, 255), "mouth": (60, 30, 20)}
SHINY = {"brown": (240, 210, 170), "brown_dark": (190, 150, 110), "purple": (200, 80, 100), "purple_dark": (130, 30, 50)}


def P(v):
    return pal(BASE, SHINY, v)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        if b > 9.6 + abs(a) * 0.4:
            return skin(P, "purple", dark="purple_dark")(x, y, z, face, variant, box=box, **k)
        for sx in (-1, 1):
            c = eye(p, a - sx * 2.2, b - 7.6, 1.2, "eye", lid="brown")
            if c is not None:
                return c, None
        if abs(b - 4.4 - 0.08 * a * a) < 0.25 and abs(a) < 2.4:
            return p["mouth"], None
        return skin(P, "brown", dark="brown_dark")(x, y, z, face, variant, box=box, **k)
    if y > 6.0:
        return skin(P, "purple", dark="purple_dark")(x, y, z, face, variant, box=box, **k)
    return skin(P, "brown", dark="brown_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("yarmon")
    top = m.bone("yarmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 8.0, 0), 6.0, headf, layers=5, squash=0.85)
    for sx in (-1, 1):
        spike(m, bd, (sx * 4.6, 12.0, 0.4), (sx * 1.0, 0.5, 0.2), 2.6, 5.0, skin(P, "purple", dark="purple_dark"), tip=0.8)
    return m
