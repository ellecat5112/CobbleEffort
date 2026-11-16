"""Armagemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Armageddon that ends the Digital World, made of countless Digimon fused together. Here in its
crawling form: a long armoured black-violet body of segmented plates, a small fanged head with cold blue eye-slits,
a long segmented tail and spindly jointed legs ending in hooked claws. 35 blocks tall.

Front is -z, y is up. 48 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, slab_z
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(35, HEIGHT, 3.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a crawling armoured horror of segmented black-violet plates with a small fanged head, blue eye-slits, a long "
        "segmented tail and spindly jointed legs with hooked claws")
BASE = {"plate": (60, 50, 80), "plate_dark": (20, 16, 30), "plate_light": (130, 116, 170), "eye": (90, 170, 255),
        "fang": (230, 226, 236)}
SHINY = {"plate": (110, 30, 30), "plate_dark": (50, 10, 10), "plate_light": (200, 90, 90), "eye": (255, 220, 60)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "plate", "plate_dark", light="plate_light", seams=(1.4,))
LIMB = metal(P, "plate", dark="plate_dark", light="plate_light", streak=2.0)


def build():
    m = Model("armagemon")
    top = m.bone("armagemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 26, 0))
    for i in range(6):                                           # the segmented thorax
        z0 = -10 + i * 3.6
        slab_z(m, bd, 0, 28.0 - i * 0.6, z0, z0 + 3.8, 6.0 - abs(i - 2) * 0.5, 4.6, PLATE)
    hd = m.bone("head", bd, (0, 27, -11))
    m.round_box(hd, 0, -14.0, 3.4, 3.0, 24.0, 30.0, PLATE, cut=1)
    for sx in (-1, 1):
        m.box(hd, sx * 1.6 - 0.8, 28.0, -17.1, sx * 1.6 + 0.8, 28.6, -16.9, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 1.6, 24.4, -16.0), (0, -1, -0.3), 0.9, 2.4, solid(P, "fang"))
        spike(m, hd, (sx * 2.6, 30.0, -13.0), (sx * 0.4, 1, 0.6), 1.2, 3.6, LIMB)
    tl = m.bone("tail", bd, (0, 26, 11))
    p = (0, 26.0, 11.0)
    for j in range(10):                                          # long segmented tail curving up and back
        q = (0, p[1] + 1.4 + j * 0.2, p[2] + 3.0 - j * 0.15)
        m.round_box(tl, 0, (p[2] + q[2]) / 2, 1.8 - j * 0.1, 1.4, p[1] - 1.2, p[1] + 1.4, PLATE, cut=1)
        p = q
    spike(m, tl, p, (0, 0.6, 1), 1.2, 3.0, LIMB)
    for i in range(3):                                           # six spindly legs
        zz = -7.0 + i * 7.0
        for sx in (1, -1):
            nm = f"leg_{i}_{'left' if sx > 0 else 'right'}"
            lg = m.bone(nm, top, (sx * 5.0, 25.0, zz))
            knee = (sx * 16.0, 40.0, zz + (i - 1) * 4.0)
            ankle = (sx * 22.0, 14.0, zz + (i - 1) * 8.0)
            foot = (sx * 24.0, 0.6, zz + (i - 1) * 9.0)
            for a_, b_ in (((sx * 5.0, 25.0, zz), knee), (knee, ankle), (ankle, foot)):
                rod(m, lg, a_, b_, 2, LIMB, extend=0.4)
            for d in ((sx * 0.6, -0.3, -1), (sx * 0.6, -0.3, 1), (sx, -0.3, 0)):
                spike(m, lg, foot, d, 1.0, 2.6, LIMB)
    return m
