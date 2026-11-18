"""Pipimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a round green fruit-like creature with a crown of dark green leaves, big shiny black eyes, a happy
pink mouth, rosy cheeks and two stubby feet. 0.35 blocks tall.

Front is -z, y is up. 16 units tall; Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.35, HEIGHT, 1.4)
KIND = "floater"
K = 3
LOOK = "a round green fruit-like creature with a crown of dark leaves, big shiny black eyes, a happy pink mouth and rosy cheeks"
BASE = {"green": (150, 210, 90), "green_dark": (90, 150, 40), "leaf": (60, 140, 50), "black": (20, 20, 20),
        "white": (250, 250, 250), "pink": (240, 120, 150), "cheek": (250, 190, 200)}
SHINY = {"green": (240, 200, 90), "green_dark": (190, 140, 40), "leaf": (180, 90, 40)}


def P(v):
    return pal(BASE, SHINY, v)


def build():
    m = Model("pipimon")
    top = m.bone("pipimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 6.6, 0), 5.6, skin(P, "green", dark="green_dark", var=0.02), layers=5, ry=5.4)
    for sx in (-1, 1):
        ball(m, bd, (sx * 1.8, 7.6, -4.8), 1.1, solid(P, "black"), layers=2, squash=0.5)
        m.box(bd, sx * 1.8 - 0.5, 8.0, -5.4, sx * 1.8 - 0.1, 8.4, -5.3, solid(P, "white"))
        m.box(bd, sx * 3.4 - 0.6, 6.0, -5.0, sx * 3.4 + 0.6, 6.6, -4.8, solid(P, "cheek"))
        m.round_box(top, sx * 2.6, -0.6, 1.6, 1.8, 0.0, 1.4, skin(P, "green", dark="green_dark"), cut=0)
    m.round_box(bd, 0, -5.2, 1.2, 0.4, 5.0, 6.0, solid(P, "pink"), cut=0)
    for i in range(7):                                                                   # crown of leaves
        ang = 2 * math.pi * i / 7
        spike(m, bd, (1.2 * math.cos(ang), 12.0, 1.2 * math.sin(ang)), (math.cos(ang), 0.6, math.sin(ang)), 1.6, 3.4,
              solid(P, "leaf"), tip=0.8)
    return m
