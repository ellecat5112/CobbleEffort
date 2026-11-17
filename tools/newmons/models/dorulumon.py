"""Dorulumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the drill wolf. A powerful wolf with a shaggy flame-orange coat and white fur on its chest, belly and
paws, a gold drill horn on a steel brow plate, sharp black fins rising from its back like drill blades, huge clawed
paws with steel claws and a long white tail ending in a gold-and-steel drill. 15 blocks tall.

Front is -z, y is up. 36 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, fur, metal, solid
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 3.2)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a powerful wolf with a shaggy flame-orange coat, white chest and paws, a gold drill horn, black fins on its "
        "back, steel claws and a white tail ending in a drill")
BASE = {"orange": (230, 100, 40), "orange_dark": (150, 40, 10), "orange_light": (255, 170, 110), "white": (246, 246, 250),
        "white_dark": (190, 190, 206), "gold": (240, 196, 60), "gold_dark": (160, 110, 20), "steel": (210, 214, 226),
        "steel_dark": (100, 104, 116), "black": (40, 40, 46), "black_dark": (12, 12, 16), "eye": (60, 140, 220),
        "mouth": (130, 20, 30), "tooth": (250, 250, 246)}
SHINY = {"orange": (120, 120, 140), "orange_dark": (50, 50, 66), "orange_light": (190, 190, 210)}


def P(v):
    return pal(BASE, SHINY, v)


COAT = fur(P, "orange", "orange_dark", tip="orange_light", length=1.8, density=2.0)
WHITE = fur(P, "white", "white_dark", length=1.4)
STEEL = metal(P, "steel", dark="steel_dark")
GOLD = metal(P, "gold", dark="gold_dark", streak=1.2)


def build():
    m = Model("dorulumon")
    mats = {"skin": COAT, "belly": WHITE, "neck": WHITE, "head": COAT, "snout": WHITE, "jaw": WHITE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": COAT, "leg_lower": WHITE,
            "paw": WHITE, "claw": STEEL, "tail": WHITE}
    a = quadruped(m, mats, "dorulumon", length=32.0, body_y=16.0, body_rx=6.4, body_ry=6.4, chest_bulk=1.4,
                  neck=((0, 20, -15), (0, 23, -19)), head_len=9.0, head_w=3.6, head_h=4.0, snout=0.6, mouth_open=10,
                  teeth=3, leg_bulk=1.6, toes=4, tail=((0, 18, 16), (0, 24, 22), (0, 28, 30), (0, 28, 36)),
                  tail_r=(1.8, 1.6, 1.4, 1.2))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.3, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.3, ez + 0.6,
              solid(P, "eye"))
        spike(m, hd, (sx * 2.4, ey + 2.0, ez + 2.4), (sx * 0.4, 1, 0.5), 1.6, 3.6, COAT, tip=0.5)          # ears
    m.round_box(hd, 0, ez - 1.0, 2.4, 1.6, ey + 0.6, ey + 2.4, STEEL, cut=1)                                # brow plate
    spike(m, hd, (0, ey + 1.6, ez - 2.0), (0, 0.5, -1), 2.4, 6.0, GOLD, tip=1.0)                           # drill horn
    for j in range(2):                                                                                     # black fins
        z = -6.0 + j * 7.0
        for sx in (-1, 1):
            spike(m, bd, (sx * 2.6, 22.0, z), (sx * 0.5, 1, 0.8), 2.4, 9.0 - j * 2, armour(P, "black", "black_dark"),
                  tip=0.6)
    for i in range(10):                                                                                    # shaggy ruff
        ang = math.radians(i * 36)
        spike(m, bd, (5.0 * math.sin(ang), 18.0 + 4.0 * math.cos(ang), -12.0), (math.sin(ang), math.cos(ang), 0.6),
              2.4, 4.0, COAT, tip=0.6)
    e = a["tail_pts"][-1]                                                                                  # tail drill
    m.round_box(a["tail"], e[0], e[2], 1.6, 1.6, e[1] - 1.6, e[1] + 1.6, STEEL, cut=0)
    spike(m, a["tail"], (e[0], e[1], e[2] + 1.0), (0, 0, 1), 3.0, 6.0, GOLD, tip=1.0)
    return m
