"""Lianpumon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
mask showman: a squat figure wrapped in a huge red-lined black cape with a gold rim, hung all over with masks (a clock
face, a pumpkin, a skull, a panda, a fanged oni), a white smiling mask face with red markings and blue ribbons, a fur
collar and two big gloves, one red with gold claws and one grey. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fabric, fur, leather, metal, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 4.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 4}
LOOK = "a squat figure in a huge red-lined black cape hung with masks, a white smiling mask face, a fur collar and big red and grey gloves"
BASE = {"black": (36, 34, 40), "black_dark": (12, 12, 14), "red": (200, 30, 40), "red_dark": (120, 10, 18),
        "gold": (240, 200, 70), "gold_dark": (160, 120, 20), "white": (246, 242, 230), "white_dark": (190, 180, 160),
        "blue": (60, 80, 200), "grey": (120, 120, 130), "grey_dark": (60, 60, 70), "fur": (220, 210, 190),
        "fur_dark": (160, 150, 130), "orange": (240, 140, 40), "panda": (240, 240, 240), "eye": (30, 30, 34)}
SHINY = {"black": (40, 60, 120), "black_dark": (14, 20, 60), "red": (220, 170, 40), "red_dark": (150, 100, 10)}


def P(v):
    return pal(BASE, SHINY, v)


def maskf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.4) < 0.7 and abs(y - 29.4) < 0.4:
                return tone(p["eye"], face), None
            if abs(x - sx * 1.4) < 0.2 and 27.6 < y < 31.0:
                return tone(p["red"], face), None
        if abs(y - 26.6 + 0.2 * x * x) < 0.3 and abs(x) < 2.4:
            return tone(p["eye"], face), None
    return skin(P, "white", dark="white_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("lianpumon")
    top = m.bone("lianpumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    CAPE = fabric(P, "black", "black_dark")
    for j in range(5):                                                               # huge caped body
        r = 11.0 - j * 1.4
        m.round_box(bd, 0, 1.0, r, r * 0.8, j * 4.6, j * 4.6 + 5.2, CAPE, cut=max(1, int(r * 0.35)))
    m.round_box(bd, 0, 1.0, 11.4, 9.2, 0.0, 1.4, metal(P, "gold", dark="gold_dark"), cut=3)          # gold rim
    m.round_box(bd, 0, 2.0, 11.2, 8.4, 1.0, 4.0, fabric(P, "red", "red_dark"), cut=3)                # red lining
    masks = [(-6.0, 12.0, "gold"), (-3.0, 6.0, "orange"), (2.6, 7.0, "panda"), (6.0, 13.0, "white"), (-1.0, 16.0, "red")]
    for (mx, my, key) in masks:                                                     # hanging masks
        m.round_box(bd, mx, -7.0 + abs(mx) * 0.2, 1.8, 0.6, my - 1.8, my + 1.8, solid(P, key), cut=0)
        m.box(bd, mx - 0.8, my, -7.8 + abs(mx) * 0.2, mx - 0.2, my + 0.6, -7.6 + abs(mx) * 0.2, solid(P, "eye"))
        m.box(bd, mx + 0.2, my, -7.8 + abs(mx) * 0.2, mx + 0.8, my + 0.6, -7.6 + abs(mx) * 0.2, solid(P, "eye"))
    m.round_box(bd, 0, 0, 7.0, 6.0, 22.0, 25.0, fur(P, "fur", "fur_dark"), cut=2)                   # fur collar
    hd = m.bone("head", bd, (0, 25, 0))
    m.round_box(hd, 0, -1.6, 3.4, 2.0, 24.6, 32.4, maskf, cut=1)
    for sx in (-1, 1):                                                               # blue ribbons
        rod(m, hd, (sx * 2.4, 26.0, -2.4), (sx * 3.4, 18.0, -3.6), 1, fabric(P, "blue", "blue"), extend=0.2, t2=2)
    m.round_box(hd, 0, -3.8, 1.0, 0.4, 32.0, 33.4, solid(P, "gold"), cut=0)
    ar = m.bone("arm_right", bd, (-8.0, 26.0, -2.0))                                 # big red glove, raised
    m.round_box(ar, -11.0, -4.0, 3.6, 2.4, 30.0, 37.0, leather(P, "red", "red_dark"), cut=1)
    for j in range(4):
        spike(m, ar, (-12.6 + j * 1.2, 37.0, -4.0), (-0.2, 1, 0), 1.0, 3.0, leather(P, "red", "red_dark"), tip=0.8)
        spike(m, ar, (-12.6 + j * 1.2, 39.6, -4.0), (-0.2, 1, 0), 0.8, 1.4, metal(P, "gold", dark="gold_dark"), tip=0.8)
    al = m.bone("arm_left", bd, (8.0, 24.0, -2.0))                                    # grey glove
    m.round_box(al, 9.0, -6.0, 3.2, 2.4, 22.0, 28.0, leather(P, "grey", "grey_dark"), cut=1)
    return m
