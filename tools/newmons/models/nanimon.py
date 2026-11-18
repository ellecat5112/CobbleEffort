"""Nanimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a bad-tempered brawler: a round tan body covered in black stubble and stitches, a big round face
hidden behind dark sunglasses with a shouting red mouth, a shock of spiky black hair, a huge red-gloved fist thrown
forward and a smaller one held back, and stubby legs in blue-and-red striped boots with yellow stars. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a round tan stubbly brawler with dark sunglasses, a shouting mouth, spiky black hair, huge red boxing gloves and "
        "striped boots with stars")
BASE = {"tan": (230, 180, 140), "tan_dark": (170, 120, 90), "black": (30, 28, 32), "red": (210, 40, 40),
        "red_dark": (130, 14, 14), "blue": (50, 70, 170), "yellow": (250, 210, 50), "mouth": (150, 30, 40),
        "glass": (60, 70, 80)}
SHINY = {"tan": (150, 200, 150), "tan_dark": (90, 140, 90), "red": (60, 120, 220), "red_dark": (20, 60, 140)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN0 = skin(P, "tan", dark="tan_dark")


def skinf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face != "down" and math.sin(x * 2.3 + z * 1.7) * math.sin(y * 2.1) > 0.82:
        return tone(p["black"], face), None                                              # stubble
    return SKIN0(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("nanimon")
    top = m.bone("nanimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 18.0, 0), 9.0, skinf, layers=6, ry=9.6, squash=0.9)                    # round body-face
    m.box(bd, -6.0, 21.0, -8.6, 6.0, 23.4, -8.0, solid(P, "glass"))                       # dark sunglasses
    m.box(bd, -6.4, 22.4, -8.2, 6.4, 23.0, -7.0, solid(P, "black"))
    m.round_box(bd, 0, -8.0, 3.0, 0.8, 14.0, 18.0, solid(P, "mouth"), cut=1)              # shouting mouth
    for i in range(10):                                                                  # spiky black hair
        ang = math.radians(-90 + i * 20)
        spike(m, bd, (6.0 * math.sin(ang), 26.0, 1.0 + 2.0 * math.cos(ang)), (math.sin(ang) * 0.7, 1, 0.3), 2.0, 5.0,
              solid(P, "black"), tip=0.8)
    al = m.bone("arm_left", bd, (8.0, 18.0, 0))                                          # huge fist thrown forward
    rod(m, al, (8.0, 18.0, 0), (12.0, 22.0, -6.0), 3, skinf, extend=0.4)
    ball(m, al, (13.0, 24.0, -10.0), 5.0, skin(P, "red", dark="red_dark"), layers=4)
    ar = m.bone("arm_right", bd, (-8.0, 16.0, 0))
    rod(m, ar, (-8.0, 16.0, 0), (-11.0, 12.0, -2.0), 3, skinf, extend=0.4)
    ball(m, ar, (-12.0, 10.0, -3.0), 3.0, skin(P, "red", dark="red_dark"), layers=3)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.6, 8.0, 0))
        rod(m, lg, (sx * 3.6, 9.0, 0), (sx * 4.0, 4.0, 0), 3, skinf, extend=0.3)
        m.round_box(lg, sx * 4.0, -0.6, 2.4, 3.2, 0.0, 5.0, skin(P, "blue", dark="black"), cut=1)
        m.box(lg, sx * 4.0 - 1.0, 2.0, -3.9, sx * 4.0 + 1.0, 3.6, -3.7, solid(P, "yellow"))
    return m
