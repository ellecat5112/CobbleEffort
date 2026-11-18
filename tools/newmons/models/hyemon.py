"""Hyemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
grinning hyena cub: violet spotted fur with a cream muzzle and belly, a shaggy red mane down its neck and back, round
ears, a dark skull mark on its brow, a toothy laughing grin and a bushy red-tipped tail. Child stage, 1 block tall.

Front is -z, y is up. 20 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import fur, skin, solid, strands
from _route import pal, tone

HEIGHT = 20
SCALE, HITBOX = sized(1.0, HEIGHT, 1.6)
KIND = "quadruped"
K = 4
LOOK = "a grinning violet spotted hyena cub with a cream muzzle, a shaggy red mane, a skull mark and a bushy tail"
BASE = {"violet": (140, 100, 170), "violet_dark": (80, 50, 110), "spot": (60, 36, 80), "cream": (240, 226, 200),
        "cream_dark": (190, 170, 140), "red": (220, 60, 50), "red_dark": (140, 24, 20), "mouth": (160, 40, 50),
        "tooth": (250, 250, 246), "eye": (250, 210, 40), "skull": (40, 30, 50), "claw": (240, 236, 220)}
SHINY = {"violet": (210, 170, 90), "violet_dark": (140, 100, 30), "spot": (100, 70, 20), "red": (60, 140, 220),
         "red_dark": (20, 70, 150)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "violet", "violet_dark")


def coatf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    cx, cz = round(x / 2.4) * 2.4, round(z / 2.4) * 2.4
    if face in ("east", "west", "up") and math.hypot(x - cx, z - cz) < 0.6 and y > 8.0:
        return tone(p["spot"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("hyemon")
    mats = {"skin": coatf, "belly": skin(P, "cream", dark="cream_dark"), "neck": coatf, "head": coatf,
            "snout": skin(P, "cream", dark="cream_dark"), "jaw": skin(P, "cream", dark="cream_dark"),
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": coatf, "leg_lower": coatf,
            "paw": coatf, "claw": solid(P, "claw"), "tail": coatf}
    a = quadruped(m, mats, "hyemon", length=12.0, body_y=8.0, body_rx=2.8, body_ry=3.0, chest_bulk=1.3,
                  neck=((0, 10, -5), (0, 13, -7)), head_len=6.0, head_w=2.6, head_h=2.8, snout=0.6, mouth_open=14,
                  teeth=3, leg_bulk=0.8, toes=3, tail=((0, 9, 6), (0, 11, 9)), tail_r=(1.4, 1.6))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.6,
              solid(P, "eye"))
        m.round_box(hd, sx * 2.0, ez + 2.0, 1.2, 0.6, ey + 1.6, ey + 4.0, coatf, cut=0)        # round ears
    hc = a["head_c"]
    m.round_box(hd, 0, hc[2] - 1.0, 0.8, 0.4, ey + 1.6, ey + 2.6, solid(P, "skull"), cut=0)    # skull mark
    MANE = strands(P, "red", "red_dark")
    for i in range(8):                                                              # shaggy red mane
        spike(m, bd if i > 2 else a["neck"], (0, 11.2 if i > 2 else 13.4, -7.0 + i * 1.6), (0, 1, 0.6), 1.4,
              2.6 - i * 0.15, MANE, tip=0.8)
    spike(m, a["tail"], (0, 11.0, 9.0), (0, 0.6, 1), 1.8, 3.0, MANE, tip=0.8)
    return m
