"""Wankomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a lucky shrine pup: a white puppy with a black mask and ears lined pink, a little gold horn, big
eyes, red cheek marks and a lolling tongue, a blue cloth bib patterned with gold swirls tied with a red bow, black
paws, and a huge curling grey-and-white tail holding a red-and-gold temple ball. 1 block.

Front is -z, y is up. Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digidetail import eye, fabric, fur, metal, plane, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(1.0, HEIGHT, 1.6)
KIND = "quadruped"
K = 4
ANIM = {"leg_amp": 16}
LOOK = "a white shrine puppy with a black mask, a little gold horn, a blue swirl-patterned bib, a lolling tongue and a huge curling tail"
BASE = {"white": (248, 248, 252), "white_dark": (200, 200, 214), "black": (40, 38, 46), "black_dark": (14, 14, 18),
        "pink": (240, 140, 170), "gold": (240, 196, 60), "blue": (70, 110, 200), "blue_dark": (30, 50, 120),
        "red": (210, 40, 40), "eye": (30, 26, 30), "tongue": (240, 120, 140), "grey": (110, 110, 120),
        "pupil": (14, 12, 14), "white": (255, 255, 255)}
SHINY = {"black": (150, 100, 60), "black_dark": (90, 50, 24), "blue": (60, 160, 110), "blue_dark": (20, 100, 60)}


def P(v):
    return pal(BASE, SHINY, v)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            c = eye(p, a - sx * 1.6, b - 13.4, 0.9, "eye")
            if c is not None:
                return c, None
            if abs(a - sx * 3.0) < 0.8 and abs(b - 12.0) < 0.25:
                return p["red"], None
        if b > 14.6:
            return tone(p["black"], face), None
    if y > 14.6 and face != "down":
        return tone(p["black"], face), None
    return fur(P, "white", "white_dark", length=0.8)(x, y, z, face, variant, box=box, **k)


def bibf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(math.sin(x * 1.2) * math.cos(y * 1.3)) > 0.85:
        return tone(p["gold"], face), None
    return fabric(P, "blue", "blue_dark")(x, y, z, face, variant, box=box, **k)


def pawf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if y < 2.4:
        return tone(p["black"], face), None
    return fur(P, "white", "white_dark", length=0.8)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("wankomon")
    mats = {"skin": fur(P, "white", "white_dark", length=0.8), "belly": fur(P, "white", "white_dark"), "neck": bibf,
            "head": headf, "leg": pawf, "paw": pawf, "claw": solid(P, "black"), "tail": fur(P, "grey", "black")}
    a = quadruped(m, mats, "wankomon", length=12.0, body_y=7.0, body_rx=3.6, body_ry=3.4, chest_bulk=1.1,
                  neck=((0, 9, -6), (0, 11, -7)), head_len=7.0, head_w=4.0, head_h=4.4, snout=0.2, mouth_open=12,
                  tail=((0, 9, 6),), tail_r=(1.6,), toes=0, claws=False)
    bd, hd = a["body"], a["head"]
    m.round_box(bd, 0, -4.4, 4.4, 2.2, 5.0, 10.0, bibf, cut=1)                             # blue bib
    m.box(bd, -2.0, 9.6, -7.0, 2.0, 11.0, -6.0, solid(P, "red"))
    spike(m, hd, (0, 15.4, -7.6), (0, 1, -0.3), 1.2, 2.4, metal(P, "gold"), tip=0.8)
    m.box(hd, -0.9, 8.6, -11.6, 0.9, 9.4, -9.0, solid(P, "tongue"), rotation=(30, 0, 0), pivot=(0, 9.0, -9.2))
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.6, 14.6, -6.6), (sx * 0.3, 1, 0.2), 1.8, 4.0, solid(P, "black"), tip=0.8)
        m.box(hd, sx * 2.6 - 0.5, 15.6, -7.6, sx * 2.6 + 0.5, 17.6, -7.4, solid(P, "pink"))
    tl = m.bone("tail_curl", bd, (0, 9, 6))                                              # huge curling tail
    for i in range(10):
        ang = i * 0.55
        r = 7.0 - i * 0.35
        c = (0, 14.0 + r * math.sin(ang), 9.0 + r * math.cos(ang) * 0.6)
        ball(m, tl, c, 2.6 - i * 0.12, fur(P, "grey" if i > 4 else "white", "black"), layers=2)
    ball(m, tl, (0, 22.0, 9.0), 2.4, solid(P, "red"), layers=2)                           # temple ball
    m.round_box(tl, 0, 9.0, 2.5, 2.5, 21.6, 22.4, metal(P, "gold"), cut=1)
    return m
