"""Hiyarimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
Baby II ghostly drop of snow-white slime with a big dark eye, a bluish icy frill dripping from its lips, little ice
claws at its base and puddles round it. Half a block tall.

Front is -z, y is up. 16 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import gem, skin, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.5, HEIGHT, 1.6)
KIND = "floater"
K = 4
LOOK = "a ghostly drop of snow-white slime with big dark eyes, an icy dripping frill and little ice claws"
BASE = {"white": (236, 244, 252), "white_dark": (180, 200, 230), "eye": (40, 30, 50), "shine": (250, 250, 255),
        "ice": (150, 210, 250), "ice_light": (230, 250, 255)}
SHINY = {"white": (240, 220, 250), "white_dark": (200, 170, 220), "ice": (250, 170, 220)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.0, y - 10.0)
            if d < 0.4:
                return tone(p["shine"], face), None
            if d < 1.2:
                return tone(p["eye"], face), None
    return skin(P, "white", dark="white_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("hiyarimon")
    top = m.bone("hiyarimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    m.round_box(bd, 0, 0.6, 6.0, 4.4, 0.0, 6.0, bodyf, cut=2)
    m.round_box(bd, 0, 0, 4.6, 4.0, 5.0, 14.0, bodyf, cut=2)
    hd = m.bone("head", bd, (0, 12, 0))
    m.round_box(hd, 0, -4.2, 3.0, 0.8, 6.4, 8.0, gem(P, "ice", "ice_light", glow=False), cut=0)   # icy frill
    spike(m, hd, (-2.4, 6.4, -4.4), (0, -1, 0), 1.0, 2.4, gem(P, "ice", "ice_light", glow=False), tip=0.8)
    for j in range(4):
        spike(m, bd, ((j - 1.5) * 2.4, 0.6, -4.4), (0, -0.4, -1), 0.8, 1.6, gem(P, "ice", "ice_light", glow=False))
    return m
