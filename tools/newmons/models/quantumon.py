"""Quantumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a floating oracle in a great white robe with wide sleeves hemmed in gold circuit traces and dark
lining, a red tie, long teal hair and a pink veil under a golden mask-crown with four rods, golden gauntlet hands
weaving glowing numbers, and two golden rings of light circling beneath it. 35 blocks.

Front is -z, y is up. 60 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fabric, metal, solid, strands
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "a floating oracle in a great white circuit-hemmed robe with a golden mask-crown, teal hair, a pink veil and glowing numbers"
BASE = {"white": (246, 246, 252), "white_dark": (190, 190, 210), "gold": (236, 200, 80), "gold_dark": (160, 120, 30),
        "dark": (40, 36, 50), "red": (200, 30, 50), "teal": (50, 170, 160), "teal_dark": (20, 100, 100),
        "pink": (220, 100, 180), "pink_dark": (150, 50, 120), "glow": (250, 220, 120), "digit": (200, 150, 250)}
SHINY = {"white": (40, 40, 56), "white_dark": (16, 16, 24), "teal": (220, 80, 160), "teal_dark": (140, 30, 90)}


def P(v):
    return pal(BASE, SHINY, v)


def robef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if y < 8.0 or (face == "north" and abs(x) < 0.8 and y < 50.0):
        if abs((x + z) % 2.0 - 1.0) < 0.2 or abs(y % 2.0 - 1.0) < 0.15:
            return tone(p["gold"], face), p["gold"]
        return tone(p["dark"], face), None
    return fabric(P, "white", "white_dark", axis="y", period=3.0)(x, y, z, face, variant, box=box, **k)


GOLD = metal(P, "gold", dark="gold_dark")


def build():
    m = Model("quantumon")
    mats = {"skin": robef, "hand": GOLD, "finger": GOLD, "neck": solid(P, "red")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.8, leg_bulk=0.8, name="quantumon")
    m.boxes[:] = [b for b in m.boxes if b.bone not in ("leg_left", "leg_right")]
    m.bones[:] = [b for b in m.bones if b["name"] not in ("leg_left", "leg_right")]
    bd = a["body"]
    for i in range(8):                                                                   # great flared robe skirt
        t = i / 7
        r = 4.4 + 10.0 * t
        m.round_box(bd, 0, 0.4, r, r * 0.9, 34.0 - (i + 1) * 4.0, 34.0 - i * 4.0 + 0.2, robef,
                    cut=max(1, round(r * 0.35)))
    m.box(bd, -0.8, 40.0, -4.4, 0.8, 50.0, -4.0, solid(P, "red"))                          # red tie
    for side in ("arm_left", "arm_right"):                                               # wide sleeves
        e = a[side]["elbow"]
        sx = 1 if side == "arm_left" else -1
        m.round_box(a[side]["bone"], e[0] + sx * 1.0, e[2], 3.6, 3.6, e[1] - 10.0, e[1] - 2.0, robef, cut=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.6, 54.0, 60.0, solid(P, "dark"), cut=1)
    m.round_box(hd, 0, -2.6, 2.6, 0.8, 54.6, 60.0, GOLD, cut=0)                            # golden mask
    m.box(hd, -1.6, 57.0, -3.5, 1.6, 57.6, -3.3, solid(P, "glow", glow=True))
    for j in range(4):                                                                   # four crown rods
        x = -2.4 + j * 1.6
        rod(m, hd, (x, 60.0, -1.0), (x, 66.0, -1.0), 1, GOLD, extend=0.2)
        m.box(hd, x - 0.6, 66.0, -1.6, x + 0.6, 67.2, -0.4, GOLD)
    m.box(hd, -3.6, 61.0, -1.6, 3.6, 62.0, -0.4, GOLD)
    for sx in (-1, 1):                                                                   # teal hair + pink veil
        m.box(hd, sx * 2.6 - 0.8, 36.0, -1.6, sx * 2.6 + 0.8, 58.0, 1.6, strands(P, "teal", "teal_dark"))
        m.box(hd, sx * 3.4 - 0.6, 40.0, -0.6, sx * 3.4 + 0.6, 61.0, 3.0, fabric(P, "pink", "pink_dark", axis="y"))
    m.box(hd, -3.4, 44.0, 2.6, 3.4, 61.0, 3.4, fabric(P, "pink", "pink_dark", axis="y"))
    for j in range(8):                                                                   # glowing numbers
        ang = 2 * math.pi * j / 8
        cx, cy, cz = 14.0 * math.cos(ang), 46.0 + 8.0 * math.sin(ang * 1.5), 14.0 * math.sin(ang) - 4.0
        m.box(bd, cx - 0.4, cy - 1.0, cz, cx + 0.4, cy + 1.0, cz, solid(P, "digit" if j % 2 else "glow", glow=True))
    rb = m.bone("ring_halo", a["top"], (0, -1, 0))                                       # rings of light below
    for r in (8.0, 12.0):
        for i in range(16):
            ang = 2 * math.pi * i / 16
            m.box(rb, r * math.cos(ang) - 1.0, -0.2, r * math.sin(ang) - 1.0, r * math.cos(ang) + 1.0, 0.6,
                  r * math.sin(ang) + 1.0, solid(P, "glow", glow=True))
    return m
