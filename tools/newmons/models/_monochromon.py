"""Shared builder for Monochromon and Monochromon (X-Antibody) (CobbleEffort: Digital; hand-built after the official
art on wikimon.net): a stocky four-legged horned dinosaur with a hide of grey and black patches, a white-scaled
underside, one great black horn on its snout, red-tipped spikes along its armoured back, green eyes, a toothy jaw and
heavy clawed feet. The X-Antibody ("x"): black armour plating, a towering blade-like horn edged red, steel claws and a
curved blade on its tail.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import quadruped
from _digidetail import armour, metal, scales, solid
from _route import pal, tone

BASE = {"grey": (150, 150, 158), "grey_dark": (70, 70, 78), "black": (44, 42, 48), "black_dark": (16, 16, 20),
        "belly": (236, 236, 240), "red": (200, 40, 40), "horn": (50, 50, 56), "steel": (200, 204, 214),
        "steel_dark": (100, 104, 116), "eye": (60, 190, 100), "mouth": (150, 30, 40), "tooth": (250, 250, 240)}
SHINY = {"grey": (200, 170, 120), "grey_dark": (140, 100, 50), "black": (110, 70, 40), "black_dark": (60, 30, 14)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    HIDE0 = scales(P, "grey", "grey_dark", size=1.6)
    ARM = armour(P, "black", "black_dark", trim="red", trim_w=0.2)

    def hidef(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "down":
            return tone(p["belly"], face), None
        if x:
            return ARM(xx, y, z, face, variant, box=box, **k)
        if math.sin(xx * 0.6 + 1.3) * math.sin(z * 0.45) + 0.4 * math.sin(y * 0.7) > 0.55:
            return tone(p["black"], face), None
        return HIDE0(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        mats = {"skin": hidef, "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"),
                "claw": metal(P, "steel") if x else solid(P, "black")}
        a = quadruped(m, mats, name, length=32.0, body_y=16.0, body_rx=7.0, body_ry=6.4, chest_bulk=1.2,
                      neck=((0, 20, -14), (0, 21, -17)), head_len=11.0, head_w=4.2, head_h=4.4, snout=0.7,
                      mouth_open=18, teeth=6, leg_bulk=1.7, toes=3,
                      tail=((0, 18, 16), (0, 16, 22), (0, 13, 28)), tail_r=(3.0, 2.2, 1.4))
        bd, hd = a["body"], a["head"]
        ex, ey, ez = a["eye"]
        sf = a["snout_front"]
        for sx in (-1, 1):
            m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4,
                  ez + 0.6, solid(P, "eye"))
        if not x:                                                                  # one great snout horn
            spike(m, hd, (0, ey + 1.0, sf + 3.0), (0, 1, -0.25), 3.0, 12.0, solid(P, "horn"), tip=0.8)
        else:                                                                      # towering blade horn
            m.box(hd, -0.8, ey + 1.0, sf + 1.0, 0.8, ey + 20.0, sf + 8.0, ARM, rotation=(-15, 0, 0),
                  pivot=(0, ey + 1.0, sf + 4.0))
            spike(m, a["tail"], a["tail_pts"][-1], (0, 1, 0.6), 1.6, 8.0, metal(P, "steel", dark="steel_dark"),
                  tip=0.8)
        for j in range(6):                                                         # red-tipped back spikes
            for sx in (-1, 1):
                spike(m, bd, (sx * 3.0, 21.6, -10.0 + j * 4.0), (sx * 0.3, 1, 0.2), 1.6, 3.6, solid(P, "red"), tip=0.8)
        return m

    return build
