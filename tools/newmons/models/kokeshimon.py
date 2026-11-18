"""Kokeshimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
kokeshi doll: a cylindrical wooden doll in a long violet kimono patterned with gold and red, a black obi, a round head
with a straight black bob, violet side locks, round yellow eyes and rosy cheeks, a red bow with tassels, and two
floating kokeshi-doll arms in violet sleeves. 15 blocks tall.

Front is -z, y is up. 44 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fabric, skin, solid, strands
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(15, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = "a cylindrical kokeshi doll in a long violet kimono with a black bob, round yellow eyes, a red bow and two floating doll arms"
BASE = {"violet": (120, 60, 170), "violet_dark": (60, 20, 100), "gold": (240, 200, 60), "red": (210, 40, 50),
        "black": (30, 28, 34), "black_dark": (10, 10, 12), "face": (250, 236, 220), "face_dark": (210, 190, 170),
        "eye": (240, 210, 40), "pupil": (24, 20, 20), "cheek": (240, 140, 140), "wood": (220, 180, 120),
        "white": (250, 250, 250)}
SHINY = {"violet": (40, 130, 120), "violet_dark": (10, 70, 60)}


def P(v):
    return pal(BASE, SHINY, v)


def kimonof(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 0.4:
        return tone(p["red"], face), None
    if (y % 6.0) < 0.4:
        return tone(p["gold"], face), None
    return fabric(P, "violet", "violet_dark")(x, y, z, face, variant, box=box, **k)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.6, y - 32.0)
            if d < 0.5:
                return tone(p["pupil"], face), None
            if d < 1.1:
                return tone(p["eye"], face), None
            if math.hypot(x - sx * 2.6, y - 30.4) < 0.6:
                return tone(p["cheek"], face), None
        if abs(y - 29.6) < 0.25 and abs(x) < 0.4:
            return tone(p["red"], face), None
    return skin(P, "face", dark="face_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("kokeshimon")
    top = m.bone("kokeshimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    m.round_box(bd, 0, 0, 5.0, 4.4, 0.0, 26.0, kimonof, cut=2)
    m.round_box(bd, 0, 0, 5.2, 4.6, 16.0, 19.4, solid(P, "black"), cut=2)                  # obi
    hd = m.bone("head", bd, (0, 26, 0))
    m.round_box(hd, 0, 0, 4.4, 4.0, 26.0, 35.6, facef, cut=2)
    m.round_box(hd, 0, 0.8, 4.8, 3.6, 33.0, 37.4, strands(P, "black", "black_dark"), cut=2)   # bob
    m.round_box(hd, 0, -3.8, 4.4, 0.4, 34.0, 35.6, strands(P, "black", "black_dark"), cut=0)   # fringe
    for sx in (-1, 1):
        m.round_box(hd, sx * 4.6, 0.4, 0.8, 1.6, 27.0, 33.0, strands(P, "violet", "violet_dark"), cut=0)
        m.round_box(hd, sx * 2.0, 0.4, 1.6, 0.8, 37.0, 38.6, solid(P, "red"), cut=0)            # bow
        m.round_box(hd, sx * 4.0, -1.0, 0.6, 0.6, 33.0, 36.0, solid(P, "red"), cut=0)           # tassels
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # floating doll arms
        ab = m.bone(nm, bd, (sx * 10.0, 20.0, 0))
        rod(m, ab, (sx * 7.0, 16.0, 0), (sx * 14.0, 22.0, -2.0), 3, kimonof, extend=0.4)
        m.round_box(ab, sx * 15.0, -2.4, 1.6, 1.6, 22.0, 25.4, skin(P, "wood", dark="face_dark"), cut=1)
    return m
