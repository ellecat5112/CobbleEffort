"""Bio Spinomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a Bio Hybrid spinosaur. An orange-red scaly body with a pale yellow belly, a long green crested
head with jagged teeth, a great sail of steel blades along its back, clawed arms and powerful legs with white talons.
35 blocks tall.

Front is -z, y is up. 62 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import theropod
from _digidetail import armour, eye, metal, scales, solid
from _route import pal, tone

HEIGHT = 62
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a Bio Hybrid spinosaur: an orange-red scaly body with a pale belly, a long green crested head with jagged "
        "teeth, a great sail of steel blades along its back and white talons")
BASE = {"orange": (230, 90, 40), "orange_dark": (150, 40, 16), "orange_light": (250, 170, 110), "belly": (250, 220, 120),
        "belly_dark": (210, 170, 70), "green": (60, 160, 70), "green_dark": (20, 90, 30), "steel": (210, 214, 226),
        "steel_dark": (110, 114, 128), "white": (246, 244, 236), "mouth": (110, 20, 30), "tongue": (210, 70, 90),
        "eye": (250, 200, 40), "pupil": (20, 16, 10)}
SHINY = {"orange": (60, 120, 200), "orange_dark": (24, 60, 130), "orange_light": (140, 190, 250),
         "green": (200, 70, 120), "green_dark": (130, 30, 70)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "orange", "orange_dark", size=1.6, light="orange_light", rim_mix=0.45)
GREEN = scales(P, "green", "green_dark", size=1.2, rim_mix=0.4)
STEEL = metal(P, "steel", dark="steel_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 14.0, y - 50.6, 1.0, "eye", slit=True)
        if c is not None:
            return c, None
    return GREEN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("biospinomon")
    mats = {"skin": HIDE, "belly": scales(P, "belly", "belly_dark", size=1.8, rim_mix=0.3), "neck": HIDE,
            "head": headf, "snout": GREEN, "jaw": GREEN, "mouth": solid(P, "mouth"), "tooth": solid(P, "white"),
            "tongue": solid(P, "tongue"), "arm": HIDE, "hand": HIDE, "claw": solid(P, "white"), "thigh": HIDE,
            "shin": HIDE, "foot": HIDE, "talon": solid(P, "white"), "tail": HIDE, "tail_tip": HIDE}
    a = theropod(m, mats, "biospinomon", hip_y=22.0, hip_z=4.0, chest=(0, 38.0, -4.0), body_r=7.0, chest_r=6.6,
                 neck_top=(0, 48.0, -8.0), head_len=14.0, head_w=3.6, head_h=4.0, mouth_open=20, teeth=8,
                 arm_len=12.0, arm_bulk=1.3, leg_bulk=1.6, stance=5.4,
                 tail=((0, 20, 12), (3, 16, 20), (7, 13, 28), (11, 12, 35), (14, 12, 41)), tail_r=(5, 4, 3, 2, 1.2))
    hd = a["head"]
    for j in range(5):                                           # head crest
        spike(m, hd, (0, a["skull_top"], a["skull_z"][0] + j * 1.4), (0, 1, 0.6), 1.2, 3.0 - j * 0.3,
              armour(P, "orange", "orange_dark"))
    bd = a["body"]
    for j in range(7):                                           # the sail of steel blades
        t = j / 6
        base = (0, 40.0 - 22.0 * t, -2.0 + 14.0 * t)
        ln = 14.0 - abs(t - 0.4) * 10.0
        m.box(bd, -0.6, base[1], base[2] - 2.0, 0.6, base[1] + ln, base[2] + 2.0, STEEL,
              rotation=(-20 - 10 * t, 0, 0), pivot=base)
        for sx in (-1, 1):
            m.box(bd, min(sx * 0.6, sx * 1.2), base[1] + ln * 0.2, base[2] - 1.0, max(sx * 0.6, sx * 1.2),
                  base[1] + ln * 0.8, base[2] + 1.0, solid(P, "steel_dark"), rotation=(-20 - 10 * t, 0, 0), pivot=base)
    return m
