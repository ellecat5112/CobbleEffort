"""CobbleEffortian Gengar (Ghost/Fire), after @tomats_art's art: a squat orange body with a huge white-toothed grin, a
black bat-winged mask across its face with two slanted yellow eyes and a third eye on its forehead, two great red
horns, and a wild mane of red-and-yellow flames sweeping back over its head and down its sides, with flame tufts on
its short arms and legs.

Shiny: pale blue with cyan flames.

Front is -z, y is up. 28 units tall; baseScale 0.95 (1.6 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _hellfire import P, flame_shader, flames, solid
from _route import tone

SCALE = 0.95
HITBOX = [1.6, 1.65]
KIND = "biped"
K = 3
HEIGHT = 28
LOOK = ("a squat orange body with a huge toothy grin, a black bat-winged mask with two yellow eyes and a third on its "
        "forehead, two red horns and a wild red-and-yellow flame mane")


def facef(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        if (x * x) / 0.7 + (y - 18.6) ** 2 / 0.9 < 1:
            return p["iris"], p["iris"]                                           # the third eye
        for sx in (-1, 1):
            dx, dy = x - sx * 2.0, y - 15.8
            if dx * dx / 1.2 + (dy + sx * dx * 0.35) ** 2 / 0.45 < 1:
                return (p["pupil"] if abs(dx) < 0.25 else p["iris"]), p["iris"]   # slanted yellow eyes
        band = 15.0 < y < 17.6 + 0.35 * abs(x) and abs(x) < 4.8 or (abs(x) < 1.3 and y < 19.8 and y > 15.0)
        if band:
            return p["mask"], None                                                 # the bat-winged mask
        if 11.4 < y < 13.8 and abs(x) < 4.2 - 0.25 * abs(y - 12.6):
            if abs(y - 12.6) < 0.12 or int((x + 5) * 1.3) % 2 == 0 and abs(y - 12.6) < 1.1:
                return p["pupil"], None                                            # tooth gaps
            return p["white"], None                                                # the grin
    return tone(p["red"] if y > 14.0 else p["orange"], face), None


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["orange"] if face != "down" else p["orange_dark"], face), None


def build() -> Model:
    m = Model("gengar_cobbleeffortian")
    top = m.bone("gengar_cobbleeffortian", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    m.round_box(bd, 0, 0.6, 6.0, 5.0, 3.0, 11.0, bodyf, cut=1.8)                   # the squat orange body
    hd = m.bone("head", bd, (0, 11, 0))
    m.round_box(hd, 0, -0.4, 5.4, 4.6, 10.4, 20.2, facef, cut=1.8)
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.6, 19.8, -0.4), (sx * 0.35, 1, 0.25), 2.4, 7.4, solid("red"), tip=1.2)    # great horns
    mn = m.bone("mane", hd, (0, 18, 3))
    flames(m, mn, (0, 19.0, 2.4), 5, 13.0, 3.4, spread=0.42, up=(0, 0.9, 1.1))     # the mane sweeping back
    for sx in (-1, 1):
        flames(m, mn, (sx * 5.0, 15.0, 1.0), 3, 9.0, 3.0, spread=0.5, up=(sx * 1.2, 0.4, 0.6))   # side flames
        flames(m, mn, (sx * 5.4, 10.4, 0.4), 2, 4.0, 2.0, spread=0.5, up=(sx * 1.0, -0.4, 0.3))
    tl = m.bone("tail", bd, (0, 6, 5))
    flames(m, tl, (0, 6.0, 5.4), 3, 6.0, 2.4, spread=0.5, up=(0, 0.6, 1.2))           # a flame tail
    for sx, side in ((-1, "left"), (1, "right")):
        ar = m.bone(f"arm_{side}", bd, (sx * 6, 9, -1))
        m.round_box(ar, sx * 7.2, -1.2, 1.6, 1.6, 6.0, 9.6, bodyf, cut=0.6)
        flames(m, ar, (sx * 7.4, 9.0, -0.6), 2, 2.4, 1.2, spread=0.6, up=(sx * 0.8, 1, 0.4))
        for i in range(3):
            spike(m, ar, (sx * (6.6 + i * 0.6), 6.2, -2.4), (0, -0.4, -1), 0.6, 1.2, solid("white"))   # little claws
        lb = m.bone(f"leg_{side}", top, (sx * 3, 3, 0))
        m.round_box(lb, sx * 3.4, -0.2, 2.0, 2.2, 0.0, 4.0, bodyf, cut=0.7)
        for i in range(3):
            spike(m, lb, (sx * 3.4 + (i - 1) * 1.1, 0.6, -2.2), (0, 0, -1), 0.8, 1.2, solid("white"))  # toes
    return m
