"""Sephirothmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the living Tree of Life: ten glossy green spheres, each with a single red-ringed eye,
arranged in the Sephirot's pattern and joined by golden paths, a grinning red-lipped mouth in the crown sphere and a
glowing star at the heart. 25 blocks.

Front is -z, y is up. 48 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _digi import sized
from _digibeast import ball
from _digidetail import metal, skin, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "the living Tree of Life: ten glossy green spheres each with one red-ringed eye, joined by golden paths, a red-lipped grin at the crown"
BASE = {"green": (80, 200, 90), "green_dark": (30, 120, 40), "green_light": (180, 250, 170), "gold": (230, 190, 70),
        "gold_dark": (150, 100, 20), "red": (200, 30, 40), "white": (250, 250, 250), "black": (24, 20, 20),
        "star": (255, 250, 200)}
SHINY = {"green": (180, 80, 200), "green_dark": (100, 30, 120), "green_light": (230, 180, 250)}


def P(v):
    return pal(BASE, SHINY, v)


NODES = [(0, 44.0), (-6.0, 38.0), (6.0, 38.0), (-6.0, 28.0), (6.0, 28.0), (0, 32.0), (-6.0, 18.0), (6.0, 18.0),
         (0, 20.0), (0, 10.0)]
PATHS = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (1, 5), (2, 5), (3, 4), (3, 5), (4, 5), (3, 6), (4, 7), (5, 8),
         (6, 7), (6, 8), (7, 8), (8, 9), (6, 9), (7, 9)]


def spheref_for(cx, cy, mouth=False):
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            if mouth and abs(y - cy) < 1.2 and abs(x - cx) < 2.0:
                return tone(p["red"] if abs(y - cy) > 0.4 else p["white"], face), None
            d = math.hypot(x - cx, y - cy)
            if not mouth:
                if d < 0.6:
                    return tone(p["black"], face), None
                if d < 1.4:
                    return tone(p["red"], face), None
                if d < 1.8:
                    return tone(p["white"], face), None
        return skin(P, "green", dark="green_dark", light="green_light", var=0.02)(x, y, z, face, variant, box=box, **k)
    return s


def build():
    m = Model("sephirothmon")
    top = m.bone("sephirothmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 24, 0))
    for a_, b_ in PATHS:                                                                 # golden paths
        rod(m, bd, (NODES[a_][0], NODES[a_][1], 0.6), (NODES[b_][0], NODES[b_][1], 0.6), 1,
            metal(P, "gold", dark="gold_dark"), extend=0.0)
    for i, (cx, cy) in enumerate(NODES):                                                 # ten spheres
        ball(m, bd, (cx, cy, 0), 3.4, spheref_for(cx, cy, mouth=(i == 0)), layers=3)
    ball(m, bd, (0, 32.0, -3.0), 1.0, solid(P, "star", glow=True), layers=1)
    return m
