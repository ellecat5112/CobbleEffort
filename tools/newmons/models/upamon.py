"""Upamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a round pale-yellow axolotl baby with black bead eyes, a wide happy mouth, pink cheeks, a single
upright fin on its head and feathery gill fronds spreading from its sides. 0.5 blocks.

Front is -z, y is up. Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import plane, skin, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.5, HEIGHT, 2.0)
KIND = "floater"
K = 4
LOOK = "a round pale-yellow axolotl baby with bead eyes, a wide smile, a head fin and feathery gill fronds"
BASE = {"cream": (252, 246, 200), "cream_dark": (220, 206, 140), "eye": (24, 24, 30), "white": (255, 255, 255),
        "mouth": (220, 70, 90), "pink": (250, 180, 190)}
SHINY = {"cream": (200, 230, 250), "cream_dark": (140, 180, 220)}


def P(v):
    return pal(BASE, SHINY, v)


CREAM = skin(P, "cream", dark="cream_dark")


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            d = math.hypot(a - sx * 2.2, b - 9.4)
            if d < 0.9:
                return (p["white"] if math.hypot(a - sx * 2.2 + 0.3, b - 9.7) < 0.3 else p["eye"]), None
            if math.hypot(a - sx * 3.6, b - 7.4) < 0.8:
                return p["pink"], None
        if 5.6 < b < 7.6 and abs(a) < 2.6 - (7.6 - b) * 0.8 and b < 7.6 - 0.1 * a * a + 0.4:
            return p["mouth"], None
    return CREAM(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("upamon")
    top = m.bone("upamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 8.0, 0), 5.6, bodyf, layers=5, squash=0.85)
    spike(m, bd, (0, 12.4, 0.4), (0, 1, 0.1), 1.6, 6.0, CREAM, tip=0.8)
    for sx in (-1, 1):                                                                  # gill fronds
        for j in range(3):
            spike(m, bd, (sx * 5.0, 9.0, 0.6), (sx, 0.5 - j * 0.45, 0.1), 1.4, 5.4 - abs(j - 1) * 1.2, CREAM, tip=0.8)
    return m
