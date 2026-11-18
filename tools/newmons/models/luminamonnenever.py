"""Luminamon (Nene Ver.) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the manga art on
wikimon.net): Luminamon fused with its partner, a slender angel girl with short brown hair, a golden halo, long thin
curling ribbon antennae, one great white feathered wing, and a white fluffy fur tunic with fur cuffs and a dark anklet.
25 blocks tall. Built modestly: the fur outfit is a full tunic and no anatomy is modelled.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digibody import humanoid
from _digidetail import feathers, fur, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a slender angel girl with short brown hair, a golden halo, curling ribbon antennae, one great white wing and a white fur tunic"
BASE = {"white": (250, 250, 252), "white_dark": (200, 200, 214), "skin": (250, 226, 212), "skin_dark": (210, 170, 150),
        "hair": (150, 100, 90), "hair_dark": (90, 56, 50), "gold": (250, 220, 90), "eye": (220, 60, 140),
        "ribbon": (140, 90, 80), "black": (30, 28, 30)}
SHINY = {"hair": (230, 200, 120), "hair_dark": (170, 140, 60)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "white", "white_dark", length=0.8)
SK = skin(P, "skin", dark="skin_dark")


def build():
    m = Model("luminamonnenever")
    mats = {"skin": SK, "chest": FUR, "abs": FUR, "pelvis": FUR, "neck": SK, "deltoid": SK, "upper_arm": SK,
            "forearm": SK, "hand": SK, "finger": SK, "thigh": FUR, "knee": SK, "shin": SK, "calf": SK, "foot": SK, "toe": SK}
    a = humanoid(m, mats, bulk=0.74, arm_bulk=0.74, leg_bulk=0.8, name="luminamonnenever")
    bd = a["body"]
    for i in range(8):                                                               # fur tunic hem
        ang = 2 * math.pi * i / 8
        spike(m, bd, (3.2 * math.cos(ang), 33.0, 2.6 * math.sin(ang)), (math.cos(ang) * 0.3, -1, math.sin(ang) * 0.3), 2.6,
              5.0, FUR, tip=0.8)
    for nm in ("arm_left", "arm_right"):                                              # fur cuffs
        w = a[nm]["wrist"]
        m.round_box(a[nm]["bone"], w[0], w[2], 1.6, 1.6, w[1] - 0.2, w[1] + 1.6, FUR, cut=1)
    ank = a["leg_left"]["ankle"]
    m.round_box(a["leg_left"]["bone"], ank[0], ank[2], 1.4, 1.4, ank[1] + 1.0, ank[1] + 2.0, solid(P, "black"), cut=0)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 60.0, SK, cut=1)
    m.box(hd, -1.4, 57.2, -2.9, -0.4, 58.0, -2.8, solid(P, "eye"))
    m.box(hd, 0.4, 57.2, -2.9, 1.4, 58.0, -2.8, solid(P, "eye"))
    m.round_box(hd, 0, 0.4, 2.8, 2.8, 57.6, 61.0, strands(P, "hair", "hair_dark"), cut=1)       # short hair
    for i in range(7):
        ang = math.radians(-90 + i * 30)
        spike(m, hd, (2.4 * math.sin(ang), 59.0, 0.4 + 1.4 * math.cos(ang)), (math.sin(ang) * 0.6, -1, 0.3), 1.2, 3.0,
              strands(P, "hair", "hair_dark"), tip=0.8)
    hb = m.bone("ring_halo", hd, (0, 63, 0))
    for i in range(10):
        a0, a1 = 2 * math.pi * i / 10, 2 * math.pi * (i + 1) / 10
        rod(m, hb, (2.8 * math.cos(a0), 63.0, 2.8 * math.sin(a0)), (2.8 * math.cos(a1), 63.0, 2.8 * math.sin(a1)), 1,
            solid(P, "gold", glow=True), extend=0.1, t2=1)
    for sx in (-1, 1):                                                               # ribbon antennae
        pts = [(sx * 1.4, 60.6, 0), (sx * 6.0, 66.0, 1.0), (sx * 9.0, 56.0, 2.0), (sx * 8.0, 44.0, 2.0), (sx * 10.0, 40.0, 2.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "ribbon"), extend=0.1, t2=1)
    wb = m.bone("wing_left", bd, (2.6, 50.0, 3.4))                                   # one great white wing
    feather_wing(m, wb, (2.6, 50.0, 3.4), 24.0, 10.0, 3, feathers(P, "white", "white_dark"), side=1, sweep=10, droop=-20.0)
    return m
