"""Cutemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the healing rabbit. A small pale pink rabbit with long upright ears, a sleepy-kind face, round
headphones with a cross badge on each side, a long pink scarf wound round its neck with its ends trailing to the
ground, and little red shoes. Child stage.

Front is -z, y is up. 32 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, metal, skin, solid
from _route import pal, tone

HEIGHT = 32
SCALE, HITBOX = sized(1.0, HEIGHT, 0.9)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 14}
LOOK = ("a small pale pink rabbit with long upright ears, round headphones with cross badges, a long pink scarf and "
        "little red shoes")
BASE = {"pink": (250, 220, 236), "pink_dark": (220, 170, 200), "scarf": (240, 150, 190), "scarf_dark": (200, 100, 150),
        "blue": (60, 110, 200), "blue_dark": (30, 60, 140), "white": (250, 250, 252), "black": (30, 30, 36),
        "red": (220, 50, 50), "cross": (130, 160, 230)}
SHINY = {"pink": (220, 240, 250), "pink_dark": (170, 200, 230), "scarf": (130, 200, 240), "scarf_dark": (70, 140, 200)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "pink", dark="pink_dark", var=0.02)
SCARF = fabric(P, "scarf", "scarf_dark", axis="x", period=1.4)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 1.8, y - 20.4) < 0.7:
                return tone(p["black"], face), None
        if abs(y - 18.8) < 0.15 and abs(x) < 0.6:
            return tone(p["black"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("cutemon")
    top = m.bone("cutemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    m.round_box(bd, 0, 0.2, 3.6, 3.0, 4.0, 14.6, SKIN, cut=1)
    hd = m.bone("head", bd, (0, 15, 0))
    ball(m, hd, (0, 20.0, 0), 4.6, headf, layers=5)
    for sx in (-1, 1):                                                       # long upright ears
        rod(m, hd, (sx * 1.6, 24.0, 0.2), (sx * 2.6, 32.0, 0.6), 2, SKIN, extend=0.4, t2=1)
        m.round_box(hd, sx * 4.6, 0, 1.0, 2.0, 18.0, 22.0, metal(P, "blue", dark="blue_dark"), cut=1)   # headphones
        m.box(hd, min(sx * 5.4, sx * 5.8), 19.2, -0.8, max(sx * 5.4, sx * 5.8), 20.8, 0.8, solid(P, "cross"))
    rod(m, hd, (-4.6, 22.0, 0), (4.6, 22.0, 0), 1, solid(P, "white"), extend=0)     # headband over the top
    m.round_box(bd, 0, 0.0, 4.0, 3.4, 13.0, 15.6, SCARF, cut=1)                      # the long scarf
    for sx in (-1, 1):
        pts = [(sx * 3.0, 14.0, 1.0), (sx * 6.0, 10.0, 2.0), (sx * 7.0, 4.0, 2.4), (sx * 7.4, 0.6, 1.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, bd, p0, p1, 1, SCARF, extend=0.3, t2=3)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.6, 12.0, 0))
        rod(m, ab, (sx * 3.6, 12.0, 0), (sx * 4.6, 8.0, -0.6), 2, SKIN, extend=0.3)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.8, 4.0, 0))
        rod(m, lg, (sx * 1.8, 4.6, 0), (sx * 2.0, 1.4, 0), 2, SKIN, extend=0.3)
        m.box(lg, sx * 2.0 - 1.2, 0.0, -2.0, sx * 2.0 + 1.2, 1.4, 1.0, solid(P, "red"))
    return m
