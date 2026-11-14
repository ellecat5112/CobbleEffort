"""Ashtraylor, the Ashtray Pokémon (Ground/Rock), the Nicodex's Ground type (the user's design): a sluggish, heavy
tortoise whose shell is a massive, chipped ceramic ashtray basin, filled with grey ash, crushed butts and a few
glowing embers; cigarette-rest notches on its rim, stubby stone legs and a sleepy face.

Shiny: a blue glazed basin.

Front is -z, y is up. 18 units tall; baseScale 0.85 (0.95 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _nico import palette, tube_z
from _route import tone

SHINY = {"tan": (90, 140, 200), "ivory_shade": (60, 100, 160)}
P, solid, ramp = palette(SHINY)
SCALE = 0.85
HITBOX = [1.7, 1.15]
KIND = "quadruped"
K = 3
HEIGHT = 18
LOOK = "a heavy tortoise whose shell is a chipped ceramic ashtray basin full of ash, butts and glowing embers"


def basinf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west", "north", "south") and abs(y - 12.6) < 0.5:
        return p["ivory"], None                                               # a glazed rim band
    return tone(p["tan"], face), None


def ashf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up":
        h = math.sin(x * 2.3 + z * 1.1) + math.cos(x * 0.7 - z * 2.9)
        if h > 1.6:
            return p["ember"], p["ember"]                                     # glowing embers
        if h > 1.1:
            return p["ember_hot"], p["ember_hot"]
        if h < -1.2:
            return p["ash_dark"], None
    return p["ash"], None


def skinf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(y - 7.6) < 0.4 and abs(x) > 0.4 and abs(x) < 1.6:
        return p["pupil"], None                                               # sleepy slit eyes
    return tone(p["ash_dark"], face), None


def build() -> Model:
    m = Model("ashtraylor")
    top = m.bone("ashtraylor", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 9.0, 9.0, 4.0, 13.0, basinf, cut=3.0)                 # the ceramic basin shell
    m.round_box(bd, 0, 0, 7.4, 7.4, 12.0, 13.4, ashf, cut=2.4)                  # ash heaped inside
    for x, z, a in ((2.0, -1.0, 0.4), (-2.6, 2.0, -0.8), (0.6, 3.4, 1.6)):     # crushed butts
        tube_z(m, bd, x, 13.6, 0.6, z - 1.6, z + 1.6, solid("filter"))
    for d in (-1, 1):                                                           # cigarette-rest notches
        m.box(bd, -1.0, 12.4, d * 9.0 - (0.6 if d > 0 else 0), 1.0, 13.4, d * 9.0 + (0.6 if d < 0 else 0),
              solid("ash_dark"))
    hd = m.bone("head", bd, (0, 7, -9))
    m.round_box(hd, 0, -11.0, 2.4, 2.4, 4.6, 9.0, skinf, cut=0.8)
    tl = m.bone("tail", bd, (0, 6, 9))
    rod(m, tl, (0, 6.0, 8.6), (0, 5.0, 11.4), 1.4, solid("ash_dark"), extend=0.2)
    for sx, side in ((-1, "left"), (1, "right")):
        for role, z in (("front", -5.6), ("back", 5.6)):
            lb = m.bone(f"leg_{role}_{side}", top, (sx * 6, 5, z))
            m.round_box(lb, sx * 6.4, z, 2.0, 2.0, 0.0, 5.6, solid("ash_dark"), cut=0.8)
    return m
