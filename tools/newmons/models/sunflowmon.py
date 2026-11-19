"""Sunflowmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a sunflower spirit: a round cream face with a pink forehead mark and a grumpy look, ringed by
bright yellow petals, two great green leaf-wings, a slender green body that splits into long leaf-blade legs and a
curling root tail. 15 blocks.

Front is -z, y is up. 48 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a sunflower spirit with a grumpy cream face ringed by yellow petals, two great green leaf-wings and long leaf-blade legs"
BASE = {"cream": (252, 240, 210), "pink": (240, 160, 180), "yellow": (250, 210, 50), "yellow_dark": (210, 150, 20),
        "green": (110, 190, 70), "green_dark": (50, 120, 30), "black": (30, 26, 24)}
SHINY = {"yellow": (250, 140, 60), "yellow_dark": (200, 80, 20), "green": (60, 160, 160), "green_dark": (20, 100, 100)}


def P(v):
    return pal(BASE, SHINY, v)


GREEN = skin(P, "green", dark="green_dark")


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if abs(x) < 1.6 and 40.0 < y < 42.0:
            return tone(p["pink"], face), None
        for sx in (-1, 1):
            if math.hypot(x - sx * 1.6, y - 38.4) < 0.5:
                return tone(p["black"], face), None
        if abs(y - 36.0) < 0.15 and abs(x) < 0.8:
            return tone(p["black"], face), None
    return tone(p["cream"], face), None


def build():
    m = Model("sunflowmon")
    top = m.bone("sunflowmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    rod(m, bd, (0, 32.0, 0), (0, 18.0, 0), 3, GREEN, extend=0.4)                             # slender body
    for sx in (-1, 1):                                                                   # leaf-blade legs
        spike(m, bd, (sx * 1.6, 18.0, 0), (sx * 0.3, -1, 0.1), 2.4, 14.0, GREEN, tip=0.8)
    pts = [(0, 18.0, 1.0), (4.0, 8.0, 3.0), (8.0, 4.0, 2.0), (9.0, 6.0, 0.0)]               # root tail
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, bd, p0, p1, 1, GREEN, extend=0.2, t2=1)
    hd = m.bone("head", bd, (0, 38, 0))
    ball(m, hd, (0, 38.0, -0.4), 4.0, facef, layers=3, squash=0.5)
    for j in range(14):                                                                  # yellow petals
        ang = 2 * math.pi * j / 14
        spike(m, hd, (4.0 * math.cos(ang), 38.0 + 4.0 * math.sin(ang), 0.4), (math.cos(ang), math.sin(ang), 0), 2.0, 3.6,
              skin(P, "yellow", dark="yellow_dark"), tip=0.8)
    for sx in (-1, 1):                                                                   # great leaf-wings
        m.box(bd, min(sx * 2.0, sx * 18.0), 28.0, 1.0, max(sx * 2.0, sx * 18.0), 36.0, 1.0, GREEN,
              rotation=(0, -sx * 15, sx * 15), pivot=(sx * 2.0, 32.0, 1.0))
    return m
