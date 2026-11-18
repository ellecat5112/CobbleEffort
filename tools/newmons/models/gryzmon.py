"""Gryzmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
blue grizzly: a big navy-blue bear with a shaggy white-tipped blue ruff, a grinning pale muzzle and a crescent mark on
its brow, red gauntlets studded with silver spikes on its forelegs, a red spiked pauldron, and great silver claws.
15 blocks long.

Front is -z, y is up. 30 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, fur, metal, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 3.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a big navy-blue bear with a shaggy white-tipped ruff, a pale muzzle, a crescent brow mark, red spiked "
        "gauntlets and great silver claws")
BASE = {"navy": (40, 50, 120), "navy_dark": (16, 20, 60), "navy_light": (120, 140, 220), "muzzle": (200, 200, 220),
        "red": (210, 40, 40), "red_dark": (130, 14, 18), "silver": (214, 218, 228), "silver_dark": (110, 114, 126),
        "moon": (230, 230, 250), "eye": (220, 40, 40), "mouth": (100, 20, 30), "tooth": (250, 250, 240),
        "white": (246, 246, 250)}
SHINY = {"navy": (110, 80, 50), "navy_dark": (60, 40, 20), "navy_light": (190, 150, 110)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "navy", "navy_dark", tip="navy_light", length=1.4, density=2.0)
RED = armour(P, "red", "red_dark", trim="silver", trim_w=0.3)
SILVER = metal(P, "silver", dark="silver_dark")


def build():
    m = Model("gryzmon")
    mats = {"skin": FUR, "snout": solid(P, "muzzle"), "jaw": solid(P, "muzzle"), "mouth": solid(P, "mouth"),
            "tooth": solid(P, "tooth"), "claw": SILVER}
    a = quadruped(m, mats, "gryzmon", length=28.0, body_y=15.0, body_rx=7.0, body_ry=6.4, chest_bulk=1.3,
                  neck=((0, 19, -12), (0, 19, -16)), head_len=8.0, head_w=4.0, head_h=4.0, snout=0.7, mouth_open=8,
                  teeth=4, leg_bulk=1.6, toes=4, tail=((0, 18, 14), (0, 18, 16)), tail_r=(1.6, 1.0))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.6,
              solid(P, "eye"))
    hc = a["head_c"]
    m.round_box(hd, hc[0], hc[2] - 3.6, 1.0, 0.3, hc[1] + 2.0, hc[1] + 3.4, solid(P, "moon"), cut=0)
    for i in range(14):                                                                     # shaggy ruff
        ang = math.radians(-160 + i * 24)
        spike(m, bd, (6.0 * math.cos(ang), 19.0 + 4.0 * math.sin(ang) + 2.0, -10.0), (math.cos(ang), 0.6, 0.6), 2.2, 6.0,
              FUR, tip=0.9)
    for nm in ("leg_front_left", "leg_front_right"):                                        # red spiked gauntlets
        w = a[nm]["wrist"]
        sx = 1 if w[0] > 0 else -1
        m.round_box(a[nm]["bone"], w[0], w[2], 3.4, 3.4, w[1] - 1.0, w[1] + 4.0, RED, cut=1)
        for j in range(3):
            spike(m, a[nm]["bone"], (w[0] + sx * 3.4, w[1] + 0.6 + j * 1.4, w[2] - 1.0 + j * 0.6), (sx, 0.2, -0.3), 1.0,
                  2.6, SILVER, tip=0.8)
    m.round_box(bd, 6.0, -8.0, 2.4, 3.4, 18.0, 22.0, RED, cut=1)                           # red spiked pauldron
    for j in range(3):
        spike(m, bd, (8.0, 21.0, -10.0 + j * 2.6), (1, 0.6, 0), 1.2, 2.6, SILVER, tip=0.8)
    return m
