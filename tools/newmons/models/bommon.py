"""Bommon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a cat-eared baby bomb. A glossy black ball with two pointed cat ears, three mismatched eyes (yellow,
red and teal) with heavy lids, a blue cap at its back from which a braided fuse trails away, sparking at its tip.
Baby I.

Front is -z, y is up. 22 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import mix, solid
from _route import pal, tone

HEIGHT = 22
SCALE, HITBOX = sized(0.35, HEIGHT, 0.35)
KIND = "floater"
K = 4
LOOK = "a glossy black cat-eared bomb with three mismatched lidded eyes, a blue cap and a sparking braided fuse"
BASE = {"black": (40, 40, 48), "black_light": (130, 132, 150), "blue": (40, 60, 180), "yellow": (240, 210, 60),
        "red": (230, 70, 60), "teal": (60, 200, 190), "white": (250, 250, 250), "pupil": (16, 16, 20),
        "fuse": (150, 120, 80), "spark": (255, 200, 80)}
SHINY = {"black": (236, 236, 244), "black_light": (255, 255, 255), "blue": (220, 60, 140)}


def P(v):
    return pal(BASE, SHINY, v)


EYES = ((-3.4, 11.6, "yellow"), (-2.8, 8.0, "red"), (1.4, 8.6, "teal"))


def ballf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for ex, ey, key in EYES:
            d = math.hypot(x - ex, y - ey)
            if d < 1.6:
                if y - ey > 0.35:                                       # heavy lid over the top half
                    return tone(p["black_light"] if d > 1.3 else p["black"], face), None
                return tone(p["pupil"] if math.hypot(x - ex - 0.2, y - ey) < 0.6 else
                            p[key] if d < 1.3 else p["pupil"], face), None
    g = max(0.0, (y - 8.0) / 8.0 - abs(x + 2.0) / 12.0)
    return tone(mix(p["black"], p["black_light"], min(0.5, g)), face), None


def build():
    m = Model("bommon")
    top = m.bone("bommon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 9, 0))
    ball(m, bd, (0, 9.0, 0), 7.6, ballf, layers=7)
    for sx in (-1, 1):                                                       # cat ears
        spike(m, bd, (sx * 4.0, 14.6, 0), (sx * 0.4, 1, -0.1), 3.0, 3.6, solid(P, "black"), tip=0.8)
    m.round_box(bd, 3.6, 4.6, 2.4, 2.4, 2.6, 6.4, solid(P, "blue"), cut=1)  # the cap at its back
    pts = [(3.6, 3.0, 5.4), (4.6, 0.6, 7.0), (6.0, -1.0, 8.4), (7.0, -1.4, 10.4)]
    for a, b in zip(pts, pts[1:]):
        rod(m, bd, a, b, 1, solid(P, "fuse"), extend=0.3)
    for i in range(6):
        ang = math.radians(i * 60)
        spike(m, bd, pts[-1], (math.cos(ang), math.sin(ang), 0.6), 0.8, 2.4, solid(P, "spark", glow=True))
    return m
