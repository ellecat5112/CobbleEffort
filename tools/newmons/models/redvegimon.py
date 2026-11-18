"""Red Vegimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a red pepper of a plant demon: a fat glossy red bulb with a wide fanged grin, a violet tongue and
slit yellow eyes, a long pointed nose, a crown of green leafy spikes, and two long curling vine arms sprouting from a
cluster of spiky green-and-yellow seed pods. 15 blocks.

Front is -z, y is up. 36 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "a fat glossy red pepper plant demon with a wide fanged grin, slit yellow eyes, a leafy green crown and curling vine arms"
BASE = {"red": (220, 50, 40), "red_dark": (140, 20, 14), "red_light": (250, 130, 110), "green": (80, 170, 60),
        "green_dark": (30, 100, 30), "yellow": (240, 200, 60), "eye": (250, 220, 60), "black": (24, 20, 20),
        "mouth": (90, 20, 50), "tongue": (140, 80, 190), "tooth": (250, 250, 240)}
SHINY = {"red": (240, 190, 50), "red_dark": (170, 120, 10), "red_light": (255, 230, 140)}


def P(v):
    return pal(BASE, SHINY, v)


RED = skin(P, "red", dark="red_dark", light="red_light", var=0.03)


def bulbf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 2.6) < 1.4 and abs(y - 25.0 - (x * sx - 2.6) * 0.4) < 0.4:
                return tone(p["eye"], face), None
        if 15.0 < y < 21.0 and abs(x) < 6.0 - (21.0 - y) * 0.4:
            if y > 19.6 or y < 15.8:
                return tone(p["tooth"], face), None
            return tone(p["mouth"], face), None
    return RED(x, y, z, face, variant, box=box, **k)


def podf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["yellow"] if (x + z) > 2.0 else p["green"], face), None


def build():
    m = Model("redvegimon")
    top = m.bone("redvegimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    for c in ((-3.0, 4.0, 0), (3.0, 4.0, 0), (0, 4.0, 3.0)):                             # spiky seed pods
        ball(m, bd, c, 3.6, podf, layers=3)
        for j in range(4):
            ang = 2 * math.pi * j / 4
            spike(m, bd, (c[0] + 3.0 * math.cos(ang), c[1] + 1.0, c[2] + 3.0 * math.sin(ang)),
                  (math.cos(ang), 0.4, math.sin(ang)), 0.9, 1.8, solid(P, "green"), tip=0.8)
    hd = m.bone("head", bd, (0, 18, 0))
    ball(m, hd, (0, 20.0, 0), 9.0, bulbf, layers=7, ry=10.0)                                # red bulb
    spike(m, hd, (0, 23.0, -8.4), (0, -0.2, -1), 2.2, 7.0, RED, tip=0.8)                    # long nose
    rod(m, hd, (1.0, 16.0, -8.0), (2.4, 12.0, -10.0), 2, solid(P, "tongue"), extend=0.2, t2=1)
    for j in range(9):                                                                   # leafy crown
        ang = math.radians(-80 + j * 20)
        spike(m, hd, (3.0 * math.sin(ang), 29.0, 1.0 + math.cos(ang)), (math.sin(ang), 1, 0.4 * math.cos(ang)), 1.6,
              6.0, skin(P, "green", dark="green_dark"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                  # curling vine arms
        ab = m.bone(nm, bd, (sx * 4.0, 6.0, 0))
        pts = [(sx * 4.0, 6.0, 0), (sx * 11.0, 6.0, -2.0), (sx * 14.0, 12.0, -3.0), (sx * 12.0, 16.0, -3.0),
               (sx * 9.0, 14.0, -3.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 2, RED, extend=0.3)
    return m
