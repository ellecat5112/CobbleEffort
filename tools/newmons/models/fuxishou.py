"""Fuxishou (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
gliding beast. A pale-pink flying-squirrel creature with a small rounded head, a dark eye and a little curled snout,
wide feathered gliding membranes along its sides striped with black tiger bars, two tall violet ear tufts swept back
and a curled spiral tail. Child stage, 1 block long.

Front is -z, y is up. 20 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fur, local, solid
from _route import pal, tone

HEIGHT = 20
SCALE, HITBOX = sized(1.0, HEIGHT, 1.8)
KIND = "floater"
K = 4
LOOK = ("a pale-pink flying-squirrel creature with a dark eye, wide feathered gliding membranes striped with black bars, "
        "tall violet ear tufts and a curled spiral tail")
BASE = {"pink": (240, 214, 210), "pink_dark": (190, 160, 160), "bar": (40, 36, 44), "violet": (130, 80, 180),
        "violet_dark": (70, 40, 110), "eye": (60, 40, 30), "shine": (240, 240, 240)}
SHINY = {"pink": (210, 230, 250), "pink_dark": (150, 170, 200), "violet": (60, 170, 200)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "pink", "pink_dark", length=0.8, density=2.0)


def barf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if abs((u * 0.7) % 2.6 - 1.3) < 0.35 and v < H * 0.8:
        return tone(p["bar"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west") and abs(y - 13.4) < 0.7 and abs(abs(x) - 1.8) < 0.7 and z < -4.0:
        return tone(p["eye"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("fuxishou")
    top = m.bone("fuxishou", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 1.0, 3.0, 6.0, 7.0, 13.0, barf, cut=2)
    hd = m.bone("head", bd, (0, 12, -5))
    m.round_box(hd, 0, -6.0, 2.6, 2.6, 10.0, 15.6, headf, cut=1)
    spike(m, hd, (0, 11.6, -8.4), (0, -0.4, -1), 1.4, 1.6, FUR, tip=0.4)               # curled snout
    for sx in (-1, 1):                                                                  # violet ear tufts
        for j in range(2):
            spike(m, hd, (sx * (1.0 + j * 0.8), 15.4, -5.0 + j * 1.0), (sx * 0.3, 1, 0.5), 1.0, 6.0 - j,
                  fur(P, "violet", "violet_dark", length=0.6), tip=0.2)
    for side in (1, -1):                                                                # feathered gliding membranes
        for j in range(4):
            x0, x1 = sorted((side * 2.6, side * (11.0 - j * 1.2)))
            m.box(bd, x0, 9.0 + j * 0.2, -4.0 + j * 2.6, x1, 9.4 + j * 0.2, -1.2 + j * 2.6, barf,
                  rotation=(0, side * (-10 + j * 12), side * 12), pivot=(side * 2.6, 9.2, -2.6 + j * 2.6))
            spike(m, bd, (side * (11.0 - j * 1.2), 9.2, -2.6 + j * 2.6), (side, 0, 0.4), 1.0, 2.6,
                  solid(P, "bar"), tip=0.3)
    tb = m.bone("tail", bd, (0, 8, 7))
    pts = [(0, 8.0, 7.0), (0, 5.0, 9.0), (0, 3.0, 11.0), (0, 3.6, 13.0), (0, 5.4, 12.6), (0, 5.0, 11.0)]
    for p0, p1 in zip(pts, pts[1:]):                                                    # spiral tail
        rod(m, tb, p0, p1, 1, FUR, extend=0.3, t2=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, bd, (sx * 1.6, 7.0, 0))
        rod(m, lg, (sx * 1.6, 7.0, -2.0), (sx * 1.8, 4.0, -3.0), 1, FUR, extend=0.2, t2=1)
        rod(m, lg, (sx * 1.6, 7.0, 3.0), (sx * 1.8, 4.0, 4.0), 1, FUR, extend=0.2, t2=1)
    return m
