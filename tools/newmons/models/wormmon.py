"""Wormmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little green caterpillar: a plump segmented body, a round head with a big violet jaw-plate cracked
down the middle, shiny blue eyes and a pink star on its brow, two long ribbon-like antennae, and stubby legs tipped
with pink claws. 1 block.

Front is -z, y is up. Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, plane, skin, solid
from _route import pal, tone

HEIGHT = 23
SCALE, HITBOX = sized(1.0, HEIGHT, 2.0)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a little green caterpillar with a violet jaw-plate, blue eyes, a pink brow star, long ribbon antennae and pink claws"
BASE = {"green": (150, 210, 80), "green_dark": (80, 140, 30), "violet": (120, 100, 180), "violet_dark": (60, 40, 110),
        "pink": (240, 80, 140), "eye": (80, 140, 220), "pupil": (20, 20, 40), "white": (255, 255, 255),
        "black": (40, 40, 50)}
SHINY = {"green": (230, 190, 70), "green_dark": (170, 120, 20)}


def P(v):
    return pal(BASE, SHINY, v)


GREEN = skin(P, "green", dark="green_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            c = eye(p, a - sx * 2.4, b - 15.0, 1.0, "eye")
            if c is not None:
                return c, None
        if abs(a) < 1.6 and abs(b - 17.4) < 0.6 and abs(abs(a) - abs(b - 17.4)) < 0.5:
            return p["pink"], None
    return GREEN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("wormmon")
    top = m.bone("wormmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    for i in range(4):                                                                 # segmented body
        ball(m, bd, (0, 4.0 + i * 0.6, 1.0 + i * 2.6), 3.4 - i * 0.2, GREEN, layers=2)
    hd = m.bone("head", bd, (0, 12, -1))
    ball(m, hd, (0, 14.0, -1.0), 4.4, headf, layers=4)
    m.round_box(hd, 0, -5.0, 2.0, 1.0, 10.6, 14.4, skin(P, "violet", dark="violet_dark"), cut=0)   # jaw plate
    m.box(hd, -0.2, 10.8, -6.1, 0.2, 14.0, -5.9, solid(P, "black"))
    for sx in (-1, 1):                                                                 # ribbon antennae
        pts = [(sx * 1.4, 18.0, -1.0), (sx * 4.0, 21.6, -1.0), (sx * 9.0, 20.0, 0), (sx * 12.0, 15.0, 1.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, GREEN, extend=0.3, t2=2)
    for i in range(3):
        for sx in (-1, 1):
            lg = m.bone("leg_%s_%d" % ("left" if sx > 0 else "right", i), bd, (sx * 3.0, 3.0, -1.0 + i * 2.6))
            ball(m, lg, (sx * 3.6, 2.0, -1.0 + i * 2.6), 1.2, GREEN, layers=1)
            spike(m, lg, (sx * 3.8, 1.0, -1.6 + i * 2.6), (sx * 0.3, -0.6, -1), 0.9, 1.8, solid(P, "pink"), tip=0.8)
    return m
