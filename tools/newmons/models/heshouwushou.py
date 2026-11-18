"""Heshouwushou (a Digimon of the CobbleEffort: Digital crossover; hand-built after the manga art on wikimon.net): the
old mountain sage: a stooped elder whose head is a crown of broad drooping leaves with a sprout on top, a tired wrinkled
face, a long beard flowing down like roots over a robed body, and a gnarled staff topped with a curled leaf. 15 blocks.

Front is -z, y is up. 48 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fabric, skin, solid, strands, twisted
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 4}
LOOK = "a stooped elder with a crown of drooping leaves, a tired wrinkled face, a long root-like beard and a gnarled staff"
BASE = {"leaf": (110, 160, 80), "leaf_dark": (50, 100, 30), "face": (200, 170, 130), "face_dark": (140, 110, 80),
        "beard": (220, 216, 200), "beard_dark": (160, 156, 140), "robe": (150, 120, 80), "robe_dark": (90, 70, 40),
        "wood": (120, 90, 50), "wood_dark": (70, 50, 24), "eye": (30, 26, 24)}
SHINY = {"leaf": (200, 120, 60), "leaf_dark": (140, 70, 20)}


def P(v):
    return pal(BASE, SHINY, v)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 1.8, y - 34.0) < 0.9:
                return tone(p["eye"], face), None
            if abs(y - 35.2) < 0.25 and abs(x - sx * 1.8) < 1.4:
                return tone(p["face_dark"], face), None
    return skin(P, "face", dark="face_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("heshouwushou")
    top = m.bone("heshouwushou", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0.6, 6.0, 5.0, 0.0, 28.0, fabric(P, "robe", "robe_dark", axis="y"), cut=3)
    hd = m.bone("head", bd, (0, 30, -2))
    m.round_box(hd, 0, -2.0, 4.0, 3.6, 28.0, 37.0, facef, cut=2)
    for j in range(7):                                                                  # long root-like beard
        rod(m, hd, ((j - 3) * 1.0, 31.0, -5.4), ((j - 3) * 1.4, 12.0, -6.6), 1, strands(P, "beard", "beard_dark"),
            extend=0.3, t2=2)
    for i in range(10):                                                                 # crown of drooping leaves
        ang = 2 * math.pi * i / 10
        spike(m, hd, (2.4 * math.cos(ang), 37.0, -2.0 + 2.4 * math.sin(ang)),
              (math.cos(ang), -0.4, math.sin(ang)), 3.0, 8.0, skin(P, "leaf", dark="leaf_dark"), tip=1.0)
    spike(m, hd, (0, 37.6, -2.0), (0.2, 1, 0), 1.2, 6.0, skin(P, "leaf", dark="leaf_dark"), tip=0.8)  # sprout
    ab = m.bone("arm_right", bd, (-6.0, 24.0, -2.0))                                       # gnarled staff
    rod(m, ab, (-8.0, 0.0, -4.0), (-8.0, 46.0, -4.0), 2, twisted(P, "wood", "wood_dark"), extend=0)
    spike(m, ab, (-8.0, 46.0, -4.0), (0.6, 0.4, 0), 2.0, 4.0, skin(P, "leaf", dark="leaf_dark"), tip=0.8)
    m.round_box(ab, -7.0, -4.0, 1.4, 1.4, 24.0, 27.0, skin(P, "face", dark="face_dark"), cut=0)
    return m
