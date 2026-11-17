"""Cernumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the forest stag. A slender pale stag with a green leaf-patterned coat, a white mane and red facial
markings, gold bands on its legs, a great bushy evergreen tail, and enormous antlers of curling golden horns ending in
bells of hunting horns and sprouting green pine boughs. 35 blocks tall.

Front is -z, y is up. 60 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import fur, metal, skin, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(35, HEIGHT, 3.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a slender pale stag with a green leaf-patterned coat, a white mane, gold leg bands, a bushy evergreen tail "
        "and enormous golden horn antlers sprouting pine boughs")
BASE = {"cream": (236, 230, 210), "cream_dark": (180, 170, 140), "green": (110, 160, 60), "green_dark": (50, 100, 30),
        "pine": (60, 120, 50), "pine_dark": (24, 70, 30), "gold": (230, 186, 60), "gold_dark": (160, 120, 20),
        "gold_light": (255, 230, 150), "red": (200, 40, 40), "hoof": (60, 50, 40), "eye": (40, 30, 20)}
SHINY = {"green": (170, 90, 160), "green_dark": (100, 40, 100), "pine": (190, 120, 60), "pine_dark": (120, 60, 20)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")
PINE = fur(P, "pine", "pine_dark", length=1.4)
MANE = fur(P, "cream", "cream_dark", length=1.6)


def coatf(x, y, z, face, variant, box=None, **k):
    """Green coat with darker leaf shapes."""
    p = P(variant)
    a, b = (x, z) if face in ("up", "down") else (z, y)
    if (math.sin(a * 0.9) + math.cos(b * 1.1 + a * 0.4)) > 1.2:
        return tone(p["green_dark"], face), None
    return skin(P, "green", dark="green_dark", var=0.04)(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        if abs(y - 39.6) < 0.5 and abs(z + 25.0) < 0.6:
            return tone(p["eye"], face), None
        if abs(y - 38.6 - 0.4 * (z + 24.0)) < 0.25 and -26.0 < z < -22.0:
            return tone(p["red"], face), None
    return skin(P, "cream", dark="cream_dark", var=0.03)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("cernumon")
    mats = {"skin": coatf, "belly": skin(P, "cream", dark="cream_dark"), "neck": MANE, "head": headf, "snout": headf,
            "jaw": headf, "leg_upper": coatf, "leg_lower": coatf, "paw": solid(P, "hoof"), "claw": solid(P, "hoof"),
            "tail": PINE}
    a = quadruped(m, mats, "cernumon", length=22.0, body_y=20.0, body_rx=4.6, body_ry=5.0, chest_bulk=1.2,
                  neck=((0, 28, -12), (0, 36, -17)), head_len=9.0, head_w=2.6, head_h=3.0, snout=0.6, mouth_open=0,
                  teeth=0, leg_bulk=1.0, toes=2, claws=False,
                  tail=((0, 24, 14), (0, 26, 22), (2, 24, 30), (4, 20, 36)), tail_r=(4.0, 5.0, 4.6, 3.0))
    hd = a["head"]
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):
        lg = a[nm]
        e = lg["elbow"]
        m.round_box(lg["bone"], e[0], e[2], 1.8, 1.8, e[1] - 1.0, e[1] + 0.6, GOLD, cut=1)
    st = a["skull_top"]
    for sx in (-1, 1):                                                        # golden horn antlers
        pts = [(sx * 1.6, st, -17.0), (sx * 5.0, st + 6.0, -18.0), (sx * 10.0, st + 9.0, -16.0),
               (sx * 14.0, st + 14.0, -16.0), (sx * 18.0, st + 16.0, -17.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 2 if j < 2 else 1, GOLD, extend=0.4)
        bell = pts[-1]
        for r, dz in ((1.2, 0.0), (2.0, 1.0), (2.8, 2.0)):                     # the horn bell
            m.round_box(hd, bell[0] + sx * dz, bell[2], r, r, bell[1] - r, bell[1] + r, GOLD, cut=1)
        ring = (sx * 9.0, st + 9.0, -16.0)                                    # a coiled horn loop
        for i in range(8):
            ang = i * math.pi / 4
            p0 = (ring[0] + sx * 2.6 * math.cos(ang), ring[1] + 2.6 * math.sin(ang), ring[2])
            p1 = (ring[0] + sx * 2.6 * math.cos(ang + math.pi / 4), ring[1] + 2.6 * math.sin(ang + math.pi / 4), ring[2])
            rod(m, hd, p0, p1, 1, GOLD, extend=0.3)
        for j in (1, 2, 3):                                                  # pine boughs
            p = pts[j]
            spike(m, hd, p, (sx * 0.4, 1, 0.3), 2.4, 4.0, PINE, tip=1.0)
    for j in range(6):                                                        # white mane down the neck
        spike(m, a["neck"], (0, 28.0 + j * 1.4, -11.0 - j * 1.0), (0, -0.4, -1), 2.0, 2.6, MANE)
    return m
