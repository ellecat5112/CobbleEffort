"""Flybeemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the armoured hornet. A red-armoured insect warrior with a domed helmet, large dark compound eyes,
mandibles, thin black segmented arms and legs ending in claws, a ringed red-and-black abdomen with a sharp stinger
and four clear veined wings. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, local, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = ("a red-armoured hornet warrior with a domed helmet, dark compound eyes, mandibles, thin black clawed limbs, a "
        "ringed abdomen with a stinger and four clear veined wings")
BASE = {"red": (210, 40, 40), "red_dark": (120, 14, 18), "red_light": (255, 130, 120), "black": (34, 32, 38),
        "black_dark": (14, 14, 18), "eye": (40, 30, 50), "eye_light": (140, 120, 170), "steel": (200, 204, 214),
        "steel_dark": (100, 104, 116), "wing": (220, 240, 255, 100), "vein": (120, 140, 170, 200)}
SHINY = {"red": (240, 200, 40), "red_dark": (160, 110, 10), "red_light": (255, 240, 140)}


def P(v):
    return pal(BASE, SHINY, v)


RED = armour(P, "red", "red_dark", light="red_light", trim="black", trim_w=0.3)
BLACK = metal(P, "black", dark="black_dark")


def eyef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    on = (int(x * 1.6) + int(y * 1.6) + int(z * 1.6)) % 2
    return tone(p["eye_light"] if on else p["eye"], face), None


def ringf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (z * 0.5) % 2.0 < 0.6:
        return tone(p["black"], face), None
    return RED(x, y, z, face, variant, box=box, **k)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if (u % 2.6) < 0.25 or abs(v - H * 0.5) < 0.2:
        return p["vein"], None
    return p["wing"], None


def build():
    m = Model("flybeemon")
    top = m.bone("flybeemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    m.round_box(bd, 0, -1.0, 4.4, 3.6, 20.0, 30.0, RED, cut=1)                          # thorax
    ab_ = m.bone("abdomen", bd, (0, 20, 2))
    for j in range(5):                                                                   # ringed abdomen
        r = 4.4 - abs(j - 1.5) * 0.6
        m.round_box(ab_, 0, 3.0 + j * 2.6, r, r, 15.0 - j * 2.2, 15.0 - j * 2.2 + 2 * r, ringf, cut=1)
    spike(m, ab_, (0, 8.0, 15.0), (0, -0.8, 0.6), 1.6, 6.0, metal(P, "steel", dark="steel_dark"), tip=0.2)
    hd = m.bone("head", bd, (0, 30, -1))
    m.round_box(hd, 0, -1.0, 3.6, 3.4, 30.0, 37.0, RED, cut=2)                           # domed helmet
    spike(m, hd, (0, 36.6, -2.0), (0, 0.6, -1), 1.4, 3.0, RED, tip=0.3)
    for sx in (-1, 1):
        m.round_box(hd, sx * 2.6, -3.0, 1.4, 1.4, 31.6, 35.0, eyef, cut=0)               # compound eyes
        spike(m, hd, (sx * 1.2, 30.6, -4.0), (-sx * 0.4, -0.4, -1), 0.8, 2.6, BLACK, tip=0.2)   # mandibles
        rod(m, hd, (sx * 1.6, 36.6, -2.0), (sx * 4.0, 41.0, -4.0), 1, BLACK, extend=0.2, t2=1)  # antennae
    for side in (1, -1):                                                                 # four wings
        for j, (ang, ln) in enumerate(((20, 16.0), (-10, 12.0))):
            x0, x1 = sorted((side * 3.0, side * (3.0 + ln)))
            m.box(bd, x0, 28.0 - j * 2.0, 3.0 + j * 0.6, x1, 32.0 - j * 2.0, 3.0 + j * 0.6, wingf,
                  rotation=(0, side * 30, side * ang), pivot=(side * 3.0, 30.0, 3.0))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                  # thin clawed arms
        ab = m.bone(nm, bd, (sx * 4.4, 28.0, -1.0))
        rod(m, ab, (sx * 4.4, 28.0, -1.0), (sx * 8.0, 22.0, -3.0), 1, BLACK, extend=0.3, t2=1)
        rod(m, ab, (sx * 8.0, 22.0, -3.0), (sx * 8.0, 16.0, -6.0), 1, BLACK, extend=0.3, t2=1)
        for j in range(2):
            spike(m, ab, (sx * (8.0 + (j - 0.5) * 0.8), 16.0, -6.0), (0, -0.6, -1), 0.6, 2.4, BLACK, tip=0.2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                                  # dangling legs
        lg = m.bone(nm, bd, (sx * 2.4, 20.0, 0))
        for j, dz in enumerate((-1.0, 1.4)):
            rod(m, lg, (sx * 2.4, 20.0, dz), (sx * 5.0, 12.0, dz - 1.0), 1, BLACK, extend=0.3, t2=1)
            rod(m, lg, (sx * 5.0, 12.0, dz - 1.0), (sx * 4.4, 4.0, dz - 2.0), 1, BLACK, extend=0.3, t2=1)
    return m
