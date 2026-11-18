"""Kohagurumon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
little gear Digimon: one round steel cog with eight square teeth and a dark round face plate split down the middle,
with two big red-ringed eyes. Baby II stage (no level on wikimon), half a block tall.

Front is -z, y is up. 16 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model
from _digi import sized
from _digidetail import metal, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.5, HEIGHT, 1.2)
KIND = "floater"
K = 4
LOOK = "a little steel cog with eight square teeth, a dark split face plate and two big red-ringed eyes"
BASE = {"steel": (200, 204, 214), "steel_dark": (110, 114, 126), "dark": (50, 52, 60), "red": (220, 40, 40),
        "white": (250, 250, 250), "eye": (20, 20, 24)}
SHINY = {"steel": (230, 190, 90), "steel_dark": (160, 120, 30)}


def P(v):
    return pal(BASE, SHINY, v)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.8, y - 8.0)
            if d < 0.5:
                return tone(p["eye"], face), None
            if d < 1.0:
                return tone(p["red"], face), p["red"]
            if d < 1.4:
                return tone(p["white"], face), None
        if abs(x) < 0.2:
            return tone(p["eye"], face), None
    return tone(p["dark"], face), None


def build():
    m = Model("kohagurumon")
    top = m.bone("kohagurumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    STEEL = metal(P, "steel", dark="steel_dark")
    for i in range(8):                                                               # disc of slabs + teeth
        ang = 180.0 * i / 8
        m.box(bd, -6.0, 6.6, -1.6, 6.0, 9.4, 1.6, STEEL, rotation=(0, 0, ang), pivot=(0, 8.0, 0))
        m.box(bd, -7.6, 7.0, -1.4, 7.6, 9.0, 1.4, STEEL, rotation=(0, 0, ang + 11.25), pivot=(0, 8.0, 0))
    m.round_box(bd, 0, -1.6, 4.0, 0.6, 4.0, 12.0, facef, cut=0)
    return m
