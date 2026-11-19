"""Xiaomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little egg-shaped piglet: a smooth white oval body with a cracked shell rim over its dot eyes,
long drooping pink ears, a tiny smiling snout, four stubby pink hooves and a curly pink tail. 0.5 blocks.

Front is -z, y is up. Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import plane, skin, solid
from _route import pal, tone

HEIGHT = 17
SCALE, HITBOX = sized(0.5, HEIGHT, 1.4)
KIND = "biped"
K = 4
LOOK = "a little white egg-shaped piglet with a cracked shell rim, dot eyes, long drooping pink ears, pink hooves and a curly tail"
BASE = {"white": (250, 250, 252), "white_dark": (210, 210, 220), "pink": (230, 90, 130), "pink_dark": (170, 40, 80),
        "eye": (20, 20, 24), "crack": (120, 120, 130), "mouth": (220, 80, 110)}
SHINY = {"white": (250, 236, 190), "white_dark": (210, 190, 130), "pink": (120, 160, 230), "pink_dark": (60, 100, 180)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        if abs(b - 13.0 - (1.0 if int(a + 10) % 2 else -0.6) * (abs(a) % 1.6) * 0.6) < 0.25 and abs(a) < 5.0:
            return p["crack"], None
        for sx in (-1, 1):
            if math.hypot(a - sx * 1.8, b - 10.6) < 0.6:
                return p["eye"], None
        if math.hypot(a, b - 8.6) < 0.7:
            return p["mouth"], None
    return skin(P, "white", dark="white_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("xiaomon")
    top = m.bone("xiaomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    ball(m, bd, (0, 10.0, 0), 6.0, bodyf, layers=6, ry=7.0)
    for sx in (-1, 1):
        m.box(bd, sx * 5.4 - 0.6, 4.0, -2.0, sx * 5.4 + 0.6, 11.0, 1.0, skin(P, "pink", dark="pink_dark"),
              rotation=(0, 0, sx * 12), pivot=(sx * 5.4, 11.0, 0))
    for sx, sz in ((1, -1), (-1, -1), (1, 1), (-1, 1)):
        m.round_box(top, sx * 2.6, sz * 2.4, 1.0, 1.0, 0.0, 3.6, skin(P, "pink", dark="pink_dark"), cut=0)
    tl = m.bone("tail", bd, (0, 8, 6))
    for i in range(6):
        ang = i * 1.0
        rod(m, tl, (2.0 * math.cos(ang), 8.0 + 2.0 * math.sin(ang), 6.6 + i * 0.3),
            (2.0 * math.cos(ang + 1.0), 8.0 + 2.0 * math.sin(ang + 1.0), 6.9 + i * 0.3), 1, solid(P, "pink"), extend=0.2)
    return m
