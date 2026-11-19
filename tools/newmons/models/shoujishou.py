"""Shoujishou (a Digimon of the CobbleEffort: Digital crossover; built after the manga panel on wikimon.net, its only
picture): a little flip-phone scout of the Shou: a boxy grey mobile-phone body with a glowing screen face, a keypad
belly, a stubby antenna, little gloved arms and legs. 1 block.

Front is -z, y is up. 24 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(1, HEIGHT, 1.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a little flip-phone scout: a boxy grey phone body with a glowing screen face, a keypad belly, a stubby antenna and gloved limbs"
BASE = {"grey": (170, 174, 186), "grey_dark": (90, 94, 108), "screen": (150, 220, 160), "black": (24, 24, 28),
        "key": (240, 240, 246), "white": (250, 250, 250)}
SHINY = {"grey": (220, 120, 160), "grey_dark": (150, 60, 100)}


def P(v):
    return pal(BASE, SHINY, v)


CASE = armour(P, "grey", "grey_dark")


def screenf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 1.0, y - 19.0) < 0.5:
                return tone(p["black"], face), None
        if abs(y - 17.4) < 0.2 and abs(x) < 1.2:
            return tone(p["black"], face), None
        return p["screen"], p["screen"]
    return CASE(x, y, z, face, variant, box=box, **k)


def keyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and (x % 1.4) < 0.9 and (y % 1.4) < 0.9:
        return tone(p["key"], face), None
    return CASE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("shoujishou")
    top = m.bone("shoujishou", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.box(bd, -3.0, 6.0, -1.6, 3.0, 14.0, 1.6, keyf)                                         # keypad half
    hd = m.bone("head", bd, (0, 14, 0))
    m.box(hd, -3.0, 14.0, -1.4, 3.0, 22.0, 1.6, screenf)                                     # screen half
    m.box(hd, -2.4, 15.0, -1.6, 2.4, 21.0, -1.4, screenf)
    rod(m, hd, (2.0, 22.0, 0), (2.4, 25.0, 0), 1, metal(P, "black"), extend=0.2, t2=1)       # antenna
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.0, 12.0, 0))
        rod(m, ab, (sx * 3.0, 12.0, 0), (sx * 5.6, 9.0, -1.0), 1, solid(P, "black"), extend=0.2, t2=2)
        ball(m, ab, (sx * 6.0, 8.6, -1.2), 1.2, solid(P, "white"), layers=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.6, 6.0, 0))
        rod(m, lg, (sx * 1.6, 6.0, 0), (sx * 1.8, 1.4, 0), 1, solid(P, "black"), extend=0.2, t2=2)
        m.round_box(lg, sx * 1.8, -0.6, 1.4, 2.0, 0.0, 1.6, solid(P, "white"), cut=0)
    return m
