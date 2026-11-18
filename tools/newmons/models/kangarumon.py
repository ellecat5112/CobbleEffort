"""Kangarumon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
boxing kangaroo: a golden-yellow kangaroo with white chevron stripes on its arms and legs, big red boxing gloves, huge
red boots, a long thick tail, a dark blue cap with a white feather over its little blue joey (who peeks out of the
pouch on its belly) and a confident grin. 15 blocks tall.

Front is -z, y is up. 48 units tall; Adult stage (Armor).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, leather, skin, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a golden-yellow boxing kangaroo with white chevron stripes, big red gloves and boots, a long tail and a joey in its pouch"
BASE = {"gold": (240, 190, 70), "gold_dark": (180, 120, 24), "white": (250, 248, 240), "red": (210, 40, 40),
        "red_dark": (130, 14, 18), "navy": (40, 50, 110), "blue": (100, 130, 200), "blue_dark": (50, 70, 140),
        "eye": (30, 24, 24), "nose": (60, 40, 30)}
SHINY = {"gold": (180, 130, 90), "gold_dark": (110, 70, 40), "red": (60, 150, 80), "red_dark": (20, 80, 30)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "gold", "gold_dark", length=1.2)


def stripef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face != "down" and (y + abs(x) * 0.8) % 4.0 < 0.8:
        return tone(p["white"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("kangarumon")
    top = m.bone("kangarumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    m.round_box(bd, 0, 0.6, 5.6, 4.6, 16.0, 34.0, FUR, cut=2)
    m.round_box(bd, 0, -4.2, 3.4, 1.0, 18.0, 24.0, skin(P, "white", dark="gold"), cut=1)           # pouch
    jb = m.bone("joey", bd, (0, 24, -5))                                              # the joey peeking out
    m.round_box(jb, 0, -5.2, 1.6, 1.4, 23.6, 26.6, skin(P, "blue", dark="blue_dark"), cut=0)
    m.box(jb, -1.0, 25.4, -6.7, 1.0, 25.9, -6.6, solid(P, "eye"))
    hd = m.bone("head", bd, (0, 34, -1))
    m.round_box(hd, 0, -1.4, 3.4, 3.6, 34.0, 41.0, FUR, cut=1)
    m.round_box(hd, 0, -5.4, 2.0, 1.4, 34.6, 37.6, FUR, cut=1)
    m.box(hd, -0.8, 36.6, -6.9, 0.8, 37.6, -6.7, solid(P, "nose"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.2, sx * 2.4), 38.4, -5.1, max(sx * 1.2, sx * 2.4), 39.2, -4.9, solid(P, "eye"))
        m.round_box(hd, sx * 2.6, 1.0, 0.8, 1.4, 40.0, 45.0, FUR, cut=0)                         # ears
    m.round_box(hd, 0, -0.6, 3.6, 3.6, 40.4, 42.6, solid(P, "navy"), cut=1)                       # dark cap
    m.round_box(hd, 0, -4.2, 2.8, 1.0, 40.4, 41.0, solid(P, "navy"), cut=0)
    spike(m, hd, (2.4, 42.0, 0), (0.6, 1, 0.6), 0.9, 4.0, solid(P, "white"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # red boxing gloves
        ab = m.bone(nm, bd, (sx * 5.6, 31.0, 0))
        rod(m, ab, (sx * 5.6, 31.0, 0), (sx * 9.0, 26.0, -3.0), 2, stripef, extend=0.4)
        m.round_box(ab, sx * 10.0, -5.0, 3.4, 3.6, 22.0, 29.0, leather(P, "red", "red_dark"), cut=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                              # huge red boots
        lg = m.bone(nm, top, (sx * 3.4, 16.0, 0))
        rod(m, lg, (sx * 3.4, 17.0, 0), (sx * 4.0, 8.0, 1.0), 3, stripef, extend=0.6)
        m.round_box(lg, sx * 4.4, -2.4, 3.4, 6.0, 0.0, 8.0, leather(P, "red", "red_dark"), cut=2)
    tb = m.bone("tail", bd, (0, 18, 4))
    pts = [(0, 18.0, 4.0), (0, 10.0, 10.0), (0, 3.0, 18.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tb, p0, p1, 3 - j, FUR, extend=0.6)
    return m
