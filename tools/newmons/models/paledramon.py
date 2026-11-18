"""Paledramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): an ice dragon: a dragon of pale crystal-blue ice plates and white fur, a jagged ice-crowned head
with red eyes, a thick white fur ruff, an armoured arm gauntlet, long dark-blue claws, and wings and spines of jagged
blue ice crystal. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import theropod
from _digidetail import armour, fur, local, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "an ice dragon of pale crystal-blue plates and white fur, a jagged ice crown, a thick fur ruff, dark claws and ice-crystal wings"
BASE = {"ice": (170, 210, 250), "ice_dark": (80, 130, 210), "white": (246, 248, 252), "white_dark": (190, 200, 220),
        "navy": (40, 60, 140), "eye": (240, 50, 70), "crystal": (190, 230, 255, 190), "mouth": (100, 60, 120),
        "tooth": (250, 250, 255)}
SHINY = {"ice": (250, 200, 210), "ice_dark": (200, 120, 150), "crystal": (255, 210, 230, 190)}


def P(v):
    return pal(BASE, SHINY, v)


ICE = armour(P, "ice", "ice_dark", trim="white", trim_w=0.2)
FUR = fur(P, "white", "white_dark", length=1.4)


def build():
    m = Model("paledramon")
    mats = {"skin": ICE, "belly": FUR, "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "claw": solid(P, "navy"),
            "talon": solid(P, "navy")}
    a = theropod(m, mats, "paledramon", hip_y=16.0, chest=(0, 25.0, -4.0), body_r=5.4, chest_r=5.6,
                 neck_top=(0, 30.0, -9.0), head_len=9.0, head_w=3.4, head_h=3.6, mouth_open=16, teeth=5,
                 arm_len=9.0, arm_bulk=1.3, leg_bulk=1.2)
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.6,
              solid(P, "eye", glow=True))
    for i in range(5):                                                                   # jagged ice crown
        spike(m, hd, ((i - 2) * 1.0, ey + 2.0, ez + 2.0), ((i - 2) * 0.3, 1, 0.5), 1.2, 4.0 + (2 - abs(i - 2)),
              solid(P, "crystal", glow=True), tip=0.8)
    for i in range(10):                                                                  # fur ruff
        ang = 2 * math.pi * i / 10
        spike(m, bd, (5.0 * math.cos(ang), 28.0, -5.0 + 3.0 * math.sin(ang)), (math.cos(ang), 0.2, math.sin(ang)), 2.0,
              4.0, FUR, tip=0.8)
    for side in (1, -1):                                                                 # ice-crystal wings
        for j in range(4):
            spike(m, bd, (side * 3.0, 28.0, 3.0), (side * 1, 0.8 - j * 0.35, 0.6), 1.6, 14.0 - j * 2.0,
                  solid(P, "crystal", glow=True), tip=0.8)
    for j in range(5):                                                                   # back spines
        spike(m, bd, (0, 26.0 - j * 3.0, 4.0 + j), (0, 1, 0.5), 1.2, 4.0, solid(P, "crystal", glow=True), tip=0.8)
    return m
