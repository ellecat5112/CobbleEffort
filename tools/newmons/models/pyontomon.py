"""Pyontomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a leaping jackalope: a tan rabbit with a cream belly and face, long ears and golden forked
antlers, sly eyes, black-socked feet, a long navy scarf marked with a red star and moon streaming behind, and one
fist blazing with golden light. 1 block.

Front is -z, y is up. 34 units tall; Child stage (no level on wikimon; by analogy).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, fur, metal, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(1, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a tan jackalope with golden forked antlers, a long navy star-marked scarf, black-socked feet and a blazing golden fist"
BASE = {"tan": (200, 140, 70), "tan_dark": (140, 90, 30), "cream": (250, 240, 220), "cream_dark": (210, 196, 170),
        "black": (30, 28, 30), "navy": (40, 50, 120), "navy_dark": (16, 20, 70), "red": (210, 40, 50),
        "gold": (240, 200, 70), "gold_dark": (170, 120, 20), "glow": (250, 230, 100), "eye": (60, 140, 90)}
SHINY = {"tan": (160, 160, 176), "tan_dark": (96, 96, 112)}


def P(v):
    return pal(BASE, SHINY, v)


def furf(x, y, z, face, variant, box=None, **k):
    if face == "north" and abs(x) < 2.0 and 10.0 < y < 18.0:
        return fur(P, "cream", "cream_dark", length=1.0)(x, y, z, face, variant, box=box, **k)
    return fur(P, "tan", "tan_dark", length=1.2)(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.5) < 0.8 and abs(y - 22.4 + (x * sx - 1.5) * 0.3) < 0.35:
                return tone(p["eye"], face), None
        if abs(x) < 1.6 and y < 21.6:
            return tone(p["cream"], face), None
    return furf(x, y, z, face, variant, box=box, **k)


def scarff(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "south") and abs((x + y + z) % 8.0 - 4.0) < 0.6:
        return tone(p["red"], face), None
    return fabric(P, "navy", "navy_dark", axis="x", period=2.0)(x, y, z, face, variant, box=box, **k)


GOLD = metal(P, "gold", dark="gold_dark")


def build():
    m = Model("pyontomon")
    top = m.bone("pyontomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 0, 3.0, 2.6, 9.0, 18.0, furf, cut=1)
    m.round_box(bd, 0, 0, 3.4, 3.0, 17.0, 19.0, scarff, cut=1)                             # scarf
    pts = [(-2.0, 18.0, 2.6), (-8.0, 22.0, 6.0), (-14.0, 26.0, 7.0)]
    for p0, p1 in zip(pts, pts[1:]):
        m.box(bd, min(p0[0], p1[0]), min(p0[1], p1[1]), p0[2], max(p0[0], p1[0]), max(p0[1], p1[1]) + 1.6, p0[2],
              scarff)
    m.box(bd, 1.0, 19.0, 3.0, 9.0, 21.0, 3.0, scarff, rotation=(0, 0, 50), pivot=(1.0, 19.0, 3.0))
    hd = m.bone("head", bd, (0, 19, 0))
    ball(m, hd, (0, 22.0, -0.2), 3.0, headf, layers=3, ry=3.0)
    m.round_box(hd, 0, -2.8, 1.4, 1.0, 19.8, 21.6, headf, cut=0)
    for sx in (-1, 1):
        m.round_box(hd, sx * 1.6, 0.6, 0.9, 0.9, 24.0, 31.0, furf, cut=0)                  # long ears
        pts = [(sx * 1.0, 24.6, 0), (sx * 3.4, 29.0, 0.6), (sx * 4.0, 33.0, 0.6)]
        for p0, p1 in zip(pts, pts[1:]):                                                  # golden antlers
            rod(m, hd, p0, p1, 1, GOLD, extend=0.2)
        spike(m, hd, pts[1], (sx * 1, 0.6, 0), 0.8, 2.4, GOLD, tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.0, 17.0, 0))
        rod(m, ab, (sx * 3.0, 17.0, 0), (sx * 6.0, 15.0, -3.0), 1, furf, extend=0.2, t2=2)
        ball(m, ab, (sx * 6.6, 14.6, -3.6), 1.4, furf, layers=2)
    ball(m, "arm_right", (-6.6, 14.6, -5.0), 2.6, solid(P, "glow", glow=True), layers=2)     # blazing fist
    for j in range(6):
        ang = 2 * math.pi * j / 6
        spike(m, "arm_right", (-6.6, 14.6, -5.0), (math.cos(ang), math.sin(ang), -0.3), 0.8, 4.0,
              solid(P, "glow", glow=True), tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.8, 9.0, 0))
        rod(m, lg, (sx * 1.8, 9.0, 0.4), (sx * 2.0, 4.0, 1.6), 2, furf, extend=0.3)
        rod(m, lg, (sx * 2.0, 4.0, 1.6), (sx * 2.0, 1.0, 0.0), 1, solid(P, "black"), extend=0.2, t2=2)
        m.round_box(lg, sx * 2.0, -1.6, 1.2, 2.6, 0.0, 1.4, solid(P, "cream"), cut=0)
    return m
