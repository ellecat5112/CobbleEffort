"""Devidramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the evil dragon. A gaunt, hunched black dragon of glossy segmented hide, four glowing red eyes in a
long fanged head with a white mane, ragged black bat wings, bandaged wrists, enormous hands with long red claws and a
long tail ending in a black spade. 15 blocks tall.

Front is -z, y is up. 48 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing, theropod
from _digidetail import cutout, fabric, local, noise2, skin, solid, strands
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a gaunt hunched black dragon with four glowing red eyes, a fanged head, ragged bat wings, bandaged wrists, "
        "huge red-clawed hands and a spade-tipped tail")
BASE = {"black": (50, 50, 58), "black_dark": (12, 12, 16), "black_light": (140, 140, 156), "red": (220, 30, 40),
        "red_light": (255, 140, 140), "bandage": (200, 180, 140), "bandage_dark": (130, 110, 80), "mane": (230, 230, 236),
        "mane_dark": (150, 150, 160), "mouth": (190, 30, 40), "tooth": (250, 250, 246)}
SHINY = {"black": (40, 60, 120), "black_dark": (10, 20, 60), "black_light": (120, 150, 220)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = skin(P, "black", dark="black_dark", light="black_light", var=0.06)
BAND = fabric(P, "bandage", "bandage_dark", axis="y", period=1.2)


def wingf(x, y, z, face, variant, box=None, **k):
    return tone(P(variant)["black"], face), None


def tatter(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return noise2(u * 0.6, v * 0.6, 23) < 0.8


def build():
    m = Model("devidramon")
    mats = {"skin": HIDE, "belly": HIDE, "neck": HIDE, "head": HIDE, "snout": HIDE, "jaw": HIDE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "arm": HIDE, "hand": HIDE, "claw": solid(P, "red"),
            "thigh": HIDE, "shin": HIDE, "foot": HIDE, "talon": solid(P, "red"), "tail": HIDE, "tail_tip": HIDE}
    a = theropod(m, mats, "devidramon", hip_y=16.0, hip_z=3.0, chest=(0, 28.0, -4.0), body_r=5.6, chest_r=6.2,
                 neck_top=(0, 36.0, -7.0), head_len=10.0, head_w=3.6, head_h=4.0, mouth_open=24, teeth=6, arm_len=14.0,
                 arm_bulk=1.3, leg_bulk=1.3, stance=4.4,
                 tail=((0, 16, 8), (3, 10, 14), (5, 4, 18), (6, 1, 24), (6, 2, 30)), tail_r=(3.0, 2.2, 1.6, 1.2, 0.8))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):                                                    # four red eyes
        for j in range(2):
            m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.3 - j * 1.2, ez - 0.6 + j * 1.6, max(sx * ex, sx * (ex + 0.3)),
                  ey + 0.4 - j * 1.2, ez + 0.6 + j * 1.6, solid(P, "red", glow=True))
    for i in range(7):                                                    # white mane
        rod(m, hd, ((i - 3) * 0.7, ey + 1.6, ez + 2.0), ((i - 3) * 1.2, ey - 2.0, ez + 8.0), 1,
            strands(P, "mane", "mane_dark"), extend=0.3)
    for nm in ("arm_left", "arm_right"):                                  # bandages + huge claws
        ar = a[nm]
        h = ar["hand"]
        m.round_box(ar["bone"], h[0], h[2], 2.0, 2.0, h[1] + 1.0, h[1] + 3.6, BAND, cut=1)
        for j in range(4):
            spike(m, ar["bone"], (h[0] + (j - 1.5) * 1.1, h[1] - 1.0, h[2] - 1.0), (0, -1, -0.3), 0.9, 6.0,
                  solid(P, "red"), tip=0.25)
    e = a["tail_pts"][-1]                                                 # spade tail tip
    m.box(a["tail_tip"], e[0] - 2.0, e[1] - 0.4, e[2], e[0] + 2.0, e[1] + 0.4, e[2] + 4.0, HIDE)
    spike(m, a["tail_tip"], (e[0], e[1], e[2] + 4.0), (0, 0, 1), 2.0, 2.6, HIDE)
    for side in (1, -1):                                                  # ragged bat wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 32.0, 2.0))
        bat_wing(m, wb, (side * 3.0, 32.0, 2.0), 22.0, 22.0, 4, HIDE, cutout(tatter, wingf), side=side, sweep=25)
    return m
