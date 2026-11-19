"""Vermillimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a vermilion ankylosaur dragon: a low heavy red body under dark brown armour plates edged with
spikes, a single huge brown horn rising from its snout, a toothy jaw and green eyes, thick clawed legs and a spiked
tail. 25 blocks.

Front is -z, y is up. Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digidetail import armour, eye, metal, scales, solid
from _route import pal, tone

HEIGHT = 31
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a vermilion ankylosaur dragon under dark spiked armour plates with one huge horn on its snout"
BASE = {"red": (220, 90, 60), "red_dark": (140, 40, 20), "brown": (90, 60, 50), "brown_dark": (40, 26, 20),
        "horn": (120, 80, 60), "horn_dark": (60, 34, 24), "eye": (60, 210, 120), "pupil": (10, 20, 10),
        "white": (255, 255, 255), "claw": (60, 50, 46)}
SHINY = {"red": (120, 160, 90), "red_dark": (60, 100, 40)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "red", "red_dark", size=1.4)
PLATE = armour(P, "brown", "brown_dark", panel=(3.0, 3.0))


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 18.0, y - 19.4, 1.0, "eye", slit=True)
        if c is not None:
            return c, None
    return HIDE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("vermillimon")
    mats = {"skin": HIDE, "belly": HIDE, "neck": HIDE, "head": headf, "leg": HIDE, "paw": HIDE,
            "claw": solid(P, "claw"), "tail": HIDE}
    a = quadruped(m, mats, "vermillimon", length=26.0, body_y=12.0, body_rx=7.4, body_ry=6.0, chest_bulk=1.1,
                  neck=((0, 15, -13), (0, 17, -15)), head_len=11.0, head_w=4.6, head_h=5.0, snout=0.5, mouth_open=14,
                  teeth=6, tail=((0, 12, 13), (0, 10, 20), (0, 9, 27)), tail_r=(3.0, 2.2, 1.4), toes=3, claws=True)
    bd, hd = a["body"], a["head"]
    for i in range(5):                                                                 # armour plates
        z = -9.0 + i * 4.6
        m.round_box(bd, 0, z, 6.6, 2.2, 16.0, 19.0, PLATE, cut=1)
        for sx in (-1, 1):
            spike(m, bd, (sx * 6.6, 17.0, z), (sx, 0.3, 0), 1.4, 3.0, PLATE, tip=0.8)
    spike(m, hd, (0, 20.0, a["snout_front"] + 3.0), (0, 1, 0.15), 3.4, 18.0, metal(P, "horn", dark="horn_dark"), tip=0.8)
    for j in range(4):
        spike(m, bd, (0, 10.0, 18.0 + j * 2.4), (0, 1, 0.2), 1.2, 2.6, PLATE, tip=0.8)
    return m
