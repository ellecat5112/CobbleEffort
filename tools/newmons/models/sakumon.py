"""Sakumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a glossy golden droplet of a baby with one tall black-edged blade horn, big brown eyes and a tiny
frown. 0.35 blocks.

Front is -z, y is up. 16 units tall; Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, skin, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.35, HEIGHT, 1.6)
KIND = "floater"
K = 4
LOOK = "a glossy golden droplet baby with one tall black-edged blade horn, big brown eyes and a tiny frown"
BASE = {"gold": (250, 220, 70), "gold_dark": (200, 150, 20), "gold_light": (255, 245, 180), "black": (30, 26, 20),
        "eye": (110, 70, 40), "white": (255, 255, 255)}
SHINY = {"gold": (200, 210, 230), "gold_dark": (130, 140, 170), "gold_light": (240, 246, 255)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.8, (y - 5.2) * 0.8)
            if math.hypot(x - sx * 1.8 + 0.3, y - 5.6) < 0.3:
                return tone(p["white"], face), None
            if d < 1.0:
                return tone(p["eye"] if d < 0.8 else p["black"], face), None
        if abs(y - 3.4) < 0.15 and abs(x) < 0.6:
            return tone(p["black"], face), None
    return skin(P, "gold", dark="gold_dark", light="gold_light", var=0.02)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("sakumon")
    top = m.bone("sakumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    ball(m, bd, (0, 4.6, 0), 4.6, bodyf, layers=4, ry=3.8)
    m.box(bd, -0.6, 8.0, -1.6, 0.6, 15.6, 1.6, metal(P, "gold", dark="black"))               # blade horn
    spike(m, bd, (0, 15.6, 0), (0, 1, 0), 1.2, 1.6, metal(P, "gold", dark="black"), tip=0.8)
    return m
