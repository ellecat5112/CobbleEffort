"""Shooting Starmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a blazing comet of a star: a round black-and-gold armoured star body bristling with long
silver blade-rays swept back like a comet's tail, a golden lightning-bolt crest, a red V-visor and a glowing green eye.
15 blocks. Adult stage.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a blazing comet star of black-and-gold armour bristling with silver blade-rays swept back, a golden bolt crest and a red V-visor"
BASE = {"gold": (250, 210, 60), "gold_dark": (170, 120, 20), "black": (30, 30, 36), "black_dark": (10, 10, 12),
        "silver": (210, 214, 226), "silver_dark": (110, 114, 130), "red": (210, 40, 40), "green": (90, 240, 120),
        "trail": (255, 240, 180, 150)}
SHINY = {"gold": (200, 210, 230), "gold_dark": (120, 130, 160), "red": (60, 120, 230)}


def P(v):
    return pal(BASE, SHINY, v)


def build():
    m = Model("shootingstarmon")
    top = m.bone("shootingstarmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    ball(m, bd, (0, 14.0, 0), 6.0, armour(P, "black", "black_dark", trim="gold", trim_w=0.3), layers=5)
    for j in range(12):                                                                  # swept silver blade-rays
        ang = 2 * math.pi * j / 12
        d = (math.cos(ang) * 0.6, math.sin(ang) * 0.6, 1.0)
        spike(m, bd, (5.0 * math.cos(ang), 14.0 + 5.0 * math.sin(ang), 2.0), d, 2.0, 12.0 + (j % 3) * 3.0,
              metal(P, "silver", dark="silver_dark"), tip=0.8)
    for j in range(5):                                                                   # golden star points in front
        ang = math.radians(90 + j * 72)
        spike(m, bd, (0, 14.0, -4.0), (math.cos(ang), math.sin(ang), -0.3), 2.4, 8.0, armour(P, "gold", "gold_dark"),
              tip=0.8)
    for sx in (-1, 1):
        m.box(bd, min(sx * 0.4, sx * 4.0), 15.0, -6.3, max(sx * 0.4, sx * 4.0), 16.0, -6.0, solid(P, "red"),
              rotation=(0, 0, sx * 30), pivot=(0, 13.0, -6.1))
    m.box(bd, 1.4, 16.0, -6.4, 2.6, 17.2, -6.2, solid(P, "green", glow=True))
    m.box(bd, -0.6, 20.0, -2.0, 0.6, 26.0, -1.0, solid(P, "gold"), rotation=(0, 0, 20), pivot=(0, 20.0, -1.5))
    m.box(bd, -0.6, 24.0, -2.0, 0.6, 30.0, -1.0, solid(P, "gold"), rotation=(0, 0, -25), pivot=(0, 24.0, -1.5))
    return m
