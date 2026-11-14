"""Sakekoi, the Sake Cup Pokémon (Water), a Liquor Meadows Pokémon (the user's design): a serene porcelain-white koi
with soft vermilion patches, a round vermilion sakazuki (ceremonial cup) with a gold rim on its forehead, flowing
translucent fins, long barbels and a sweeping tail.

Shiny: black lacquer with gold patches.

Front is -z, y is up. 10 units tall, 28 long; baseScale 0.55 (0.55 m). A floater (it swims).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, rod
from _liquor import palette
from _route import tone

SHINY = {"porcelain": (40, 36, 44), "porcelain_shade": (26, 24, 30), "vermilion": (236, 190, 70)}
P, solid, ramp = palette(SHINY)
SCALE = 0.55
HITBOX = [0.9, 0.6]
KIND = "floater"
K = 5
HEIGHT = 10
LOOK = "a serene porcelain-white koi with vermilion patches, a vermilion sake cup with a gold rim on its forehead and flowing fins"
CUT = (0, 0, 0, 0)


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west", "up") and math.sin(z * 0.55 + 1.0) + math.cos(x * 1.3 + z * 0.3) > 1.1:
        return tone(p["vermilion"], face), None                               # koi patches
    if face == "down":
        return p["porcelain_shade"], None
    return tone(p["porcelain"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up":
        d = math.hypot(x, z + 9.4)
        if d < 1.6:
            return p["vermilion"], None                                       # the sakazuki on its forehead
        if d < 2.1:
            return p["gold"], None
    if face in ("east", "west") and abs(y - 5.4) < 0.6 and abs(z + 10.6) < 0.6:
        return p["pupil"], None
    return bodyf(x, y, z, face, variant)


def finf(x, y, z, face, variant, **k):
    p = P(variant)
    c = p["vermilion"] if (int(abs(x) * 2 + y * 2 + z * 2) % 5 == 0) else p["porcelain"]
    return c[:3] + (200,), None


def build() -> Model:
    m = Model("sakekoi")
    top = m.bone("sakekoi", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    for z0, z1, rx, ry in ((-8.0, -4.0, 2.8, 2.8), (-4.0, 1.0, 3.2, 3.2), (1.0, 5.0, 2.6, 2.6), (5.0, 8.0, 1.8, 1.8)):
        m.box(bd, -rx, 4.6 - ry, z0, rx, 4.6 + ry, z1, bodyf)
        m.box(bd, -rx + 0.8, 4.6 - ry - 0.6, z0, rx - 0.8, 4.6 + ry + 0.6, z1, bodyf)
    hd = m.bone("head", bd, (0, 5, -8))
    m.box(hd, -2.4, 2.4, -11.6, 2.4, 6.6, -7.6, headf)
    m.box(hd, -1.6, 2.8, -12.6, 1.6, 4.8, -11.4, solid("porcelain_shade"))       # the mouth
    for sx in (-1, 1):
        chain(m, hd, [(sx * 1.2, 3.0, -12.2), (sx * 2.4, 2.0, -13.4), (sx * 3.0, 1.0, -13.0)], [0.6, 0.5],
              solid("porcelain_shade"))                                          # barbels
    tl = m.bone("tail", bd, (0, 5, 8))
    m.box(tl, 0.0, 0.6, 7.4, 0.0, 9.0, 14.6, finf)                               # the sweeping tail fin
    m.box(bd, 0.0, 7.0, -3.0, 0.0, 9.6, 4.0, finf)                               # dorsal fin
    for sx, side in ((-1, "left"), (1, "right")):
        fn = m.bone(f"arm_{side}", bd, (sx * 3, 3, -4))
        x0, x1 = sorted((sx * 3.0, sx * 7.0))
        m.box(fn, x0, 2.6, -5.0, x1, 2.6, -1.4, finf, rotation=(0, 0, -sx * 20), pivot=(sx * 3.0, 2.6, -3.0))
    return m
