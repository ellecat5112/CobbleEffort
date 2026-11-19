"""Xuanwumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Black Tortoise, holy beast of the north: a colossal tortoise whose shell bears a whole ancient
tree, a vast dark-green crown hung with golden fruits over a gnarled brown trunk, a scaly tan body, a fierce reptile
head and a snake for a tail. 35 blocks.

Front is -z, y is up. Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digidetail import armour, eye, fur, metal, scales, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(35, HEIGHT, 10.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 4}
LOOK = "a colossal tortoise bearing an ancient tree on its shell, a dark-green crown hung with golden fruits, a fierce head and a snake tail"
BASE = {"tan": (220, 200, 160), "tan_dark": (150, 120, 80), "shell": (120, 90, 60), "shell_dark": (60, 40, 24),
        "bark": (100, 70, 40), "bark_dark": (50, 30, 14), "leaf": (40, 100, 50), "leaf_dark": (14, 50, 20),
        "gold": (240, 210, 120), "eye": (220, 50, 40), "pupil": (20, 10, 10), "white": (255, 255, 255),
        "snake": (90, 80, 70), "snake_dark": (40, 34, 30)}
SHINY = {"leaf": (180, 80, 60), "leaf_dark": (100, 30, 20), "tan": (170, 190, 210), "tan_dark": (100, 120, 150)}


def P(v):
    return pal(BASE, SHINY, v)


TAN = scales(P, "tan", "tan_dark", size=1.4)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 25.0, y - 13.6, 1.0, "eye", slit=True)
        if c is not None:
            return c, None
    return TAN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("xuanwumon")
    mats = {"skin": TAN, "belly": TAN, "neck": TAN, "head": headf, "leg": TAN, "paw": TAN, "claw": solid(P, "shell_dark"),
            "tail": TAN}
    a = quadruped(m, mats, "xuanwumon", length=30.0, body_y=10.0, body_rx=10.0, body_ry=6.0, chest_bulk=1.0,
                  neck=((0, 11, -16), (0, 13, -21)), head_len=10.0, head_w=3.6, head_h=4.0, snout=0.5, mouth_open=10,
                  teeth=4, tail=((0, 10, 16),), tail_r=(1.6,), toes=3, claws=True)
    bd = a["body"]
    ball(m, bd, (0, 13.0, 0), 13.0, armour(P, "shell", "shell_dark", panel=(4.0, 4.0)), layers=4, squash=0.45)
    tr = m.bone("tree", bd, (0, 18, 0))                                                 # the ancient tree
    m.round_box(tr, 0, 0, 3.4, 3.4, 16.0, 30.0, armour(P, "bark", "bark_dark", panel=(1.6, 4.0)), cut=1)
    for i, (x, y, z, r) in enumerate(((0, 38, 0, 10.0), (-8, 34, 2, 7.0), (8, 34, -2, 7.0), (0, 34, 8, 7.0),
                                      (0, 34, -8, 7.0), (-5, 44, -3, 6.0), (5, 43, 3, 6.0))):
        ball(m, tr, (x, y, z), r, fur(P, "leaf", "leaf_dark", length=2.0), layers=3)
    for i in range(10):
        ang = i * 2 * math.pi / 10
        rod(m, tr, (11.0 * math.cos(ang), 31.0, 11.0 * math.sin(ang)), (11.4 * math.cos(ang), 27.0, 11.4 * math.sin(ang)),
            1, solid(P, "bark"), extend=0.0)
        ball(m, tr, (11.4 * math.cos(ang), 26.2, 11.4 * math.sin(ang)), 1.0, solid(P, "gold"), layers=1)
    sn = m.bone("snake", bd, (0, 10, 16))                                               # snake tail
    pts = [(0, 10.0, 16.0), (4.0, 9.0, 21.0), (9.0, 10.0, 23.0), (12.0, 13.0, 21.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, sn, p0, p1, 2, scales(P, "snake", "snake_dark"), extend=0.4)
    m.round_box(sn, 12.4, 19.6, 1.4, 2.4, 12.4, 15.0, scales(P, "snake", "snake_dark"), cut=1)
    return m
