"""Loogamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
demon wolf pup: a navy-blue wolf pup with a white muzzle, chest and tail tip, pink goggles pushed up on its head, red
eyes, a fanged snarl, black leather bands with silver buckles round its legs, red claws and a big bushy tail. Child
stage, 1 block long.

Front is -z, y is up. 24 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import fur, gem, leather, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(1.0, HEIGHT, 2.4)
KIND = "quadruped"
K = 4
LOOK = "a navy-blue wolf pup with a white muzzle and chest, pink goggles on its head, leg straps, red claws and a bushy tail"
BASE = {"navy": (50, 60, 140), "navy_dark": (20, 24, 80), "white": (246, 246, 250), "white_dark": (180, 180, 200),
        "pink": (230, 60, 180), "pink_light": (255, 190, 240), "black": (34, 34, 40), "black_dark": (12, 12, 14),
        "red": (210, 40, 40), "eye": (220, 40, 40), "mouth": (180, 60, 80), "tooth": (250, 250, 246), "silver": (210, 214, 224)}
SHINY = {"navy": (70, 70, 80), "navy_dark": (24, 24, 30)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "navy", "navy_dark", tip="white", length=1.0)
WHITE = fur(P, "white", "white_dark", length=0.8)


def build():
    m = Model("loogamon")
    mats = {"skin": FUR, "belly": WHITE, "neck": WHITE, "head": FUR, "snout": WHITE, "jaw": WHITE, "mouth": solid(P, "mouth"),
            "tooth": solid(P, "tooth"), "leg_upper": FUR, "leg_lower": FUR, "paw": FUR, "claw": solid(P, "red"), "tail": FUR}
    a = quadruped(m, mats, "loogamon", length=14.0, body_y=8.0, body_rx=3.2, body_ry=3.4, chest_bulk=1.3,
                  neck=((0, 10, -6), (0, 12, -8)), head_len=6.8, head_w=3.0, head_h=3.0, snout=1.0, mouth_open=18, teeth=4,
                  leg_bulk=1.0, toes=3, tail=((0, 10, 7), (0, 13, 11), (0, 14, 15)), tail_r=(1.4, 1.8, 1.4))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    hc = a["head_c"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.3, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.3, ez + 0.6,
              solid(P, "eye", glow=True))
        spike(m, hd, (sx * 1.8, hc[1] + 2.4, hc[2] + 1.6), (sx * 0.3, 1, 0.2), 1.4, 3.0, FUR, tip=0.8)
    m.round_box(hd, 0, hc[2] - 0.6, 3.2, 1.2, hc[1] + 1.8, hc[1] + 3.0, leather(P, "black", "black_dark"), cut=0)   # goggles
    for sx in (-1, 1):
        m.round_box(hd, sx * 1.4, hc[2] - 1.8, 1.0, 0.3, hc[1] + 1.8, hc[1] + 3.0, gem(P, "pink", "pink_light"), cut=0)
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):   # leg straps
        el = a[nm]["elbow"]
        m.round_box(a[nm]["bone"], el[0], el[2], 1.4, 1.4, el[1] - 2.0, el[1] - 1.0, leather(P, "black", "black_dark"), cut=0)
    tp = a["tail_pts"][-1]
    spike(m, a["tail"], tp, (0, 0.6, 1), 1.6, 3.0, WHITE, tip=0.8)
    return m
