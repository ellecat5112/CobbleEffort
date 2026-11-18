"""Liollmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
little holy lion: a golden-yellow lion cub crouched to pounce, a spiky red mane tuft on its head, big blue eyes, a
fanged roar, a gold collar with a round emerald pendant, grey claws and a long thin tail with a tufted tip. Child
stage, 1 block long.

Front is -z, y is up. 24 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import fur, gem, metal, solid, strands
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(1.0, HEIGHT, 2.4)
KIND = "quadruped"
K = 4
LOOK = "a golden-yellow lion cub with a spiky red mane tuft, big blue eyes, a gold collar with an emerald pendant and a tufted tail"
BASE = {"gold": (250, 210, 70), "gold_dark": (200, 150, 20), "gold_light": (255, 240, 170), "red": (220, 60, 40),
        "red_dark": (150, 20, 14), "eye": (60, 150, 230), "collar": (220, 170, 60), "collar_dark": (150, 110, 30),
        "green": (40, 170, 110), "green_light": (170, 240, 200), "claw": (130, 130, 140), "mouth": (180, 40, 50),
        "tooth": (250, 250, 246)}
SHINY = {"gold": (240, 240, 246), "gold_dark": (170, 172, 190), "red": (60, 120, 220), "red_dark": (20, 60, 150)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "gold", "gold_dark", tip="gold_light", length=0.7)


def build():
    m = Model("liollmon")
    mats = {"skin": FUR, "belly": FUR, "neck": FUR, "head": FUR, "snout": FUR, "jaw": FUR, "mouth": solid(P, "mouth"),
            "tooth": solid(P, "tooth"), "leg_upper": FUR, "leg_lower": FUR, "paw": FUR, "claw": solid(P, "claw"), "tail": FUR}
    a = quadruped(m, mats, "liollmon", length=14.0, body_y=8.0, body_rx=3.2, body_ry=3.4, chest_bulk=1.3,
                  neck=((0, 10, -6), (0, 12, -8)), head_len=6.4, head_w=3.0, head_h=3.0, snout=0.6, mouth_open=16, teeth=3,
                  leg_bulk=1.0, toes=3, tail=((0, 10, 7), (0, 15, 10), (0, 19, 8)), tail_r=(0.8, 0.6, 0.6))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    hc = a["head_c"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.6, ez - 1.0, max(sx * ex, sx * (ex + 0.3)), ey + 0.6, ez + 1.0,
              solid(P, "eye"))
        spike(m, hd, (sx * 2.2, hc[1] + 2.0, hc[2] + 1.4), (sx * 0.4, 1, 0.3), 1.0, 1.6, FUR, tip=0.8)
    for j in range(5):                                                               # red mane tuft
        spike(m, hd, ((j - 2) * 0.6, hc[1] + 2.6, hc[2] - 0.6 + abs(j - 2) * 0.4), ((j - 2) * 0.2, 1, 0.3), 1.0, 3.2,
              strands(P, "red", "red_dark"), tip=0.8)
    nk = a["neck"]
    m.round_box(nk, 0, -6.6, 2.6, 2.0, 9.4, 10.6, metal(P, "collar", dark="collar_dark"), cut=1)
    m.round_box(nk, 0, -8.8, 1.0, 0.4, 8.0, 10.0, gem(P, "green", "green_light"), cut=0)
    spike(m, a["tail"], a["tail_pts"][-1], (0, -0.2, -1), 1.2, 2.0, FUR, tip=0.8)
    return m
