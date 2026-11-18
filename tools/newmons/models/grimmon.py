"""Grimmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the devil dragon of the Ghost Game: a lean black-armoured dragon-man with a wild blond mane, a
blazing white-hot core blazing in his chest ringed with spikes, jagged black-and-gold wings, a long segmented
black-and-silver tail and one arm ending in a great silver blade-claw. 15 blocks tall.

Front is -z, y is up. 60 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, gem, local, metal, solid, strands
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a lean black-armoured dragon-man with a wild blond mane, a blazing spiked core in his chest, jagged "
        "black-and-gold wings, a segmented tail and a great silver blade-claw")
BASE = {"black": (34, 32, 38), "black_dark": (12, 12, 16), "black_light": (100, 96, 110), "gold": (240, 200, 70),
        "gold_dark": (160, 120, 20), "silver": (214, 218, 228), "silver_dark": (110, 114, 126), "core": (255, 220, 230),
        "core_light": (255, 255, 255), "mane": (240, 210, 110), "mane_dark": (180, 140, 40), "eye": (240, 40, 60),
        "glow": (255, 170, 80, 160)}
SHINY = {"black": (230, 230, 240), "black_dark": (160, 160, 176), "black_light": (255, 255, 255), "core": (130, 200, 255)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "black", "black_dark", light="black_light", trim="gold", trim_w=0.3)
SILVER = metal(P, "silver", dark="silver_dark")


def build():
    m = Model("grimmon")
    mats = {"skin": ARM, "claw": SILVER, "talon": SILVER}
    a = humanoid(m, mats, bulk=0.9, arm_bulk=0.95, leg_bulk=1.0, claws=True, talons=True, digitigrade=True,
                 name="grimmon")
    bd = a["body"]
    m.round_box(bd, 0, -3.6, 3.0, 1.0, 42.0, 48.0, gem(P, "core", "core_light"), cut=1)       # blazing core
    for j in range(8):
        ang = 2 * math.pi * j / 8
        spike(m, bd, (3.4 * math.cos(ang), 45.0 + 3.4 * math.sin(ang), -4.0), (math.cos(ang), math.sin(ang), -0.3), 1.0,
              4.0, SILVER, tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 2.6, 3.4, 53.6, 59.6, ARM, cut=1)
    m.round_box(hd, 0, -4.6, 1.6, 1.4, 54.0, 57.0, ARM, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.2), 57.4, -4.5, max(sx * 0.8, sx * 2.2), 58.2, -4.3, solid(P, "eye", glow=True))
    for i in range(12):                                                                   # wild blond mane
        ang = math.radians(-120 + i * 22)
        spike(m, hd, (2.4 * math.sin(ang), 59.0, 0.6 + 2.0 * math.cos(ang) + 1.0), (math.sin(ang) * 0.8, 0.9, 0.7), 1.6,
              7.0 + (i % 3) * 2.0, strands(P, "mane", "mane_dark"), tip=0.8)
    for side in (1, -1):                                                                  # jagged wings
        for j in range(3):
            spike(m, bd, (side * 3.0, 50.0 - j * 2.0, 4.0), (side * 1.0, 0.7 - j * 0.3, 0.6), 2.0, 16.0 - j * 3.0,
                  armour(P, "black", "black_dark", trim="gold", trim_w=0.4), tip=0.9)
    tb = m.bone("tail", bd, (0, 32, 3))                                                    # segmented tail
    pts = [(0, 32.0, 3.0), (3.0, 24.0, 10.0), (8.0, 20.0, 15.0), (14.0, 22.0, 17.0), (18.0, 27.0, 15.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tb, p0, p1, 3 - j // 2, ARM if j % 2 == 0 else SILVER, extend=0.4)
    ar, h = a["arm_right"]["bone"], a["arm_right"]["hand"]                                   # great blade-claw
    for j in range(3):
        spike(m, ar, (h[0] + (j - 1) * 1.2, h[1], h[2] - 1.0), ((j - 1) * 0.4, -0.6, -1), 1.4, 10.0, SILVER, tip=0.8)
    return m
