"""Ankylomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): an armoured ankylosaur. A domed shell of gold armour plates studded with black spikes, a violet
underside, a stubby armoured head with green eyes and a black horn, thick legs with gold claws and a long tail of
gold rings ending in a black spiked mace. 15 blocks tall.

Front is -z, y is up. 34 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped, slab_z
from _digidetail import armour, eye, metal, skin, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 2.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("an armoured ankylosaur: a domed gold shell studded with black spikes, a violet underside, a stubby armoured "
        "head with green eyes, gold claws and a tail of gold rings ending in a black spiked mace")
BASE = {"gold": (226, 186, 60), "gold_dark": (150, 110, 26), "gold_light": (255, 236, 150), "black": (40, 40, 48),
        "black_light": (110, 110, 124), "violet": (90, 60, 150), "violet_dark": (50, 30, 90), "eye": (90, 200, 90),
        "pupil": (20, 30, 20), "white": (250, 250, 250), "mouth": (100, 30, 40), "tooth": (240, 236, 230)}
SHINY = {"gold": (130, 170, 230), "gold_dark": (60, 90, 160), "gold_light": (200, 230, 255), "violet": (200, 120, 50),
         "violet_dark": (130, 70, 20)}


def P(v):
    return pal(BASE, SHINY, v)


SHELL = armour(P, "gold", "gold_dark", light="gold_light", panel=(3.2, 2.6))
GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")
SPIKE = metal(P, "black", dark="black", light="black_light", streak=2.0)
UNDER = skin(P, "violet", dark="violet_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 19.0, y - 14.6, 1.0, "eye")
        if c is not None:
            return c, None
    return SHELL(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("ankylomon")
    mats = {"skin": UNDER, "belly": UNDER, "neck": SHELL, "head": headf, "snout": SHELL, "jaw": UNDER,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": SHELL, "leg_lower": SHELL,
            "paw": SHELL, "claw": GOLD, "tail": GOLD}
    a = quadruped(m, mats, "ankylomon", length=26.0, body_y=12.0, body_rx=7.0, body_ry=5.0, chest_bulk=1.0,
                  neck=((0, 13, -14), (0, 14, -16)), head_len=9.0, head_w=4.0, head_h=4.0, snout=0.25,
                  mouth_open=6, teeth=3, leg_bulk=1.5, toes=3,
                  tail=((0, 14, 18), (0, 15, 23), (0, 18, 27)), tail_r=(2.4, 1.8, 1.4))
    bd = a["body"]
    for i in range(6):                                           # the domed shell
        z0 = -13 + i * 4.4
        r = 9.0 - abs(i - 2.5) * 0.7
        slab_z(m, bd, 0, 15.0, z0, z0 + 4.6, r, 5.6, SHELL)
        for sx in (-1, 0, 1):                                    # rows of black spikes
            if sx == 0 and i % 2:
                continue
            base = (sx * r * 0.75, 15.0 + 5.6 - abs(sx) * 1.6, z0 + 2.3)
            spike(m, bd, base, (sx * 0.6, 1, 0), 2.0, 4.0 - abs(sx) * 0.6, SPIKE, tip=0.8)
        for sx in (-1, 1):
            spike(m, bd, (sx * r, 12.0, z0 + 2.3), (sx, -0.1, 0), 1.6, 2.6, SPIKE)
    hd = a["head"]
    spike(m, hd, (0, 16.4, -18.0), (0, 1, -0.6), 1.6, 3.0, SPIKE)
    tl = a["tail"]
    for j in range(4):                                           # gold tail rings
        p = tuple(a["tail_pts"][1][q] + (a["tail_pts"][-1][q] - a["tail_pts"][1][q]) * j / 3 for q in range(3))
        m.round_box(tl, p[0], p[2], 2.0, 1.0, p[1] - 1.6, p[1] + 1.6, GOLD, cut=1)
    e = a["tail_pts"][-1]
    ball(m, tl, (e[0], e[1] + 2.0, e[2] + 1.5), 2.6, SPIKE, layers=3)                   # the mace
    for d in ((0, 1, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0.6, 0.6, 0.6), (-0.6, 0.6, 0.6), (0, -0.4, 1)):
        spike(m, tl, (e[0], e[1] + 2.0, e[2] + 1.5), d, 1.2, 4.0, SPIKE)
    return m
