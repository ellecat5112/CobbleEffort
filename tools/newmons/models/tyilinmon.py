"""Tyilinmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a qilin holy beast: a green dragon head with a long red tongue, curled horns and a white mane,
great swept white feather-wings, a golden scaled body draped with a green jade collar, white-socked legs ending in
black hooves, a curling golden cloud-tail, and lightning crackling round it. 25 blocks.

Front is -z, y is up. Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing, quadruped
from _digidetail import eye, feathers, fur, metal, scales, solid
from _route import pal, tone

HEIGHT = 33
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a qilin with a green dragon head and red tongue, white feather wings, a golden scaled body, black hooves and a curling gold cloud-tail"
BASE = {"green": (60, 150, 90), "green_dark": (20, 80, 40), "gold": (220, 180, 80), "gold_dark": (150, 110, 30),
        "white": (246, 246, 250), "white_dark": (190, 194, 210), "red": (220, 60, 80), "black": (30, 30, 34),
        "eye": (250, 200, 40), "pupil": (20, 10, 10), "jade": (60, 170, 120), "bolt": (200, 240, 255)}
SHINY = {"gold": (180, 190, 210), "gold_dark": (110, 120, 150), "green": (60, 110, 170), "green_dark": (20, 50, 110)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = scales(P, "gold", "gold_dark", size=1.2)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 20.0, y - 27.0, 1.0, "eye", slit=True)
        if c is not None:
            return c, None
    return scales(P, "green", "green_dark", size=1.0)(x, y, z, face, variant, box=box, **k)


def legf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if y < 1.8:
        return tone(p["black"], face), None
    if y < 6.0:
        return fur(P, "white", "white_dark")(x, y, z, face, variant, box=box, **k)
    return GOLD(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("tyilinmon")
    mats = {"skin": GOLD, "belly": GOLD, "neck": GOLD, "head": headf, "leg": legf, "paw": legf, "claw": solid(P, "black"),
            "tail": GOLD}
    a = quadruped(m, mats, "tyilinmon", length=24.0, body_y=14.0, body_rx=5.6, body_ry=5.6, chest_bulk=1.15,
                  neck=((0, 20, -12), (0, 24, -15)), head_len=10.0, head_w=3.8, head_h=4.4, snout=0.6, mouth_open=10,
                  teeth=4, tail=((0, 16, 12),), tail_r=(2.0,), toes=0, claws=False)
    bd, hd = a["body"], a["head"]
    spike(m, hd, (0, a["mouth_y"], a["snout_front"] + 1.0), (0, -0.4, -1), 1.2, 6.0, solid(P, "red"), tip=0.8)
    for sx in (-1, 1):
        pts = [(sx * 2.0, 27.0, -15.0), (sx * 3.4, 30.0, -13.0), (sx * 2.6, 31.6, -11.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, metal(P, "gold"), extend=0.3)
    for j in range(7):                                                                 # white mane
        spike(m, hd, ((j - 3) * 0.8, 27.0, -11.0), ((j - 3) * 0.3, 0.6, 1), 1.4, 7.0, fur(P, "white", "white_dark"),
              tip=0.8)
    for i in range(8):                                                                 # jade collar
        ang = i * 2 * math.pi / 8
        ball(m, bd, (4.6 * math.sin(ang), 19.0 + 1.6 * math.cos(ang), -10.0 + 1.2 * math.cos(ang)), 1.0, solid(P, "jade"),
             layers=1)
    for sx in (-1, 1):
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 4.0, 19.0, -4.0))
        feather_wing(m, wb, (sx * 4.0, 19.0, -4.0), 18.0, 10.0, 3, feathers(P, "white", "white_dark"), side=sx,
                     sweep=40, droop=-8.0)
    tl = m.bone("tail", bd, (0, 16, 12))                                               # golden cloud-tail
    for j in range(7):
        ang = j * 0.9
        ball(m, tl, (2.4 * math.sin(ang), 18.0 + j * 0.8, 14.0 + 2.4 * math.cos(ang) + j * 0.4), 2.0, metal(P, "gold"),
             layers=1)
    for j in range(5):
        m.box(bd, -14.0 + j * 0.8, 20.0 + j * 2.4, -2.0, -12.6 + j * 0.8, 22.6 + j * 2.4, -1.0, solid(P, "bolt", glow=True),
              rotation=(0, 0, 25 if j % 2 else -25), pivot=(-13.0, 21.0 + j * 2.4, -1.5))
    return m
