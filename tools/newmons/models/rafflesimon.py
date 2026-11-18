"""Rafflesimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a queen of carnivorous flowers in a towering gown of crimson petals: a high spiked collar and
puffed petal sleeves studded with thorns, a jagged crown and red mask, long lavender hair, a great flared skirt of
layered red petals over an inner gown of dark-rose panels dotted with glowing rainbow pores, and drifting rainbow
petal wings about her shoulders. 35 blocks.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, fabric, metal, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a queen of carnivorous flowers in a towering gown of crimson petals with a spiked collar, a jagged crown and rainbow petal wings"
BASE = {"red": (210, 40, 50), "red_dark": (120, 14, 24), "rose": (150, 40, 70), "rose_dark": (70, 14, 30),
        "pink": (240, 170, 190), "gold": (230, 190, 70), "gold_dark": (150, 100, 20), "lavender": (200, 160, 230),
        "lavender_dark": (140, 100, 180), "black": (30, 24, 30), "pore1": (120, 220, 250), "pore2": (250, 220, 120),
        "pore3": (200, 140, 250), "wing": (220, 240, 250, 150)}
SHINY = {"red": (60, 120, 220), "red_dark": (20, 50, 140), "rose": (40, 70, 150), "rose_dark": (14, 24, 70)}


def P(v):
    return pal(BASE, SHINY, v)


PETAL = armour(P, "red", "red_dark", trim="gold", trim_w=0.2)


def gownf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face not in ("up", "down"):
        row = math.floor(y / 1.6)
        u = (x + z) * 0.8 + (row % 2) * 1.2
        if (y % 1.6) < 0.7 and (u % 2.4) < 1.6:
            c = (p["pore1"], p["pore2"], p["pore3"])[int(abs(u) // 2.4 + row) % 3]
            return c, c
    return fabric(P, "rose", "rose_dark", axis="y", period=2.0)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("rafflesimon")
    mats = {"skin": PETAL, "neck": solid(P, "black"), "hand": solid(P, "black"), "finger": solid(P, "black")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.8, leg_bulk=0.8, name="rafflesimon")
    m.boxes[:] = [b for b in m.boxes if b.bone not in ("leg_left", "leg_right")]
    m.bones[:] = [b for b in m.bones if b["name"] not in ("leg_left", "leg_right")]
    bd = a["body"]
    for i in range(9):                                                                   # inner gown
        r = 4.0 + i * 1.6
        m.round_box(bd, 0, 1.0, r, r * 0.9, 32.0 - (i + 1) * 3.6, 32.0 - i * 3.6 + 0.2, gownf, cut=max(1, round(r * 0.3)))
    for j in range(12):                                                                  # outer petal skirt
        ang = 2 * math.pi * j / 12
        if math.sin(ang) < -0.7:
            continue
        c = (12.0 * math.cos(ang), 16.0, 1.0 + 11.0 * math.sin(ang))
        m.box(bd, c[0] - 4.0, 0.0, c[2], c[0] + 4.0, 30.0, c[2], PETAL,
              rotation=(math.sin(ang) * 20, -math.degrees(ang) + 90, 0), pivot=(c[0], 30.0, c[2]))
    for sx in (-1, 1):                                                                   # puffed petal sleeves
        for j in range(3):
            spike(m, a["arm_left" if sx > 0 else "arm_right"]["bone"], (sx * (8.0 + j * 1.4), 46.0 - j * 4.0, 0),
                  (sx * 1, -0.3, 0.2 * (j - 1)), 3.0, 9.0, PETAL, tip=0.8)
        for j in range(4):
            spike(m, bd, (sx * (3.0 + j * 1.4), 53.0, 1.0), (sx * 0.3, 1, 0.4), 1.2, 5.0, PETAL, tip=0.8)   # spiked collar
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.6, 54.0, 60.0, solid(P, "pink"), cut=1)
    m.round_box(hd, 0, -2.6, 2.6, 0.8, 56.4, 58.4, solid(P, "red"), cut=0)                 # red mask
    for j in range(7):                                                                   # jagged crown
        spike(m, hd, (-2.4 + j * 0.8, 60.0, -0.6), ((j - 3) * 0.1, 1, 0), 0.9, 2.6 + (j % 2) * 1.4,
              metal(P, "gold", dark="gold_dark"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, sx * 2.6 - 0.8, 44.0, -1.0, sx * 2.6 + 0.8, 59.0, 2.6, strands(P, "lavender", "lavender_dark"))
    wb = m.bone("wings", bd, (0, 52, 4))                                                 # rainbow petal wings
    for sx in (-1, 1):
        for j in range(3):
            x0, x1 = sorted((sx * 8.0, sx * (18.0 + j * 2.0)))
            m.box(wb, x0, 52.0 + j * 4.0, 5.0 + j, x1, 60.0 + j * 4.0, 5.0 + j, solid(P, "wing", glow=True),
                  rotation=(0, -sx * 20, sx * 20 * (j - 1)), pivot=(sx * 8.0, 56.0, 5.0))
    return m
