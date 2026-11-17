"""Chicchimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little yellow chick. A round yellow ball of a bird with little wings, big eyes, a tiny orange beak,
red flame-like brows and one huge looping red crest feather sweeping up and back. Baby II.

Front is -z, y is up. 26 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, feathers, skin, solid, strands
from _route import pal, tone

HEIGHT = 26
SCALE, HITBOX = sized(0.5, HEIGHT, 0.55)
KIND = "floater"
K = 4
LOOK = "a round yellow chick with little wings, big eyes, a tiny beak, red brows and a huge looping red crest feather"
BASE = {"yellow": (250, 220, 40), "yellow_dark": (210, 160, 10), "yellow_light": (255, 245, 150), "red": (220, 40, 40),
        "red_dark": (140, 14, 20), "beak": (240, 150, 40), "eye": (110, 70, 140), "pupil": (20, 10, 30),
        "white": (255, 255, 255)}
SHINY = {"yellow": (180, 230, 250), "yellow_dark": (110, 170, 220), "yellow_light": (230, 250, 255),
         "red": (60, 100, 230), "red_dark": (20, 50, 150)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            c = eye(p, x - sx * 2.6, y - 9.4, 1.4, "eye")
            if c is not None:
                return c, None
            if abs(y - 11.6 - (x * sx - 2.0) * 0.5) < 0.4 and 1.0 < x * sx < 4.0:
                return tone(p["red"], face), None                                   # flame brows
    return skin(P, "yellow", dark="yellow_dark", light="yellow_light", var=0.03)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("chicchimon")
    top = m.bone("chicchimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 8.0, 0), 6.6, bodyf, layers=6)
    spike(m, bd, (0, 7.6, -6.4), (0, -0.2, -1), 1.6, 1.8, solid(P, "beak"), tip=0.4)
    for sx in (-1, 1):                                                             # little wings
        ab = m.bone("arm_left" if sx > 0 else "arm_right", bd, (sx * 6.0, 8.0, 0))
        m.box(ab, min(sx * 5.6, sx * 11.0), 6.0, -1.6, max(sx * 5.6, sx * 11.0), 10.0, 1.6,
              feathers(P, "yellow", "yellow_dark", size=(1.0, 1.6)), rotation=(0, 0, sx * 20),
              pivot=(sx * 5.6, 8.0, 0))
    hd = m.bone("head", bd, (0, 14, 0))                                            # the looping crest feather
    pts = [(0, 14.0, -1.0), (0, 20.0, -2.0), (0, 24.0, 2.0), (0, 22.0, 7.0), (1.0, 16.0, 9.0), (2.0, 11.0, 9.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, hd, p0, p1, 2 if j < 3 else 1, strands(P, "red", "red_dark"), extend=0.4, t2=3)
    return m
