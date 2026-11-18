"""Poyomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a translucent pale-blue jellyfish-like ghost of a blob with a round dome top, two black dot eyes,
a little pink smile and a scalloped hem. 0.35 blocks.

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
LOOK = "a translucent pale-blue ghostly blob with a dome top, two black dot eyes, a pink smile and a scalloped hem"
BASE = {"white": (240, 248, 255, 220), "blue": (170, 210, 245, 220), "black": (20, 20, 24), "pink": (240, 110, 110)}
SHINY = {"white": (255, 244, 230, 220), "blue": (250, 200, 160, 220)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 2.0, y - 8.6) < 0.8:
                return tone(p["black"], face), None
        if abs(y - 6.6) < 0.4 and abs(x) < 1.0:
            return tone(p["pink"], face), None
    c = p["blue"] if y < 4.0 or face == "down" else p["white"]
    return tone(c[:3], face) + (c[3],), None


def build():
    m = Model("poyomon")
    top = m.bone("poyomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 8.0, 0), 4.8, bodyf, layers=4, ry=4.0)
    m.round_box(bd, 0, 0, 4.8, 4.4, 2.6, 8.0, bodyf, cut=1)
    for i in range(8):
        ang = 2 * math.pi * i / 8
        spike(m, bd, (4.2 * math.cos(ang), 2.8, 3.8 * math.sin(ang)), (0, -1, 0), 1.6, 1.6, bodyf, tip=0.8)
    return m
