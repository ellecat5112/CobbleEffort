"""Eyesmon: Scatter Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): Eyesmon scattered into living shadow. A black flame-shaped spectre rising from a coiling pool of black
smoke, its head a crown of licking black flames with two huge slanted silver-rimmed eyes with red pupils, a small
jagged mouth with a purple tongue, and thin clawed arms reaching out. 15 blocks tall.

Front is -z, y is up. 58 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import cutout, flame_inside, local, solid
from _route import pal, tone

HEIGHT = 58
SCALE, HITBOX = sized(15, HEIGHT, 3.2)
KIND = "floater"
K = 3
LOOK = ("a black flame-shaped spectre rising from a coiling pool of black smoke, with a crown of black flames, two huge "
        "slanted silver-rimmed red eyes, a small jagged mouth and thin clawed arms")
BASE = {"black": (22, 20, 26), "black_light": (70, 66, 80), "silver": (200, 200, 210), "pupil": (220, 30, 40),
        "white": (240, 240, 240), "tooth": (250, 248, 240), "tongue": (130, 60, 170)}
SHINY = {"black": (230, 230, 236), "black_light": (255, 255, 255), "pupil": (60, 120, 230)}


def P(v):
    return pal(BASE, SHINY, v)


def blackf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["black_light"] if face == "up" else p["black"], face), None


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            u, v = (x - sx * 4.0) * (1 if sx > 0 else -1), y - 36.0
            ru, rv = u * math.cos(0.5) - v * math.sin(0.5), u * math.sin(0.5) + v * math.cos(0.5)
            d = math.hypot(ru / 3.2, rv / 1.4)
            if d < 1.0:
                if math.hypot(ru, rv) < 0.7:
                    return p["pupil"], p["pupil"]
                return tone(p["white"] if d < 0.75 else p["silver"], face), None
        if 29.0 < y < 31.0 and abs(x) < 1.6:
            if abs(y - 30.0) < 0.3:
                return tone(p["tongue"], face), None
            return tone(p["tooth"] if (x * 2) % 1.0 < 0.5 else p["black"], face), None
    return blackf(x, y, z, face, variant, box=box, **k)


def flamef(x, y, z, face, variant, box=None, **k):
    return blackf(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("eyesmonscattermode")
    top = m.bone("eyesmonscattermode", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    for i in range(8):                                                               # coiling pool of smoke
        ang = 2 * math.pi * i / 8
        r = 7.0 + (i % 3) * 2.0
        m.round_box(bd, r * math.cos(ang), r * math.sin(ang), 3.0, 2.4, 0.0, 2.0 + (i % 2), blackf, cut=1)
    m.round_box(bd, 0, 0, 3.0, 2.6, 2.0, 16.0, blackf, cut=1)                         # rising stem
    m.round_box(bd, 0, 0, 5.0, 3.6, 16.0, 26.0, blackf, cut=1)
    hd = m.bone("head", bd, (0, 26, 0))
    m.round_box(hd, 0, 0, 8.0, 3.6, 26.0, 40.0, facef, cut=2)                         # face
    for i in range(5):                                                               # crown of black flames
        x = -8.0 + i * 4.0
        h = 14.0 + abs(i - 2) * 3.0                                                  # the outer ones rise like horns
        lean = 0.25 * (i - 2) / 2
        for ang in (0, 90):
            m.box(hd, x - 4.0, 38.0, 0, x + 4.0, 38.0 + h, 0, cutout(flame_inside(3, lean, i, base=0.55), flamef),
                  rotation=(0, ang, 0), pivot=(x, 38.0, 0))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # thin clawed arms
        ab = m.bone(nm, bd, (sx * 5.0, 22.0, 0))
        rod(m, ab, (sx * 5.0, 22.0, 0), (sx * 11.0, 20.0, -2.0), 1, blackf, extend=0.4, t2=2)
        rod(m, ab, (sx * 11.0, 20.0, -2.0), (sx * 14.0, 24.0, -3.0), 1, blackf, extend=0.4, t2=2)
        for j in range(3):
            spike(m, ab, (sx * 14.0, 24.0, -3.0), (sx * 0.6, 0.4 + (j - 1) * 0.6, -0.4), 0.7, 3.0, blackf, tip=0.2)
    return m
