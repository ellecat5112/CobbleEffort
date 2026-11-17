"""DORUmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
little beast dragon. A lean violet fox-like dragon pup with shaggy fur, a white muzzle and chest, a red triangular gem
set in a silver plate on its forehead, pointed ears, little wing-fins on its elbows, white clawed paws and a huge
fluffy violet tail with a white tip. Child stage, 1 block tall.

Front is -z, y is up. 28 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import fur, gem, metal, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "quadruped"
K = 4
ANIM = {"leg_amp": 12}
LOOK = ("a lean violet fox-like dragon pup with a white muzzle, a red forehead gem in a silver plate, pointed ears, "
        "white clawed paws and a huge fluffy white-tipped tail")
BASE = {"violet": (140, 120, 200), "violet_dark": (70, 56, 130), "white": (246, 246, 250), "white_dark": (190, 190, 206),
        "red": (220, 40, 40), "red_light": (255, 160, 150), "silver": (210, 214, 226), "silver_dark": (110, 114, 128),
        "eye": (200, 140, 40), "mouth": (130, 30, 40), "tooth": (250, 250, 246), "claw": (60, 60, 70)}
SHINY = {"violet": (230, 170, 80), "violet_dark": (160, 100, 20)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "violet", "violet_dark", length=1.2, density=2.6)
WHITE = fur(P, "white", "white_dark", length=1.0)


def build():
    m = Model("dorumon")
    mats = {"skin": FUR, "belly": WHITE, "neck": WHITE, "head": FUR, "snout": WHITE, "jaw": WHITE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": FUR, "leg_lower": FUR,
            "paw": WHITE, "claw": solid(P, "claw"), "tail": FUR}
    a = quadruped(m, mats, "dorumon", length=18.0, body_y=9.0, body_rx=3.6, body_ry=3.6, chest_bulk=1.1,
                  neck=((0, 11, -8), (0, 14, -10)), head_len=7.0, head_w=3.4, head_h=3.6, snout=0.4, mouth_open=4,
                  teeth=0, leg_bulk=0.9, toes=3, tail=((0, 11, 9), (0, 16, 12), (0, 22, 13)), tail_r=(2.6, 3.4, 3.0))
    hd, bd = a["head"], a["body"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.5, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.5, ez + 0.6,
              solid(P, "eye"))
        spike(m, hd, (sx * 2.4, ey + 2.0, ez + 2.0), (sx * 0.5, 1, 0.4), 1.6, 4.0, FUR, tip=0.5)          # ears
        for nm in ("leg_front_left",) if sx > 0 else ("leg_front_right",):
            el = a[nm]["elbow"] if "elbow" in a[nm] else a[nm]["hip"]
            spike(m, a[nm]["bone"], el, (sx, 0.4, 0.6), 1.2, 3.0, FUR, tip=0.4)                          # wing-fins
    m.round_box(hd, 0, ez - 1.6, 1.6, 0.6, ey + 0.6, ey + 2.6, metal(P, "silver", dark="silver_dark"), cut=0)
    spike(m, hd, (0, ey + 1.0, ez - 2.2), (0, 1, 0), 1.6, 1.8, gem(P, "red", "red_light"))                  # forehead gem
    e = a["tail_pts"][-1]
    m.round_box(a["tail"], e[0], e[2], 2.4, 2.4, e[1], e[1] + 3.0, WHITE, cut=1)                          # white tip
    return m
