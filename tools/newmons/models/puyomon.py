"""Puyomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a translucent pale-blue jellyfish of a baby: a round glassy bell with one big pink-ringed eye, two
tiny round ears and a fringe of stubby tentacle feet. 0.35 blocks.

Front is -z, y is up. 14 units tall; Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _route import pal, tone

HEIGHT = 14
SCALE, HITBOX = sized(0.35, HEIGHT, 1.4)
KIND = "floater"
K = 4
LOOK = "a translucent pale-blue jellyfish baby with one big pink-ringed eye, two tiny round ears and stubby tentacle feet"
BASE = {"jelly": (200, 226, 250, 210), "jelly_dark": (150, 190, 230, 210), "ring": (230, 110, 200), "iris": (60, 70, 120),
        "pupil": (20, 20, 30), "white": (255, 255, 255), "ear": (240, 180, 230)}
SHINY = {"jelly": (250, 220, 200, 210), "jelly_dark": (230, 180, 150, 210)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        d = math.hypot(x, y - 8.0)
        if math.hypot(x + 0.6, y - 8.6) < 0.4:
            return tone(p["white"], face), None
        if d < 0.8:
            return tone(p["pupil"], face), None
        if d < 1.6:
            return tone(p["iris"], face), None
        if d < 2.2:
            return tone(p["ring"], face), None
    c = p["jelly_dark"] if face == "down" or y < 5.0 else p["jelly"]
    return tone(c[:3], face) + (c[3],), None


def build():
    m = Model("puyomon")
    top = m.bone("puyomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    ball(m, bd, (0, 8.0, 0), 4.4, bodyf, layers=4)
    for sx in (-1, 1):
        ball(m, bd, (sx * 3.0, 12.0, 0), 0.9, bodyf, layers=1)
    for i in range(6):
        ang = 2 * math.pi * i / 6
        spike(m, bd, (2.6 * math.cos(ang), 4.0, 2.6 * math.sin(ang)), (0.2 * math.cos(ang), -1, 0.2 * math.sin(ang)),
              1.6, 3.4, bodyf, tip=0.8)
    return m
