"""Venusmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net; built covered): one of the Olympos Twelve, the goddess of love: a serene figure blindfolded with a
white ribbon, long golden hair braided into great coils with pearl strings, a full-length white gown with long
flowing sleeves and ribbon streamers, white armoured boots, and a white dove perched on her raised hand. 35 blocks.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, fabric, feathers, skin, solid, strands
from _route import pal, tone

HEIGHT = 62
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a serene blindfolded goddess with coiled golden braids, a full-length white gown with flowing ribbons and a white dove"
BASE = {"white": (248, 248, 252), "white_dark": (196, 200, 214), "gold": (240, 214, 120), "gold_dark": (190, 150, 60),
        "skin": (250, 226, 210), "skin_dark": (210, 176, 160), "pearl": (250, 246, 236), "silver": (210, 214, 226),
        "silver_dark": (130, 134, 150)}
SHINY = {"white": (240, 200, 220), "white_dark": (190, 140, 170), "gold": (200, 210, 240), "gold_dark": (130, 140, 190)}


def P(v):
    return pal(BASE, SHINY, v)


GOWN = fabric(P, "white", "white_dark")
SKIN = skin(P, "skin", dark="skin_dark")
HAIR = strands(P, "gold", "gold_dark")


def build():
    m = Model("venusmon")
    mats = {"skin": SKIN, "chest": GOWN, "abs": GOWN, "pelvis": GOWN, "deltoid": GOWN, "upper_arm": GOWN,
            "forearm": GOWN, "hand": SKIN, "thigh": GOWN, "knee": GOWN, "shin": armour(P, "silver", "silver_dark"),
            "calf": armour(P, "silver", "silver_dark"), "foot": armour(P, "silver", "silver_dark"), "neck": SKIN}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.8, leg_bulk=0.85, name="venusmon")
    bd = a["body"]
    for i in range(10):                                                                 # full-length gown skirt
        ang = i * 2 * math.pi / 10
        r0, r1 = 4.4, 7.0
        cx, cz = r1 * math.sin(ang) * 0.8, r1 * math.cos(ang) * 0.7
        m.box(bd, cx - 2.0, 4.0, cz - 0.5, cx + 2.0, 32.0, cz + 0.5, GOWN, rotation=(0, math.degrees(ang), 0),
              pivot=(cx, 18.0, cz))
    for nm in ("arm_left", "arm_right"):                                               # flowing sleeves
        w = a[nm]["wrist"]
        m.box(a[nm]["bone"], w[0] - 2.4, w[1] - 6.0, w[2] - 1.0, w[0] + 2.4, w[1] + 4.0, w[2] + 2.6, GOWN)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.8, 3.0, 54.0, 61.0, SKIN, cut=1)
    m.box(hd, -3.0, 57.6, -3.3, 3.0, 59.0, -2.9, solid(P, "white"))                        # blindfold
    m.round_box(hd, 0, 0.8, 3.2, 3.0, 58.4, 62.0, HAIR, cut=1)
    for sx in (-1, 1):                                                                  # coiled braids
        for j in range(6):
            c = (sx * (4.4 + 0.6 * math.sin(j)), 58.0 - j * 4.0, 1.0)
            ball(m, hd, c, 1.8 - j * 0.12, HAIR, layers=2)
            ball(m, hd, (c[0] + sx * 1.2, c[1] - 1.6, c[2] - 1.0), 0.5, solid(P, "pearl"), layers=1)
    for j in range(3):                                                                  # ribbon streamers
        m.box(bd, -10.0 + j * 1.0, 8.0 + j * 6.0, 3.0, -2.0 + j * 1.0, 9.0 + j * 6.0, 3.6, GOWN,
              rotation=(0, 0, -20 + j * 15), pivot=(-6.0, 8.5 + j * 6.0, 3.3))
    h = a["arm_left"]["hand"]                                                           # dove on the raised hand
    db = m.bone("dove", a["arm_left"]["bone"], h)
    ball(m, db, (h[0], h[1] + 2.4, h[2]), 1.4, feathers(P, "white", "white_dark"), layers=2)
    for sx in (-1, 1):
        spike(m, db, (h[0] + sx * 1.0, h[1] + 2.8, h[2]), (sx, 0.8, 0.2), 0.9, 3.0, feathers(P, "white", "white_dark"),
              tip=0.8)
    return m
