"""Ginryumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the armoured dragon steed: a long-bodied black dragon armoured in lacquered plates laced with red
cord, a long violet-plated neck, a horned helm shaped like a skull with a white muzzle, red-and-steel guards on its
legs, yellow scaled legs with steel claws and a long tail ending in a golden tassel. Adult stage, 15 blocks.

Front is -z, y is up. 32 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, metal, scales, solid, strands
from _route import pal, tone

HEIGHT = 32
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a long-bodied black dragon in red-laced lacquered armour with a violet-plated neck, a skull-like horned helm, "
        "yellow scaled legs with steel claws and a golden tassel tail")
BASE = {"black": (44, 36, 40), "black_dark": (16, 12, 14), "black_light": (110, 96, 104), "red": (200, 40, 40),
        "violet": (150, 120, 190), "violet_dark": (80, 60, 120), "yellow": (240, 190, 60), "yellow_dark": (180, 120, 20),
        "steel": (210, 214, 224), "steel_dark": (100, 104, 116), "white": (246, 246, 246), "gold": (240, 200, 70),
        "gold_dark": (170, 120, 20), "eye": (230, 40, 40), "mouth": (100, 20, 30), "tooth": (250, 250, 240)}
SHINY = {"black": (230, 230, 240), "black_dark": (160, 160, 176), "black_light": (255, 255, 255)}


def P(v):
    return pal(BASE, SHINY, v)


ARM0 = armour(P, "black", "black_dark", light="black_light", trim="red", trim_w=0.3)


def armf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west", "up") and abs((z * 0.5) % 3.0 - 1.5) < 0.12:
        return tone(p["red"], face), None
    return ARM0(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("ginryumon")
    mats = {"skin": armf, "neck": armour(P, "violet", "violet_dark", trim="black"), "head": metal(P, "steel", dark="steel_dark"),
            "snout": solid(P, "white"), "jaw": solid(P, "white"), "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"),
            "leg_upper": armf, "leg_lower": scales(P, "yellow", "yellow_dark", size=1.0),
            "paw": scales(P, "yellow", "yellow_dark", size=1.0), "claw": metal(P, "steel", dark="steel_dark"),
            "tail": armf}
    a = quadruped(m, mats, "ginryumon", length=30.0, body_y=15.0, body_rx=5.0, body_ry=5.0, chest_bulk=1.1,
                  neck=((0, 21, -14), (0, 27, -19)), head_len=9.0, head_w=2.8, head_h=3.2, snout=0.8, mouth_open=8,
                  teeth=4, leg_bulk=1.1, toes=3,
                  tail=((0, 18, 15), (0, 24, 20), (0, 27, 25), (0, 25, 29)), tail_r=(2.4, 2.0, 1.6, 1.2))
    hd = a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.6,
              solid(P, "eye", glow=True))
        spike(m, hd, (sx * 1.8, ey + 2.4, ez + 1.4), (sx * 0.6, 0.6, 1), 1.4, 5.0, metal(P, "steel", dark="steel_dark"),
              tip=0.8)
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):           # leg guards
        e = a[nm].get("elbow") or a[nm]["wrist"]
        m.round_box(a[nm]["bone"], e[0], e[2], 2.6, 2.6, e[1] - 1.6, e[1] + 1.6, armour(P, "red", "black", trim="steel"),
                    cut=1)
    e = a["tail_pts"][-1]
    for j in range(5):                                                                              # golden tassel
        spike(m, a["tail"], e, ((j - 2) * 0.3, -1, 0.5), 0.9, 6.0, strands(P, "gold", "gold_dark"), tip=0.8)
    return m
