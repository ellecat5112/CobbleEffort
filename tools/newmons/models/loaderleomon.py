"""Loader Leomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the heavy-duty lion machine: a golden armoured lion-mech crouched forward, a lion helm with a green eye, a
hazard-striped yellow body, a crane arm on its back swinging a black spiked wrecking ball, and huge clawed gauntlets
and feet tipped with silver drill claws. 25 blocks tall.

Front is -z, y is up. 48 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, metal, solid, strands
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(25, HEIGHT, 4.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a golden armoured lion-mech with a lion helm, a crane arm swinging a spiked wrecking ball, and huge silver drill claws"
BASE = {"gold": (240, 190, 50), "gold_dark": (160, 110, 14), "gold_light": (255, 235, 150), "black": (30, 30, 36),
        "silver": (220, 224, 234), "silver_dark": (110, 114, 126), "eye": (60, 230, 120), "mane": (230, 170, 40),
        "mane_dark": (150, 90, 10)}
SHINY = {"gold": (220, 70, 60), "gold_dark": (130, 20, 14), "gold_light": (250, 160, 140)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "gold", "gold_dark", light="gold_light", trim="black", trim_w=0.25, rivets=True)
SIL = metal(P, "silver", dark="silver_dark")


def hazf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (x + y) % 3.0 < 1.0:
        return tone(p["black"], face), None
    return ARM(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("loaderleomon")
    mats = {"skin": ARM, "chest": hazf, "abs": ARM, "pelvis": ARM, "neck": ARM, "deltoid": ARM, "upper_arm": ARM,
            "forearm": ARM, "hand": ARM, "finger": ARM, "claw": SIL, "thigh": ARM, "knee": ARM, "shin": ARM, "calf": ARM,
            "foot": ARM, "talon": SIL}
    a = humanoid(m, mats, bulk=1.25, arm_bulk=1.35, leg_bulk=1.3, claws=True, talons=True, digitigrade=True,
                 name="loaderleomon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, -1))
    m.round_box(hd, 0, -1.6, 3.4, 3.8, 53.0, 60.4, ARM, cut=1)
    m.round_box(hd, 0, -5.4, 2.4, 1.6, 53.4, 57.0, ARM, cut=1)
    m.box(hd, -0.8, 57.6, -5.5, 0.8, 58.6, -5.3, solid(P, "eye", glow=True))
    for i in range(12):                                                              # metal mane plates
        ang = 2 * math.pi * i / 12
        spike(m, hd, (3.6 * math.cos(ang), 57.0 + 3.6 * math.sin(ang), 0.6), (math.cos(ang), math.sin(ang), 0.5), 1.8, 4.0,
              metal(P, "mane", dark="mane_dark"), tip=0.8)
    cb = m.bone("crane", bd, (4, 50, 4))                                              # crane arm + wrecking ball
    rod(m, cb, (3.0, 50.0, 4.0), (6.0, 60.0, 4.0), 2, ARM, extend=0.6)
    rod(m, cb, (6.0, 60.0, 4.0), (12.0, 64.0, 2.0), 2, ARM, extend=0.6)
    rod(m, cb, (12.0, 64.0, 2.0), (13.0, 58.0, 2.0), 1, solid(P, "black"), extend=0, t2=1)
    ball(m, cb, (13.0, 55.0, 2.0), 3.4, metal(P, "black", dark="black"), layers=3)
    for j in range(8):
        ang = 2 * math.pi * j / 8
        spike(m, cb, (13.0 + 3.0 * math.cos(ang), 55.0 + 3.0 * math.sin(ang), 2.0), (math.cos(ang), math.sin(ang), 0), 1.0,
              2.4, SIL, tip=0.8)
    for nm in ("arm_left", "arm_right"):                                              # drill claws
        hx, hy, hz = a[nm]["hand"]
        for j in range(3):
            spike(m, a[nm]["bone"], (hx + (j - 1) * 1.4, hy - 2.0, hz - 1.0), (0, -1, -0.6), 1.4, 6.0, SIL, tip=0.8)
    return m
