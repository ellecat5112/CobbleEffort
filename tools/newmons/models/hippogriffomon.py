"""Hippogriffomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): the hippogriff: a white eagle-headed beast with a golden beak and a red mark round its eye, great white
feathered wings, violet-banded forelegs with dark talons, a lion's hind body and a long flowing white tail. 25 blocks.

Front is -z, y is up. 34 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing, quadruped
from _digidetail import feathers, fur, solid, strands
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a white eagle-headed beast with a golden beak, great white wings, violet-banded legs, dark talons and a flowing tail"
BASE = {"white": (246, 246, 250), "white_dark": (190, 192, 206), "beak": (240, 200, 60), "red": (200, 40, 40),
        "violet": (130, 100, 200), "talon": (40, 40, 50), "eye": (60, 140, 90)}
SHINY = {"white": (230, 200, 120), "white_dark": (180, 140, 60)}


def P(v):
    return pal(BASE, SHINY, v)


FUR0 = fur(P, "white", "white_dark", length=1.0)


def legf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (y % 3.0) < 0.6:
        return tone(p["violet"], face), None
    return FUR0(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("hippogriffomon")
    mats = {"skin": FUR0, "neck": feathers(P, "white", "white_dark"), "head": feathers(P, "white", "white_dark"),
            "snout": solid(P, "beak"), "jaw": solid(P, "beak"), "mouth": solid(P, "red"), "tooth": solid(P, "beak"),
            "leg_lower": legf, "claw": solid(P, "talon")}
    a = quadruped(m, mats, "hippogriffomon", length=30.0, body_y=16.0, body_rx=5.0, body_ry=5.0, chest_bulk=1.3,
                  neck=((0, 21, -13), (0, 25, -17)), head_len=7.0, head_w=3.0, head_h=3.4, snout=0.5, mouth_open=6,
                  teeth=0, leg_bulk=1.2, toes=4, tail=((0, 19, 15), (2, 17, 22), (4, 14, 28)), tail_r=(1.4, 1.4, 1.2))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.6,
              solid(P, "eye"))
        m.box(hd, min(sx * ex, sx * (ex + 0.25)), ey - 1.0, ez - 1.2, max(sx * ex, sx * (ex + 0.25)), ey + 1.0, ez - 0.6,
              solid(P, "red"))
    spike(m, hd, (0, ey - 0.6, a["snout_front"]), (0, -0.7, -1), 2.0, 3.0, solid(P, "beak"), tip=0.8)
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 4.6, 21.0, -6.0))
        feather_wing(m, wb, (side * 4.6, 21.0, -6.0), 24.0, 10.0, 3, feathers(P, "white", "white_dark"), side=side,
                     sweep=35, droop=8.0)
    e = a["tail_pts"][-1]
    for j in range(4):
        spike(m, a["tail"], e, (0.3 * (j - 1.5), -0.6, 0.6), 1.4, 6.0, strands(P, "white", "white_dark"), tip=0.8)
    return m
