"""Pillomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a sleepy pillow-sheep: a plump pink pillow of a body with a cream face, closed sleepy eyes, a ruff
of pink wool puffs round its edge, a golden curled ram's horn, a little purple nightcap with a bobble, and four tiny
cream hooves. 1 block tall.

Front is -z, y is up. 24 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, metal, skin, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(1, HEIGHT, 2.0)
KIND = "floater"
K = 3
LOOK = "a plump pink pillow-sheep with a cream face, sleepy closed eyes, pink wool puffs, a golden ram's horn and a nightcap"
BASE = {"pink": (240, 120, 130), "pink_dark": (180, 70, 80), "wool": (250, 200, 210), "cream": (250, 240, 210),
        "cream_dark": (210, 196, 160), "gold": (220, 180, 60), "purple": (130, 100, 190), "black": (40, 30, 30),
        "teal": (100, 200, 200)}
SHINY = {"pink": (130, 170, 240), "pink_dark": (70, 110, 190), "wool": (200, 220, 250)}


def P(v):
    return pal(BASE, SHINY, v)


def build():
    m = Model("pillomon")
    top = m.bone("pillomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 7.0, 5.0, 4.0, 18.0, fabric(P, "pink", "pink_dark"), cut=3)       # pillow body
    m.round_box(bd, -1.6, -4.0, 4.0, 1.6, 6.0, 16.0, skin(P, "cream", dark="cream_dark"), cut=1)   # cream face
    for sx in (-1, 1):
        m.box(bd, -1.6 + sx * 1.8 - 0.8, 12.0, -5.75, -1.6 + sx * 1.8 + 0.8, 12.4, -5.6, solid(P, "black"))
    for i in range(14):                                                                  # wool puffs round the edge
        ang = 2 * math.pi * i / 14
        ball(m, bd, (7.0 * math.cos(ang), 11.0 + 7.0 * math.sin(ang), 0), 1.6, solid(P, "wool"), layers=2)
    for j in range(5):                                                                   # golden ram's horn
        ang = j * 1.2
        ball(m, bd, (4.0 + 1.6 * math.cos(ang), 15.0 + 1.6 * math.sin(ang), -3.6 + j * 0.3), 1.2, metal(P, "gold"),
             layers=1)
    m.round_box(bd, 1.0, 0, 3.0, 3.0, 18.0, 19.4, fabric(P, "purple", "black"), cut=1)     # nightcap
    spike(m, bd, (1.0, 19.4, 0), (-0.6, 1, 0), 2.6, 4.0, fabric(P, "purple", "black"), tip=0.8)
    ball(m, bd, (-2.0, 23.0, 0), 0.9, solid(P, "teal"), layers=1)
    for sx in (-1, 1):
        for sz in (-1, 1):
            spike(m, bd, (sx * 4.0, 4.0, sz * 2.4), (0, -1, 0), 1.4, 2.4, solid(P, "cream"), tip=0.8)
    return m
