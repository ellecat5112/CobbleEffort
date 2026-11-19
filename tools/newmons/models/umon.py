"""Umon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net, a tiny game sprite): a little shadow wisp: a black head of flickering spiky darkness with slanted
glowing yellow eyes and a jagged grin, trailing a wisp of smoke. 0.5 blocks.

Front is -z, y is up. Baby II stage (by analogy: wikimon gives no level).
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import plane, skin, solid
from _route import pal, tone

HEIGHT = 17
SCALE, HITBOX = sized(0.5, HEIGHT, 1.2)
KIND = "floater"
K = 4
LOOK = "a little shadow wisp: a black head of spiky darkness with slanted glowing yellow eyes and a jagged grin"
BASE = {"black": (40, 38, 46), "black_dark": (14, 12, 18), "eye": (250, 210, 50), "mouth": (240, 230, 200),
        "smoke": (80, 76, 90, 170)}
SHINY = {"black": (70, 40, 90), "black_dark": (30, 14, 40), "eye": (120, 240, 250)}


def P(v):
    return pal(BASE, SHINY, v)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            if abs(b - 11.0 - sx * a * 0.3 + 0.6) < 0.6 and 0.8 < abs(a) < 3.0 and a * sx > 0:
                return p["eye"], p["eye"]
        if 6.6 < b < 8.0 and abs(a) < 2.6 and (int((a + 3) * 1.6) % 2 == 0 or b < 7.2):
            return p["mouth"], None
    return skin(P, "black", dark="black_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("umon")
    top = m.bone("umon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 10.0, 0), 4.6, headf, layers=5)
    for j in range(7):                                                                 # spiky darkness
        ang = j * 2 * math.pi / 7
        spike(m, bd, (3.6 * math.cos(ang), 10.0 + 3.6 * math.sin(ang), 1.0), (math.cos(ang), math.sin(ang), 0.2), 1.6,
              3.0, skin(P, "black", dark="black_dark"), tip=0.8)
    for j in range(3):
        ball(m, bd, (0.6 * j, 4.0 - j * 1.4, 1.0 + j * 0.6), 1.6 - j * 0.4, solid(P, "smoke"), layers=1)
    spike(m, bd, (0, 14.0, 0), (0.3, 1, 0), 1.4, 5.0, skin(P, "black", dark="black_dark"), tip=0.8)
    return m
