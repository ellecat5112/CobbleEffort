"""Snimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a green mantis of thorny armour: a spiky green exoskeleton bristling with thorns, an orange-crested
insect head with red eyes and mandibles, two huge silver-and-black scythe blades for arms, four translucent wings and
clawed green legs. 15 blocks.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a thorny green mantis with an orange-crested head, red eyes, two huge silver-and-black scythe arms and translucent wings"
BASE = {"green": (70, 170, 70), "green_dark": (24, 90, 24), "orange": (240, 140, 40), "red": (220, 40, 40),
        "silver": (220, 224, 236), "silver_dark": (40, 40, 46), "wing": (220, 240, 250, 150)}
SHINY = {"green": (200, 80, 160), "green_dark": (120, 30, 90)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "green", "green_dark")


def build():
    m = Model("snimon")
    top = m.bone("snimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    ball(m, bd, (0, 18.0, 2.0), 5.0, ARM, layers=4, ry=6.0)
    for j in range(10):                                                                  # thorns
        ang = 2 * math.pi * j / 10
        spike(m, bd, (4.6 * math.cos(ang), 18.0 + (j % 3) * 2.0, 2.0 + 4.6 * math.sin(ang)),
              (math.cos(ang), 0.5, math.sin(ang)), 1.0, 3.0, ARM, tip=0.8)
    hd = m.bone("head", bd, (0, 24, -2))
    m.round_box(hd, 0, -4.0, 3.0, 3.0, 23.0, 28.0, ARM, cut=1)
    for sx in (-1, 1):
        ball(m, hd, (sx * 2.6, 27.0, -5.0), 1.2, solid(P, "red", glow=True), layers=1)
        spike(m, hd, (sx * 1.0, 23.0, -6.6), (sx * 0.5, -0.6, -1), 0.9, 2.6, metal(P, "silver"), tip=0.8)
    for j in range(5):                                                                   # orange crest
        spike(m, hd, ((j - 2) * 0.8, 28.0, -3.0), ((j - 2) * 0.3, 1, 0.4), 1.0, 4.0, solid(P, "orange"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                  # scythe arms
        ab = m.bone(nm, bd, (sx * 4.0, 22.0, -2.0))
        rod(m, ab, (sx * 4.0, 22.0, -2.0), (sx * 10.0, 26.0, -4.0), 2, ARM, extend=0.4)
        for j in range(6):
            ang = math.radians(10 + j * 22)
            c = (sx * (10.0 + 8.0 * math.sin(ang)), 26.0 + 10.0 * math.cos(ang) - 4.0, -4.0)
            m.box(ab, c[0] - 1.6, c[1] - 1.6, c[2] - 0.5, c[0] + 1.6, c[1] + 1.6, c[2] + 0.5,
                  metal(P, "silver", dark="silver_dark"))
    for sx in (-1, 1):                                                                   # translucent wings
        for j in range(2):
            x0, x1 = sorted((sx * 2.0, sx * 14.0))
            m.box(bd, x0, 20.0, 6.0 + j * 0.4, x1, 24.0, 6.0 + j * 0.4, solid(P, "wing"),
                  rotation=(0, -sx * 20, sx * (20 - j * 30)), pivot=(sx * 2.0, 22.0, 6.0))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.0, 13.0, 2.0))
        rod(m, lg, (sx * 3.0, 13.0, 2.0), (sx * 6.0, 6.0, 0.0), 2, ARM, extend=0.3)
        rod(m, lg, (sx * 6.0, 6.0, 0.0), (sx * 6.0, 1.0, -2.0), 2, ARM, extend=0.3)
        for f in range(3):
            spike(m, lg, (sx * 6.0 + (f - 1) * 1.0, 0.8, -2.4), ((f - 1) * 0.3, -0.2, -1), 0.8, 2.4, ARM, tip=0.8)
    return m
