"""Puroromon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a round orange bee-grub with big glossy green eyes, a squiggly mouth, two violet antennae, little
stubby arms and feet, and two pairs of big lilac wings. 0.5 blocks.

Front is -z, y is up. 18 units tall; Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.5, HEIGHT, 1.8)
KIND = "floater"
K = 3
LOOK = "a round orange bee-grub with big green eyes, two violet antennae, stubby limbs and two pairs of lilac wings"
BASE = {"orange": (250, 170, 40), "orange_dark": (210, 120, 20), "eye": (40, 140, 60), "pupil": (14, 30, 20),
        "white": (255, 255, 255), "violet": (80, 60, 160), "wing": (160, 160, 210, 210), "black": (40, 30, 20)}
SHINY = {"orange": (240, 120, 160), "orange_dark": (190, 70, 110)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "orange", dark="orange_dark", var=0.03)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.8, (y - 10.0) * 0.8)
            if math.hypot(x - sx * 1.8 + 0.4, y - 10.6) < 0.35:
                return tone(p["white"], face), None
            if d < 0.6:
                return tone(p["pupil"], face), None
            if d < 1.4:
                return tone(p["eye"], face), None
        if abs(y - 7.6 - 0.25 * math.sin(x * 4)) < 0.15 and abs(x) < 1.2:
            return tone(p["black"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("puroromon")
    top = m.bone("puroromon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 9.0, 0), 4.0, bodyf, layers=4, ry=3.8)
    ball(m, bd, (0, 4.0, 0.6), 2.6, SKIN, layers=2)
    for sx in (-1, 1):
        rod(m, bd, (sx * 1.0, 12.6, -1.0), (sx * 1.6, 16.0, -2.0), 1, solid(P, "violet"), extend=0.2, t2=1)
        spike(m, bd, (sx * 2.6, 5.0, -1.4), (sx * 0.4, -0.4, -1), 1.0, 1.6, SKIN, tip=0.8)
        spike(m, bd, (sx * 1.4, 1.6, -0.6), (0, -1, -0.3), 1.0, 1.4, SKIN, tip=0.8)
        for j, (ang, ln) in enumerate(((20, 8.0), (-15, 6.0))):
            x0, x1 = sorted((sx * 2.0, sx * (2.0 + ln)))
            m.box(bd, x0, 8.0, 3.0 + j * 0.4, x1, 12.0, 3.0 + j * 0.4, solid(P, "wing"),
                  rotation=(0, -sx * 20, sx * ang), pivot=(sx * 2.0, 10.0, 3.0))
    return m
