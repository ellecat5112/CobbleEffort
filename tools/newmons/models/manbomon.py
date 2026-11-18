"""Manbomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
Armor sunfish: a tall round silver-white sunfish body painted with blue swirls, a big round eye, pink pouting lips,
a tall dorsal fin and a lower fin, a little propeller at its back, and two big red boxing gloves on short arms.
15 blocks tall.

Front is -z, y is up. 34 units tall; Adult stage (Armor).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import leather, metal, skin, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "floater"
K = 3
LOOK = "a tall round silver-white sunfish painted with blue swirls, a big round eye, pink pouting lips, tall fins and red boxing gloves"
BASE = {"white": (236, 240, 246), "white_dark": (170, 176, 196), "blue": (60, 70, 170), "pink": (240, 150, 170),
        "red": (210, 40, 40), "red_dark": (120, 14, 18), "eye": (30, 30, 40), "grey": (150, 154, 166), "grey_dark": (70, 74, 86)}
SHINY = {"blue": (200, 60, 120), "white": (250, 236, 200)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("west", "east", "north"):
        r = math.hypot(z if face != "north" else x, y - 18.0)
        if face != "north" and math.hypot(z + 5.0, y - 20.0) < 1.6:
            return tone(p["eye"], face), None
        if abs((r - math.atan2(y - 18.0, z if face != "north" else x) * 1.2) % 3.0 - 1.5) < 0.35:
            return tone(p["blue"], face), None
    return skin(P, "white", dark="white_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("manbomon")
    top = m.bone("manbomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    for i in range(8):                                                               # tall disc body (side-on)
        ang = 180.0 * i / 8
        m.box(bd, -4.0, 10.0, -9.0, 4.0, 26.0, 9.0, bodyf, rotation=(ang, 0, 0), pivot=(0, 18.0, 0))
    m.round_box(bd, 0, -9.6, 1.8, 1.0, 14.0, 16.4, solid(P, "pink"), cut=0)          # pouting lips
    spike(m, bd, (0, 26.0, 2.0), (0, 1, 0.6), 2.0, 10.0, bodyf, tip=0.8)              # tall dorsal fin
    spike(m, bd, (0, 10.0, 2.0), (0, -1, 0.6), 2.0, 8.0, bodyf, tip=0.8)
    m.round_box(bd, 0, 9.6, 1.0, 1.0, 16.6, 19.4, metal(P, "grey", dark="grey_dark"), cut=0)   # propeller hub
    for j in range(3):
        m.box(bd, -0.3, 18.0, 10.0, 0.3, 21.0, 10.6, metal(P, "grey", dark="grey_dark"), rotation=(0, 0, j * 120), pivot=(0, 18.0, 10.3))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # boxing gloves
        ab = m.bone(nm, bd, (sx * 4.0, 13.0, -2.0))
        rod(m, ab, (sx * 4.0, 13.0, -2.0), (sx * 6.4, 10.0, -6.0), 1, skin(P, "blue", dark="blue"), extend=0.3, t2=1)
        m.round_box(ab, sx * 6.8, -8.0, 2.8, 3.0, 6.0, 11.0, leather(P, "red", "red_dark"), cut=2)
    return m
