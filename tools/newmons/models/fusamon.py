"""Fusamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
Baby I sleepy pup. A loaf-shaped blob of white fur with a shaggy deep-blue mane and back, a floppy blue ear on each
side, closed sleepy eyes, pink cheeks, a little black nose and tan eyebrow marks. 0.35 blocks tall.

Front is -z, y is up. 12 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fur, skin, solid
from _route import pal, tone

HEIGHT = 12
SCALE, HITBOX = sized(0.35, HEIGHT, 1.4)
KIND = "quadruped"
K = 4
ANIM = {"leg_amp": 2}
LOOK = "a loaf of white fur with a shaggy deep-blue back, floppy blue ears, closed sleepy eyes, pink cheeks and a black nose"
BASE = {"white": (248, 248, 252), "white_dark": (200, 204, 220), "blue": (40, 60, 160), "blue_dark": (16, 26, 90),
        "blue_light": (100, 130, 220), "line": (30, 30, 40), "cheek": (250, 170, 180), "nose": (30, 28, 30),
        "brow": (220, 170, 110)}
SHINY = {"blue": (230, 150, 40), "blue_dark": (160, 90, 10), "blue_light": (255, 210, 120)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = fur(P, "white", "white_dark", length=0.6, density=2.0)
BLUE = fur(P, "blue", "blue_dark", tip="blue_light", length=1.0, density=2.0)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(y - 6.0) < 0.2 and abs(x - sx * 2.6) < 1.0:
                return tone(p["line"], face), None
            if math.hypot(x - sx * 3.6, y - 4.8) < 0.8:
                return tone(p["cheek"], face), None
            if abs(y - 8.0) < 0.4 and abs(x - sx * 2.4) < 0.6:
                return tone(p["brow"], face), None
        if math.hypot(x, y - 4.8) < 0.6:
            return tone(p["nose"], face), None
    if (y > 8.6 and z > -3.0) or z > 3.0:
        return BLUE(x, y, z, face, variant, box=box, **k)
    return WHITE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("fusamon")
    top = m.bone("fusamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    m.round_box(bd, 0, 1.0, 5.6, 6.0, 0.0, 10.0, bodyf, cut=3)
    hd = m.bone("head", bd, (0, 8, -4))
    for sx in (-1, 1):                                                                  # floppy ears
        m.round_box(hd, sx * 5.0, -2.0, 1.2, 1.6, 6.6, 11.0, BLUE, cut=1)
    for j in range(7):                                                                  # shaggy back fur
        spike(m, bd, ((j - 3) * 1.2, 6.0 + j * 0.0, 7.0), ((j - 3) * 0.2, -0.2, 1), 1.4, 3.0 + (j % 2), BLUE, tip=0.3)
    for sx, nm in ((1, "leg_front_left"), (-1, "leg_front_right"), (1, "leg_back_left"), (-1, "leg_back_right")):
        m.bone(nm, top, (sx * 3.0, 1.0, -3.0 if "front" in nm else 4.0))
    return m
