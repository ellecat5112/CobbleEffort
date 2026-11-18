"""Lamortmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the hare of death: a hunched golden-furred beast with three long black-tipped blade ears, a fanged
snarl and red eyes, golden armour gauntlets with great black claws, black wing-like fur blades on its back and arms,
and swirling blue wind round its claws. 25 blocks tall.

Front is -z, y is up. 44 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, fur, solid, strands
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a hunched golden-furred hare beast with three long black-tipped blade ears, gold gauntlets with black claws and black fur blades"
BASE = {"gold": (220, 180, 90), "gold_dark": (150, 110, 40), "gold_light": (250, 230, 160), "black": (34, 32, 36),
        "black_dark": (10, 10, 12), "armour": (220, 180, 60), "armour_dark": (140, 100, 20), "red": (220, 40, 40),
        "mouth": (150, 30, 40), "tooth": (250, 248, 236), "wind": (120, 200, 255)}
SHINY = {"gold": (200, 200, 210), "gold_dark": (120, 120, 134), "gold_light": (250, 250, 255)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "gold", "gold_dark", tip="gold_light", length=1.6)
ARM = armour(P, "armour", "armour_dark")
BLADE = strands(P, "black", "black_dark")


def build():
    m = Model("lamortmon")
    top = m.bone("lamortmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    ball(m, bd, (0, 22.0, 1.0), 9.0, FUR, layers=6, squash=1.1)
    hd = m.bone("head", bd, (0, 30, -4))
    m.round_box(hd, 0, -6.0, 4.0, 4.4, 26.0, 33.0, FUR, cut=2)
    m.round_box(hd, 0, -10.0, 2.4, 1.0, 26.6, 28.6, solid(P, "mouth"), cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.2, sx * 2.8), 30.6, -10.6, max(sx * 1.2, sx * 2.8), 31.4, -10.4, solid(P, "red", glow=True))
        for j in range(2):
            spike(m, hd, (sx * (0.6 + j * 0.9), 28.6, -10.4), (0, -1, -0.1), 0.8, 2.0, solid(P, "tooth"), tip=0.8)
    for j, ang in enumerate((-25, 0, 25)):                                           # three blade ears
        a = math.radians(ang)
        spike(m, hd, (2.0 * math.sin(a), 32.6, -4.0), (math.sin(a) * 0.5, 1, 0.4), 2.2, 14.0 - abs(j - 1) * 2.0, FUR, tip=0.8)
        spike(m, hd, (2.0 * math.sin(a) + 6.0 * math.sin(a), 32.6 + 12.0, 1.2), (math.sin(a) * 0.5, 1, 0.4), 1.4, 4.0,
              BLADE, tip=0.8)
    for i in range(5):                                                               # back fur blades
        ang = math.radians(-60 + i * 30)
        spike(m, bd, (6.0 * math.sin(ang), 26.0, 6.0), (math.sin(ang) * 0.8, 0.8, 0.8), 2.4, 12.0, BLADE, tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # gauntlets + claws
        ab = m.bone(nm, bd, (sx * 8.0, 26.0, -2.0))
        rod(m, ab, (sx * 8.0, 26.0, -2.0), (sx * 12.0, 18.0, -6.0), 3, FUR, extend=0.6)
        m.round_box(ab, sx * 12.6, -6.6, 3.0, 3.0, 12.0, 19.0, ARM, cut=1)
        for j in range(3):
            spike(m, ab, (sx * 12.6 + (j - 1) * 1.6, 12.0, -7.0), (sx * 0.3, -1, -0.6), 1.2, 6.0, solid(P, "black"), tip=0.8)
        spike(m, ab, (sx * 13.0, 18.0, -4.0), (sx, 0.4, 0.6), 1.6, 8.0, BLADE, tip=0.8)
        for t in range(6):                                                           # blue wind swirl
            a0, a1 = t * 0.9, (t + 1) * 0.9
            rod(m, ab, (sx * 12.6 + 6.0 * math.cos(a0), 12.0 + t * 1.2, -6.6 + 6.0 * math.sin(a0)),
                (sx * 12.6 + 6.0 * math.cos(a1), 12.0 + (t + 1) * 1.2, -6.6 + 6.0 * math.sin(a1)), 1, solid(P, "wind", glow=True),
                extend=0.2, t2=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.6, 12.0, 0))
        rod(m, lg, (sx * 4.6, 14.0, 0), (sx * 5.0, 4.0, 2.0), 3, FUR, extend=0.6)
        m.round_box(lg, sx * 5.0, -1.0, 2.6, 4.0, 0.0, 4.0, FUR, cut=1)
        for j in range(3):
            spike(m, lg, (sx * 5.0 + (j - 1) * 1.4, 0.8, -4.6), (0, -0.2, -1), 1.0, 2.6, solid(P, "black"), tip=0.8)
    return m
