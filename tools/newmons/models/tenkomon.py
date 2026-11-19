"""Tenkomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a celestial fox of snow: a slender lavender-white fox with a long pointed muzzle, swept-back ears,
a great cloud of a white chest mane, starry violet-dusted legs ringed with indigo bands, and nine enormous billowing
cloud-like tails piled up behind it. 15 blocks.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digidetail import eye, fur, plane, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 14}
LOOK = "a slender lavender-white celestial fox with a cloud of a chest mane, starry legs and nine enormous billowing cloud tails"
BASE = {"white": (240, 240, 250), "white_dark": (190, 186, 220), "lav": (190, 180, 230), "lav_dark": (130, 110, 190),
        "band": (50, 50, 120), "star": (255, 255, 255), "eye": (220, 60, 120), "pupil": (40, 10, 30),
        "tail": (224, 222, 246, 230), "nose": (60, 50, 80)}
SHINY = {"lav": (240, 200, 150), "lav_dark": (190, 140, 90), "tail": (250, 230, 200, 230)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = fur(P, "white", "white_dark", length=1.6)


def legf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if 3.0 < y < 4.2:
        return tone(p["band"], face), None
    if y < 3.0:
        return tone(p["white"], face), None
    if (int(x * 3.1) * 7 + int(y * 2.7) * 13 + int(z * 3.3) * 5) % 23 == 0:
        return p["star"], p["star"]
    return fur(P, "lav", "lav_dark", length=1.0)(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 21.4, y - 31.0, 0.9, "eye", slit=True)
        if c is not None:
            return c, None
    return WHITE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("tenkomon")
    mats = {"skin": fur(P, "lav", "lav_dark", length=1.0), "belly": WHITE, "neck": WHITE, "head": headf, "leg": legf,
            "paw": legf, "claw": solid(P, "white"), "tail": WHITE}
    a = quadruped(m, mats, "tenkomon", length=22.0, body_y=16.0, body_rx=5.0, body_ry=5.0, chest_bulk=1.2,
                  neck=((0, 24, -12), (0, 30, -16)), head_len=9.0, head_w=3.6, head_h=4.4, snout=0.7, mouth_open=0,
                  tail=((0, 18, 11), (0, 20, 14)), tail_r=(2.4, 2.0), toes=3, claws=False)
    bd, hd = a["body"], a["head"]
    for i in range(7):                                                                 # chest mane cloud
        ang = (i - 3) * 0.45
        ball(m, bd, (math.sin(ang) * 4.0, 22.0 + math.cos(ang) * 3.0, -13.0 + abs(ang) * 1.5), 3.4, WHITE, layers=2)
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.4, 33.6, -14.0), (sx * 0.5, 0.8, 0.9), 1.8, 5.0, WHITE, tip=0.8)
        for j in range(3):                                                             # flowing head plumes
            spike(m, hd, (sx * 1.4, 33.0, -13.0), (sx * 0.3, 0.3 + j * 0.2, 1), 1.2, 7.0 + j * 2.0, WHITE, tip=0.8)
    spike(m, hd, (0, 30.0, a["snout_front"]), (0, 0, -1), 1.0, 0.8, solid(P, "nose"), tip=0.8)
    tl = m.bone("tails", bd, (0, 20, 12))                                              # nine cloud tails
    for i in range(9):
        ang = (i - 4) * 0.36
        for j in range(4):
            r = 4.6 + j * 0.8
            cx = math.sin(ang) * (6.0 + j * 4.0)
            cy = 22.0 + j * 4.4 + math.cos(ang) * 2.0
            cz = 14.0 + j * 1.6 - abs(ang) * 2.0
            ball(m, tl, (cx, cy, cz), r, solid(P, "tail"), layers=2)
    return m
