"""Mori Shellmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the forest shell-dweller: a grey-green slug-like creature with a wide gaping pink-lined
mouth, one yellow eye and a scarred brow, a tangle of green tendril hair, lumpy splayed fingers, and a great teal
mossy shell bristling with horn spikes on its back. 15 blocks long.

Front is -z, y is up. 34 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, skin, solid, strands
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("a grey-green slug-like creature with a wide gaping mouth, one yellow eye, green tendril hair, lumpy fingers and "
        "a great teal mossy shell bristling with horn spikes")
BASE = {"skin": (130, 140, 110), "skin_dark": (70, 80, 56), "shell": (70, 140, 120), "shell_dark": (24, 80, 70),
        "moss": (120, 180, 80), "spot": (220, 220, 140), "mouth": (200, 60, 90), "eye": (240, 220, 40),
        "pupil": (20, 20, 20), "hair": (110, 200, 70), "hair_dark": (40, 120, 30), "tooth": (250, 250, 240)}
SHINY = {"shell": (160, 90, 60), "shell_dark": (90, 40, 20), "skin": (170, 130, 160), "skin_dark": (110, 70, 100)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN0 = skin(P, "skin", dark="skin_dark")
SHELL0 = armour(P, "shell", "shell_dark")


def skinf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face != "down" and math.sin(x * 1.3) * math.sin(y * 1.1 + z * 0.9) > 0.85:
        return tone(p["spot"], face), None
    return SKIN0(x, y, z, face, variant, box=box, **k)


def shellf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "up" or math.sin(x * 0.7) * math.sin(z * 0.6 + y * 0.3) > 0.6:
        return tone(p["moss"], face), None
    return SHELL0(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("morishellmon")
    top = m.bone("morishellmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 7.0, 10.0, 0.0, 6.0, skinf, cut=2)                              # slug foot
    ball(m, bd, (0, 14.0, 4.0), 10.0, shellf, layers=6, ry=10.0, squash=1.0)               # mossy shell
    for i in range(10):                                                                  # horn spikes
        ang = 2 * math.pi * i / 10
        spike(m, bd, (8.0 * math.cos(ang), 18.0 + 4.0 * math.sin(ang * 2), 4.0 + 8.0 * math.sin(ang)),
              (math.cos(ang), 0.8, math.sin(ang)), 2.4, 6.0, shellf, tip=0.8)
    spike(m, bd, (0, 24.0, 4.0), (0, 1, 0), 2.6, 6.0, shellf, tip=0.8)
    hd = m.bone("head", bd, (0, 12, -8))
    m.round_box(hd, 0, -10.0, 4.6, 5.0, 6.0, 15.0, skinf, cut=1)                          # head
    m.round_box(hd, 0, -14.4, 3.6, 0.8, 6.6, 11.0, solid(P, "mouth"), cut=1)              # gaping mouth
    for j in range(4):
        spike(m, hd, (-2.6 + j * 1.7, 11.0, -14.6), (0, -1, 0), 0.8, 1.4, solid(P, "tooth"), tip=0.8)
    ball(m, hd, (1.6, 14.0, -13.6), 1.6, solid(P, "eye"), layers=2)
    m.box(hd, 1.2, 13.4, -15.25, 2.0, 14.6, -15.1, solid(P, "pupil"))
    for i in range(10):                                                                  # green tendril hair
        ang = math.radians(-80 + i * 18)
        spike(m, hd, (3.0 * math.sin(ang), 15.0, -10.0 + math.cos(ang)), (math.sin(ang), 1, 0.3), 1.0, 4.0,
              strands(P, "hair", "hair_dark"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                  # lumpy splayed fingers
        ab = m.bone(nm, bd, (sx * 5.0, 6.0, -6.0))
        rod(m, ab, (sx * 5.0, 6.0, -6.0), (sx * 9.0, 2.0, -10.0), 3, skinf, extend=0.4)
        for f in range(4):
            ang = math.radians(-40 + f * 26)
            rod(m, ab, (sx * 9.0, 1.4, -10.0), (sx * (9.0 + 3.0 * math.sin(ang)), 0.6, -10.0 - 3.0 * math.cos(ang)),
                2, skinf, extend=0.3)
    return m
