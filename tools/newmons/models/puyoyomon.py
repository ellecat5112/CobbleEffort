"""Puyoyomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a bigger translucent blue jelly with pink spots, two big pink-and-blue eyes, two little round
ears and a ring of stubby tentacle feet. 0.5 blocks.

Front is -z, y is up. 16 units tall; Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.5, HEIGHT, 1.8)
KIND = "floater"
K = 4
LOOK = "a translucent blue jelly with pink spots, two big pink-and-blue eyes, little round ears and stubby tentacle feet"
BASE = {"jelly": (150, 200, 250, 210), "jelly_dark": (100, 150, 220, 210), "spot": (240, 120, 210), "iris": (80, 60, 160),
        "pink": (240, 100, 160), "pupil": (20, 20, 30), "white": (255, 255, 255)}
SHINY = {"jelly": (180, 240, 190, 210), "jelly_dark": (120, 200, 140, 210)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.2, (y - 8.4) * 0.85)
            if math.hypot(x - sx * 2.2 + 0.4, y - 9.0) < 0.35:
                return tone(p["white"], face), None
            if d < 0.6:
                return tone(p["pupil"], face), None
            if d < 1.4:
                return tone(p["iris"] if y > 8.0 else p["pink"], face), None
    if math.sin(x * 1.3 + 1.0) * math.sin(y * 1.1) * math.cos(z * 0.9) > 0.6:
        return tone(p["spot"], face), None
    c = p["jelly_dark"] if face == "down" or y < 5.0 else p["jelly"]
    return tone(c[:3], face) + (c[3],), None


def build():
    m = Model("puyoyomon")
    top = m.bone("puyoyomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    ball(m, bd, (0, 8.0, 0), 5.2, bodyf, layers=4, ry=4.6)
    for sx in (-1, 1):
        ball(m, bd, (sx * 3.6, 12.6, 0), 1.2, bodyf, layers=1)
    for i in range(8):
        ang = 2 * math.pi * i / 8
        spike(m, bd, (3.4 * math.cos(ang), 3.8, 3.4 * math.sin(ang)), (0.1 * math.cos(ang), -1, 0.1 * math.sin(ang)),
              1.6, 3.0, bodyf, tip=0.8)
    return m
