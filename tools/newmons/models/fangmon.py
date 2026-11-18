"""Fangmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the hound of calamity. A lean, gaunt red wolf bound in black leather straps with steel buckles, a
long narrow head with an enormous grin of jagged teeth and its eyes hidden, black legs with red claws, and a long
whip of a red tail tipped white. 15 blocks tall.

Front is -z, y is up. 32 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import fur, leather, metal, solid
from _route import pal, tone

HEIGHT = 32
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a lean gaunt red wolf bound in black leather straps with steel buckles, a long head with an enormous jagged "
        "grin, black legs with red claws and a white-tipped whip tail")
BASE = {"red": (200, 40, 40), "red_dark": (110, 14, 18), "white": (246, 246, 246), "black": (30, 28, 32),
        "black_dark": (10, 10, 12), "strap": (40, 36, 40), "steel": (200, 204, 214), "steel_dark": (100, 104, 116),
        "claw": (210, 40, 80), "mouth": (60, 10, 20), "tooth": (250, 250, 246)}
SHINY = {"red": (60, 60, 70), "red_dark": (24, 24, 30)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "red", "red_dark", length=1.2, density=2.4)


def strapf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face != "up" and abs((z * 0.8) % 5.0 - 2.5) < 0.6:
        return tone(p["strap"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("fangmon")
    mats = {"skin": strapf, "belly": FUR, "neck": FUR, "head": FUR, "snout": FUR, "jaw": FUR,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": strapf,
            "leg_lower": leather(P, "black", "black_dark", stitch="steel"), "paw": solid(P, "black"),
            "claw": solid(P, "claw"), "tail": FUR}
    a = quadruped(m, mats, "fangmon", length=28.0, body_y=18.0, body_rx=4.0, body_ry=4.4, chest_bulk=1.3,
                  neck=((0, 20, -12), (0, 21, -16)), head_len=13.0, head_w=2.8, head_h=3.2, snout=1.0, mouth_open=22,
                  teeth=8, leg_bulk=1.0, toes=3,
                  tail=((0, 21, 14), (2, 26, 19), (5, 30, 20), (6, 32, 16)), tail_r=(1.4, 1.2, 1.0, 0.8))
    bd = a["body"]
    for j in range(3):                                                             # buckles
        m.round_box(bd, 0, -8.0 + j * 6.0, 1.2, 0.8, 22.2, 23.4, metal(P, "steel", dark="steel_dark"), cut=0)
    e = a["tail_pts"][-1]
    spike(m, a["tail"], e, (0.2, -0.3, -1), 1.4, 4.0, solid(P, "white"), tip=0.4)
    return m
