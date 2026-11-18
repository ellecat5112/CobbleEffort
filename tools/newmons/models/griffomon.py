"""Griffomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the griffin: a cream lion's body striped with black tiger bars, a white-feathered eagle head under
a silver armoured helm, great red-brown wings tipped red, a green-tipped snake for a tail and steel-taloned forefeet.
35 blocks tall.

Front is -z, y is up. 36 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing, quadruped
from _digidetail import feathers, fur, metal, plane, scales, solid
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a griffin with a cream tiger-striped lion's body, a white eagle head in a silver helm, great red-brown wings "
        "and a snake for a tail")
BASE = {"cream": (240, 220, 160), "cream_dark": (190, 160, 100), "stripe": (40, 34, 30), "white": (246, 246, 246),
        "white_dark": (190, 190, 196), "silver": (200, 206, 220), "silver_dark": (100, 106, 120), "wing": (140, 60, 50),
        "wing_dark": (80, 26, 20), "red": (210, 40, 40), "beak": (240, 200, 70), "snake": (110, 180, 90),
        "snake_dark": (50, 110, 40), "steel": (180, 184, 200), "steel_dark": (90, 94, 106), "eye": (250, 220, 60)}
SHINY = {"cream": (200, 200, 214), "cream_dark": (140, 140, 160), "wing": (60, 70, 140), "wing_dark": (24, 30, 80)}


def P(v):
    return pal(BASE, SHINY, v)


FUR0 = fur(P, "cream", "cream_dark", length=1.0, density=2.2)


def furf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    a, b = plane(x, y, z, face)
    if face in ("east", "west", "up") and abs(((a * 0.4 + b * 0.25) % 3.0) - 1.5) < 0.35:
        return tone(p["stripe"], face), None
    return FUR0(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("griffomon")
    mats = {"skin": furf, "neck": feathers(P, "white", "white_dark"), "head": feathers(P, "white", "white_dark"),
            "snout": solid(P, "beak"), "jaw": solid(P, "beak"), "mouth": solid(P, "red"), "tooth": solid(P, "beak"),
            "claw": metal(P, "steel", dark="steel_dark")}
    a = quadruped(m, mats, "griffomon", length=32.0, body_y=16.0, body_rx=5.6, body_ry=5.6, chest_bulk=1.2,
                  neck=((0, 21, -14), (0, 25, -18)), head_len=8.0, head_w=3.4, head_h=3.8, snout=0.5, mouth_open=6,
                  teeth=0, leg_bulk=1.3, toes=4, tail=((0, 19, 16), (3, 22, 21), (6, 26, 22), (8, 27, 19)),
                  tail_r=(1.2, 1.0, 1.0, 0.8))
    bd, hd = a["body"], a["head"]
    hc = a["head_c"]
    m.round_box(hd, hc[0], hc[2], 3.8, 4.4, hc[1] + 0.6, hc[1] + 4.4, metal(P, "silver", dark="silver_dark"), cut=1)
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.6,
              solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.6, hc[1] + 4.0, hc[2] + 2.0), (sx * 0.5, 0.6, 1), 1.4, 5.0, metal(P, "silver", dark="silver_dark"),
              tip=0.8)
    spike(m, hd, (0, ey - 0.6, a["snout_front"]), (0, -0.7, -1), 1.8, 3.0, solid(P, "beak"), tip=0.8)  # hooked beak
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 4.6, 21.0, -6.0))
        feather_wing(m, wb, (side * 4.6, 21.0, -6.0), 26.0, 11.0, 3, feathers(P, "wing", "wing_dark", tip="red"),
                     side=side, sweep=35, droop=6.0)
    e = a["tail_pts"][-1]                                                                  # snake head on the tail
    m.round_box(a["tail"], e[0], e[2] - 1.0, 1.6, 2.4, e[1] - 1.0, e[1] + 1.6, scales(P, "snake", "snake_dark"), cut=1)
    return m
