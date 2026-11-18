"""Liamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
thunder lion: a powerful orange lion standing on its hind legs, a wild dark-brown mane braided with beads and feathers,
silver hoop earrings, a fanged roar, huge clawed paws with black claws and a tufted tail. 15 blocks tall.

Front is -z, y is up. 56 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fur, metal, solid, strands
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(15, HEIGHT, 3.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a powerful orange lion on its hind legs with a wild beaded dark mane, silver hoop earrings, huge clawed paws and a tufted tail"
BASE = {"orange": (240, 150, 50), "orange_dark": (170, 80, 20), "orange_light": (255, 210, 140), "mane": (110, 60, 30),
        "mane_dark": (60, 30, 10), "silver": (200, 210, 230), "silver_dark": (100, 110, 130), "black": (30, 28, 30),
        "eye": (60, 160, 90), "mouth": (160, 40, 40), "tooth": (250, 248, 236), "bead": (240, 230, 220), "red": (210, 50, 40)}
SHINY = {"orange": (230, 220, 160), "orange_dark": (170, 150, 90), "mane": (200, 80, 40), "mane_dark": (130, 40, 14)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "orange", "orange_dark", tip="orange_light", length=1.0)


def build():
    m = Model("liamon")
    mats = {"skin": FUR, "chest": FUR, "abs": FUR, "pelvis": FUR, "neck": FUR, "deltoid": FUR, "upper_arm": FUR,
            "forearm": FUR, "hand": FUR, "finger": FUR, "claw": solid(P, "black"), "thigh": FUR, "knee": FUR,
            "shin": FUR, "calf": FUR, "foot": FUR, "talon": solid(P, "black")}
    a = humanoid(m, mats, bulk=1.1, arm_bulk=1.15, leg_bulk=1.2, claws=True, talons=True, digitigrade=True, name="liamon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, -1))
    m.round_box(hd, 0, -1.6, 3.2, 3.6, 53.0, 60.4, FUR, cut=1)
    m.round_box(hd, 0, -5.2, 2.2, 1.6, 53.4, 57.0, FUR, cut=1)
    m.round_box(hd, 0, -6.6, 1.8, 0.4, 53.6, 55.4, solid(P, "mouth"), cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.4), 58.0, -5.3, max(sx * 1.0, sx * 2.4), 58.8, -5.1, solid(P, "eye"))
        spike(m, hd, (sx * 1.0, 55.4, -6.6), (0, -1, 0), 0.8, 1.6, solid(P, "tooth"), tip=0.8)
        for t in range(6):                                                           # silver hoops
            a0, a1 = 2 * math.pi * t / 6, 2 * math.pi * (t + 1) / 6
            rod(m, hd, (sx * 4.0, 56.0 + 1.4 * math.sin(a0), -1.0 + 1.4 * math.cos(a0)),
                (sx * 4.0, 56.0 + 1.4 * math.sin(a1), -1.0 + 1.4 * math.cos(a1)), 1, metal(P, "silver", dark="silver_dark"),
                extend=0.1, t2=1)
    MANE = strands(P, "mane", "mane_dark")
    for ring, (r, n, ln) in enumerate(((3.8, 14, 6.0), (5.0, 16, 9.0))):            # wild mane
        for i in range(n):
            ang = 2 * math.pi * (i + ring * 0.5) / n
            spike(m, hd, (r * math.cos(ang) * 0.9, 57.0 + r * math.sin(ang), ring * 1.2),
                  (math.cos(ang), math.sin(ang), 0.6), 2.2, ln, MANE, tip=0.8)
    for j in range(4):                                                               # beaded braids
        x0 = -3.0 + j * 2.0
        rod(m, hd, (x0, 54.0, 2.0), (x0 * 1.4, 46.0, 3.0), 1, MANE, extend=0.2, t2=1)
        m.round_box(hd, x0 * 1.4, 3.0, 0.6, 0.6, 45.0, 46.4, solid(P, "bead" if j % 2 else "red"), cut=0)
    tb = m.bone("tail", bd, (0, 32, 3))
    pts = [(0, 32.0, 3.4), (3.0, 30.0, 10.0), (5.0, 36.0, 14.0), (6.0, 42.0, 13.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 1, FUR, extend=0.3, t2=2)
    for j in range(4):
        spike(m, tb, pts[-1], ((j - 1.5) * 0.3, 1, 0), 1.2, 3.0, MANE, tip=0.8)
    return m
