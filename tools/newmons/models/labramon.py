"""Labramon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
loyal puppy: a sitting white dog with long floppy magenta ears, red eyes with pink cheek stripes, a tiny fang, a white
chest ruff, cream claws and a big spiral magenta tail. Child stage, 1 block tall.

Front is -z, y is up. 28 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fur, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1.0, HEIGHT, 2.0)
KIND = "quadruped"
K = 4
LOOK = "a sitting white puppy with long floppy magenta ears, red eyes, pink cheek stripes and a big spiral magenta tail"
BASE = {"white": (246, 246, 250), "white_dark": (180, 182, 196), "magenta": (200, 90, 140), "magenta_dark": (140, 40, 90),
        "eye": (200, 30, 40), "pink": (240, 120, 150), "nose": (40, 30, 40), "claw": (240, 230, 190), "tooth": (250, 250, 250)}
SHINY = {"magenta": (90, 150, 230), "magenta_dark": (40, 90, 170)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "white", "white_dark", length=0.8)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.6) < 0.5 and abs(y - 22.4) < 0.5:
                return tone(p["eye"], face), None
            if abs(y - 21.0 + (sx * x - 2.0) * 0.4) < 0.15 and 1.4 < sx * x < 2.8:
                return tone(p["pink"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def tailf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["magenta_dark"] if (y * 1.3 + z) % 2.0 < 0.5 else p["magenta"], face), None


def build():
    m = Model("labramon")
    top = m.bone("labramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 1.4, 3.6, 4.0, 3.0, 13.0, FUR, cut=2)                         # sitting body
    m.round_box(bd, 0, -2.2, 2.8, 0.8, 9.0, 14.0, FUR, cut=1)                        # chest ruff
    hd = m.bone("head", bd, (0, 14, -1))
    m.round_box(hd, 0, -0.6, 3.0, 3.0, 17.0, 25.0, headf, cut=1)
    m.round_box(hd, 0, -4.2, 1.8, 1.4, 17.6, 21.0, FUR, cut=1)                        # muzzle
    m.box(hd, -0.7, 20.0, -5.7, 0.7, 21.0, -5.5, solid(P, "nose"))
    spike(m, hd, (1.0, 18.0, -5.4), (0, -1, -0.2), 0.8, 1.2, solid(P, "tooth"), tip=0.8)
    for sx in (-1, 1):                                                               # floppy ears
        m.round_box(hd, sx * 3.6, 0.6, 1.0, 2.0, 15.0, 24.0, fur(P, "magenta", "magenta_dark"), cut=0)
    for sx, nm in ((1, "leg_front_left"), (-1, "leg_front_right")):
        lg = m.bone(nm, bd, (sx * 2.0, 10.0, -2.0))
        rod(m, lg, (sx * 2.0, 10.0, -2.0), (sx * 2.2, 1.0, -3.0), 1, FUR, extend=0.3, t2=2)
        for j in range(3):
            spike(m, lg, (sx * 2.2 + (j - 1) * 0.7, 0.6, -4.0), (0, -0.2, -1), 0.8, 1.6, solid(P, "claw"), tip=0.8)
    for sx, nm in ((1, "leg_back_left"), (-1, "leg_back_right")):
        lg = m.bone(nm, bd, (sx * 3.4, 4.0, 3.0))
        m.round_box(lg, sx * 3.6, 1.0, 1.6, 3.4, 0.0, 4.0, FUR, cut=1)
    tb = m.bone("tail", bd, (0, 6, 5))                                               # spiral tail
    for i in range(10):
        a0, a1 = i * 0.6, (i + 1) * 0.6
        r0, r1 = 4.0 - i * 0.3, 4.0 - (i + 1) * 0.3
        rod(m, tb, (0, 9.0 + r0 * math.sin(a0), 9.0 + r0 * math.cos(a0)), (0, 9.0 + r1 * math.sin(a1), 9.0 + r1 * math.cos(a1)),
            2 if i < 5 else 1, tailf, extend=0.4)
    return m
