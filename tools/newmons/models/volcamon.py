"""Volcamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a burly cyborg brawler: a black helmet with a V visor, a little smoking volcano erupting from its
head, heavy riveted silver chest armour stamped D-1, a red armband, green camouflage trousers, huge black boxing-glove
fists and heavy black boots. 25 blocks.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, fabric, leather, metal, riveted, solid
from _route import pal, tone

HEIGHT = 77
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a burly cyborg brawler with a V-visored black helmet, a smoking volcano on its head, silver chest armour and green camo trousers"
BASE = {"silver": (190, 194, 206), "silver_dark": (90, 94, 106), "black": (34, 32, 36), "black_dark": (12, 12, 14),
        "green": (70, 120, 60), "green_dark": (30, 70, 30), "camo": (110, 90, 50), "red": (200, 40, 40),
        "rock": (90, 70, 60), "lava": (255, 110, 30), "smoke": (210, 210, 216, 180), "yellow": (250, 210, 60)}
SHINY = {"silver": (200, 170, 100), "silver_dark": (130, 100, 40), "green": (60, 80, 130), "green_dark": (24, 34, 80)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = riveted(P, "silver", "silver_dark")
BLACK = leather(P, "black", "black_dark")


def camof(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    v = math.sin(x * 0.9 + z * 0.7) + math.cos(y * 0.8 - x * 0.4)
    if v > 1.0:
        return tone(p["camo"], face), None
    if v < -0.8:
        return tone(p["green_dark"], face), None
    return fabric(P, "green", "green_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("volcamon")
    mats = {"skin": ARM, "chest": ARM, "abs": ARM, "pelvis": BLACK, "deltoid": ARM, "upper_arm": ARM, "forearm": ARM,
            "hand": BLACK, "finger": BLACK, "thigh": camof, "knee": camof, "shin": ARM, "calf": ARM, "foot": BLACK,
            "neck": BLACK}
    a = humanoid(m, mats, bulk=1.45, arm_bulk=1.4, leg_bulk=1.35, name="volcamon")
    bd = a["body"]
    for nm in ("arm_left", "arm_right"):                                               # boxing-glove fists
        ball(m, a[nm]["bone"], a[nm]["hand"], 3.8, BLACK, layers=3)
    m.round_box(a["arm_right"]["bone"], a["arm_right"]["elbow"][0], 0, 2.6, 2.6, 41.0, 43.0, solid(P, "red"), cut=0)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 3.4, 3.6, 54.0, 61.0, BLACK, cut=2)
    for sx in (-1, 1):                                                                  # V visor
        m.box(hd, min(0.0, sx * 2.4), 57.6, -3.9, max(0.0, sx * 2.4), 58.4, -3.5, solid(P, "yellow", glow=True),
              rotation=(0, 0, -sx * 30), pivot=(0, 57.0, -3.7))
    vb = m.bone("volcano", hd, (0, 61, 0))                                             # erupting volcano
    for j in range(3):
        r = 2.6 - j * 0.7
        m.round_box(vb, 0, 0, r, r, 61.0 + j * 1.4, 62.4 + j * 1.4, solid(P, "rock"), cut=0)
    ball(m, vb, (0, 65.0, 0), 0.9, solid(P, "lava", glow=True), layers=1)
    for j in range(4):
        ball(m, vb, ((j % 2) * 1.4 - 0.7, 68.0 + j * 2.0, 0), 2.0 + j * 0.4, solid(P, "smoke"), layers=1)
    return m
