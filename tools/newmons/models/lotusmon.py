"""Lotusmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the lotus priestess: a slender figure in a violet lotus-petal bodice and violet patterned leggings
under a wide white frilled skirt and sleeves, a violet lotus mask with golden hair, a jewelled staff topped with a
rainbow lotus, and a golden snake-wand coiled round a winged rod in the other hand. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage. Built as officially drawn (clothed).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fabric, gem, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a slender lotus priestess in a violet petal bodice under a white frilled skirt, a violet lotus mask, a rainbow lotus staff and a golden snake wand"
BASE = {"violet": (140, 70, 170), "violet_dark": (70, 24, 100), "white": (248, 246, 240), "white_dark": (200, 194, 180),
        "gold": (240, 200, 70), "gold_dark": (160, 120, 20), "silver": (210, 214, 224), "silver_dark": (100, 104, 116),
        "rb1": (240, 80, 80), "rb2": (250, 220, 60), "rb3": (80, 200, 120), "rb4": (80, 140, 240), "eye": (240, 220, 60)}
SHINY = {"violet": (60, 140, 200), "violet_dark": (20, 70, 130)}


def P(v):
    return pal(BASE, SHINY, v)


V = fabric(P, "violet", "violet_dark")
W = fabric(P, "white", "white_dark", period=1.4)


def build():
    m = Model("lotusmon")
    mats = {"skin": V, "chest": V, "abs": V, "pelvis": V, "neck": V, "deltoid": W, "upper_arm": W, "forearm": W,
            "hand": V, "finger": V, "thigh": V, "knee": V, "shin": V, "calf": V, "foot": solid(P, "violet_dark"),
            "toe": solid(P, "violet_dark")}
    a = humanoid(m, mats, bulk=0.75, arm_bulk=0.78, leg_bulk=0.8, name="lotusmon")
    bd = a["body"]
    for i in range(10):                                                              # wide white frilled skirt
        ang = 2 * math.pi * i / 10
        spike(m, bd, (3.6 * math.cos(ang), 34.0, 3.0 * math.sin(ang)), (math.cos(ang) * 0.9, -0.5, math.sin(ang) * 0.9),
              3.4, 11.0, W, tip=0.8)
    for sx in (-1, 1):                                                               # wide sleeves
        m.round_box(a["arm_left" if sx > 0 else "arm_right"]["bone"], sx * 8.4, -1.0, 2.6, 3.6, 36.0, 44.0, W, cut=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 60.0, V, cut=1)
    m.box(hd, -1.4, 57.4, -2.9, -0.4, 58.0, -2.8, solid(P, "eye", glow=True))
    m.box(hd, 0.4, 57.4, -2.9, 1.4, 58.0, -2.8, solid(P, "eye", glow=True))
    for i in range(5):                                                               # lotus-petal crown
        ang = math.radians(-60 + i * 30)
        spike(m, hd, (2.0 * math.sin(ang), 59.6, -0.6), (math.sin(ang) * 0.5, 1, -0.2), 1.6, 4.0, V, tip=0.8)
    for sx in (-1, 1):
        rod(m, hd, (sx * 2.2, 59.0, 0.6), (sx * 3.6, 54.0, 1.4), 2, strands(P, "gold", "gold_dark"), extend=0.3)
    hr = a["arm_right"]                                                              # rainbow lotus staff
    hx, hy, hz = hr["hand"]
    rod(m, hr["bone"], (hx, hy - 20.0, hz), (hx - 2.0, hy + 20.0, hz), 1, metal(P, "silver", dark="silver_dark"), extend=0, t2=1)
    for j, key in enumerate(("rb1", "rb2", "rb3", "rb4", "rb1")):
        ang = math.radians(-60 + j * 30)
        spike(m, hr["bone"], (hx - 2.0, hy + 20.0, hz), (math.sin(ang), math.cos(ang), 0), 1.0, 3.0, gem(P, key, "white"), tip=0.8)
    hl = a["arm_left"]                                                               # golden snake wand
    lx, ly, lz = hl["hand"]
    rod(m, hl["bone"], (lx - 4.0, ly, lz), (lx + 14.0, ly, lz), 1, metal(P, "gold", dark="gold_dark"), extend=0, t2=1)
    for j in range(5):
        spike(m, hl["bone"], (lx + 14.0, ly, lz), (1, (j - 2) * 0.4, 0), 0.8, 4.0, metal(P, "gold", dark="gold_dark"), tip=0.8)
    for t in range(8):
        a0 = t * 1.2
        m.round_box(hl["bone"], lx + t * 1.4, lz + 0.8 * math.sin(a0), 0.6, 0.6, ly + 0.8 * math.cos(a0) - 0.6,
                    ly + 0.8 * math.cos(a0) + 0.6, solid(P, "gold"), cut=0)
    return m
