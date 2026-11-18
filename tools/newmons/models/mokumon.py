"""Mokumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little puff of grey smoke with glowing pale eyes, a red grinning mouth, a small flame flickering on
its crown and wisps curling away below. 0.35 blocks tall.

Front is -z, y is up. 14 units tall; Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import cutout, flame_inside, local, skin, solid
from _route import pal, tone

HEIGHT = 14
SCALE, HITBOX = sized(0.35, HEIGHT, 1.2)
KIND = "floater"
K = 3
LOOK = "a little puff of grey smoke with glowing pale eyes, a red grinning mouth and a small flame on its crown"
BASE = {"smoke": (170, 170, 176), "smoke_dark": (110, 110, 118), "eye": (250, 240, 170), "mouth": (220, 50, 50),
        "fire": (255, 160, 50, 215), "fire_core": (255, 240, 170, 235)}
SHINY = {"smoke": (200, 170, 220), "smoke_dark": (140, 100, 170)}


def P(v):
    return pal(BASE, SHINY, v)


SMOKE = skin(P, "smoke", dark="smoke_dark", var=0.06)


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if v / max(H, 1e-6) < 0.4 else p["fire"]
    return c, c[:3]


def build():
    m = Model("mokumon")
    top = m.bone("mokumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 7.0, 0), 4.6, SMOKE, layers=4, ry=4.2)
    for i in range(6):                                                                   # cloudy lumps
        a = 2 * math.pi * i / 6
        ball(m, bd, (4.0 * math.cos(a), 7.0 + 3.0 * math.sin(a), 1.0), 1.8, SMOKE, layers=2)
    for sx in (-1, 1):
        ball(m, bd, (sx * 1.6, 8.0, -4.0), 0.9, solid(P, "eye", glow=True), layers=2)
    m.round_box(bd, 0, -4.2, 1.4, 0.4, 5.0, 6.2, solid(P, "mouth"), cut=0)
    for ang in (0, 90):
        m.box(bd, -1.4, 11.0, 0, 1.4, 14.0, 0, cutout(flame_inside(3, 0.0, 1), firef), rotation=(0, ang, 0),
              pivot=(0, 11.0, 0))
    pts = [(0, 3.0, 1.0), (-1.0, 1.0, 1.4), (0.6, 0.0, 1.6)]
    for p0, p1 in zip(pts, pts[1:]):                                                     # wisps below
        rod(m, bd, p0, p1, 1, SMOKE, extend=0.2)
    return m
