"""Maquinamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
half-machine cat: a cream kitten whose right half is a stitched-on steel shell with a green targeting eye, a blue-
striped ear and tail, a collar with a gold bell, red stitch marks, and two jointed rocket arms of steel ending in red
nose cones and a green jet thruster. Child stage, 1 block tall.

Front is -z, y is up. 28 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fur, gem, metal, skin, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1.0, HEIGHT, 3.0)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 8}
LOOK = "a cream kitten with a stitched-on steel half and a green targeting eye, a blue-striped ear, a bell collar and steel rocket arms"
BASE = {"cream": (240, 226, 190), "cream_dark": (190, 170, 130), "steel": (200, 204, 216), "steel_dark": (100, 104, 116),
        "blue": (60, 100, 200), "red": (220, 40, 40), "green": (60, 200, 90), "green_light": (200, 255, 210),
        "gold": (240, 200, 60), "navy": (40, 40, 80), "eye": (24, 20, 20)}
SHINY = {"cream": (200, 200, 220), "cream_dark": (140, 140, 166)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "cream", "cream_dark", length=0.6)
STEEL = metal(P, "steel", dark="steel_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if x < 0:
        if face == "north" and math.hypot(x + 1.6, y - 18.0) < 1.2:
            return tone(p["green"], face), p["green"]
        return STEEL(x, y, z, face, variant, box=box, **k)
    if face == "north":
        if math.hypot(x - 1.6, y - 18.0) < 0.6:
            return tone(p["eye"], face), None
        if abs(x - 2.4) < 0.15 and 14.6 < y < 16.6:
            return tone(p["red"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("maquinamon")
    top = m.bone("maquinamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    m.round_box(bd, 0, 0.6, 3.0, 2.6, 5.0, 12.0, headf, cut=1)
    m.round_box(bd, 0, 0, 2.6, 2.4, 11.6, 12.6, solid(P, "navy"), cut=1)
    m.round_box(bd, 0, -2.4, 0.7, 0.7, 10.6, 12.0, metal(P, "gold", dark="steel_dark"), cut=0)
    hd = m.bone("head", bd, (0, 13, 0))
    m.round_box(hd, 0, 0, 3.8, 3.2, 12.6, 21.0, headf, cut=2)
    spike(m, hd, (2.6, 20.6, 0.4), (0.5, 1, 0.2), 1.8, 4.0, FUR, tip=0.8)
    spike(m, hd, (-2.6, 20.6, 0.4), (-0.5, 1, 0.2), 1.8, 4.0, STEEL, tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # steel rocket arms
        ab = m.bone(nm, bd, (sx * 3.0, 10.0, 0))
        rod(m, ab, (sx * 3.0, 10.0, 0), (sx * 7.0, 14.0 if sx < 0 else 6.0, 1.0), 2, STEEL, extend=0.4)
        rod(m, ab, (sx * 7.0, 14.0 if sx < 0 else 6.0, 1.0), (sx * 10.0, 20.0 if sx < 0 else 4.0, 1.0), 2, STEEL, extend=0.4)
        spike(m, ab, (sx * 10.0, 20.0 if sx < 0 else 4.0, 1.0), (sx * 0.4, 1 if sx < 0 else -0.2, 0), 1.8, 3.0, solid(P, "red"),
              tip=0.8)
    m.round_box(top, 11.0, 4.0, 1.2, 1.2, 1.0, 3.0, gem(P, "green", "green_light"), cut=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.6, 5.0, 0))
        rod(m, lg, (sx * 1.6, 5.4, 0), (sx * 1.8, 1.0, 0), 1, FUR if sx > 0 else STEEL, extend=0.3, t2=2)
        for j in range(2):
            spike(m, lg, (sx * 1.8 + (j - 0.5) * 0.8, 0.6, -0.6), (0, -0.2, -1), 0.8, 1.6, solid(P, "red"), tip=0.8)
    tb = m.bone("tail", bd, (0, 6, 2))
    pts = [(0, 6.0, 2.4), (-2.0, 9.0, 6.0), (-1.0, 13.0, 7.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 1, FUR, extend=0.3, t2=1)
    return m
