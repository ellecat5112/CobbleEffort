"""Starmons (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a big golden star with a grumpy black-and-gold face leading two rows of little spiked silver stars
lined up beside it like a chain of hench-stars. 1 block. Child stage.

Front is -z, y is up. 20 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, solid
from _route import pal, tone

HEIGHT = 20
SCALE, HITBOX = sized(1, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "a big grumpy golden star leading two rows of little spiked silver stars lined up beside it"
BASE = {"gold": (250, 220, 50), "gold_dark": (190, 150, 10), "black": (30, 26, 24), "silver": (200, 204, 216),
        "silver_dark": (90, 94, 108)}
SHINY = {"gold": (220, 120, 220), "gold_dark": (150, 50, 150)}


def P(v):
    return pal(BASE, SHINY, v)


def starf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and x < 0 and abs(x) < 3.0 and 7.0 < y < 13.0:
        return tone(p["black"], face), None
    return metal(P, "gold", dark="gold_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("starmons")
    top = m.bone("starmons", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 10.0, 0), 3.6, starf, layers=3, squash=0.6)
    for j in range(5):
        ang = math.radians(90 + j * 72)
        spike(m, bd, (0, 10.0, 0), (math.cos(ang), math.sin(ang), 0), 3.4, 7.0, starf, tip=0.8)
    for sx in (-1, 1):                                                                   # rows of little stars
        for j in range(4):
            c = (sx * (9.0 + j * 3.4), 8.0 - j * 0.4, 0.6 * j)
            ball(m, bd, c, 1.4, metal(P, "silver", dark="silver_dark"), layers=2)
            for k in range(5):
                a2 = math.radians(90 + k * 72)
                spike(m, bd, c, (math.cos(a2), math.sin(a2), 0), 0.9, 1.6, metal(P, "silver", dark="silver_dark"),
                      tip=0.8)
    return m
