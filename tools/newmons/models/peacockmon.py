"""Peacockmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Armor Digimon of sincerity: a lean bird-warrior in jagged blue armour bristling with blade-
feathers, a beaked blue helm, clawed armoured feet, and a great fan of translucent green energy feathers flaring
behind it. 15 blocks tall.

Front is -z, y is up. 60 units tall; Adult (Armor) stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(15, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a lean bird-warrior in jagged blue armour bristling with blade-feathers, a beaked helm and a great fan of green energy feathers"
BASE = {"blue": (60, 110, 210), "blue_dark": (20, 44, 130), "silver": (210, 214, 226), "silver_dark": (110, 116, 130),
        "green": (190, 250, 140, 160), "eye": (250, 220, 60)}
SHINY = {"blue": (200, 70, 160), "blue_dark": (120, 20, 90), "green": (255, 220, 120, 160)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "blue", "blue_dark", trim="silver", trim_w=0.25)


def build():
    m = Model("peacockmon")
    mats = {"skin": ARM, "claw": metal(P, "silver"), "talon": metal(P, "silver")}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.9, claws=True, talons=True, digitigrade=True,
                 name="peacockmon")
    bd = a["body"]
    for sx in (-1, 1):                                                                   # blade-feathers
        for j in range(4):
            spike(m, bd, (sx * 6.0, 50.0 - j * 3.0, 0.4), (sx * 0.9, 0.7 - j * 0.1, 0.4), 1.2, 6.0, ARM, tip=0.8)
    for nm in ("arm_left", "arm_right", "leg_left", "leg_right"):
        anc = a[nm]
        j = anc.get("elbow") or anc.get("knee")
        sx = 1 if j[0] > 0 else -1
        spike(m, anc["bone"], j, (sx, 0.3, 0.4), 1.0, 4.0, ARM, tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.4, 2.8, 54.0, 59.6, ARM, cut=1)
    spike(m, hd, (0, 56.6, -3.2), (0, -0.3, -1), 1.4, 4.0, metal(P, "silver"), tip=0.8)     # beak
    m.box(hd, -1.8, 57.6, -3.5, 1.8, 58.4, -3.3, solid(P, "eye", glow=True))
    for i in range(5):
        spike(m, hd, ((i - 2) * 0.8, 59.4, 0), ((i - 2) * 0.4, 1, 0.3), 1.0, 5.0, ARM, tip=0.8)
    for i in range(9):                                                                   # green energy fan
        ang = math.radians(-80 + i * 20)
        m.box(bd, -1.8, 40.0, 5.0, 1.8, 66.0, 5.0, solid(P, "green", glow=True), rotation=(0, 0, math.degrees(ang)),
              pivot=(0, 42.0, 5.0))
    return m
