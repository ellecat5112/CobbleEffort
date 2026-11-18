"""Popomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a round golden ball of a seed husk, finely streaked like straw, with two big red eyes with
white glints and a bright green leaf sprouting from its back. 0.35 blocks.

Front is -z, y is up. 12 units tall; Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model
from _digi import sized
from _digibeast import ball
from _digidetail import solid
from _route import pal, tone

HEIGHT = 12
SCALE, HITBOX = sized(0.35, HEIGHT, 1.4)
KIND = "floater"
K = 4
LOOK = "a round golden seed-husk ball streaked like straw with big red eyes and a bright green leaf on its back"
BASE = {"gold": (230, 190, 90), "gold_dark": (170, 120, 40), "red": (200, 40, 40), "white": (255, 255, 255),
        "green": (90, 190, 70), "green_dark": (30, 110, 30)}
SHINY = {"gold": (220, 220, 230), "gold_dark": (150, 150, 170), "green": (220, 90, 140), "green_dark": (140, 30, 80)}


def P(v):
    return pal(BASE, SHINY, v)


def huskf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.9, (y - 5.6) * 0.8)
            if d < 0.45 and x * sx < 1.9:
                return tone(p["white"], face), None
            if d < 1.4:
                return tone(p["red"], face), None
    streak = abs(math.sin(x * 3.1 + z * 2.3 + y * 0.3))
    return tone(p["gold_dark"] if streak > 0.9 else p["gold"], face), None


def leaff(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["green_dark"] if abs(x) < 0.3 else p["green"], face), None


def build():
    m = Model("popomon")
    top = m.bone("popomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 5.0, 0), 4.6, huskf, layers=4, ry=4.2, squash=0.85)
    m.box(bd, -2.4, 6.0, 4.0, 2.4, 11.0, 4.0, leaff, rotation=(-35, 0, 0), pivot=(0, 6.0, 3.6))
    return m
