"""Relemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a round golden-yellow blob with a happy closed-eye smile and a little cat mouth, and a big plump fox
tail tipped white curling up behind it. 0.35 blocks.

Front is -z, y is up. 12 units tall; Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 12
SCALE, HITBOX = sized(0.35, HEIGHT, 1.8)
KIND = "floater"
K = 4
LOOK = "a round golden-yellow blob with a happy closed-eye smile and a big plump white-tipped fox tail"
BASE = {"yellow": (250, 200, 50), "yellow_dark": (210, 140, 20), "yellow_light": (255, 236, 150), "white": (252, 250, 244),
        "black": (40, 30, 20)}
SHINY = {"yellow": (240, 160, 200), "yellow_dark": (190, 100, 150), "yellow_light": (255, 210, 230)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "yellow", dark="yellow_dark", light="yellow_light", var=0.02)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(math.hypot(x - sx * 2.2, y - 4.4) - 0.9) < 0.18 and y > 4.4:
                return tone(p["black"], face), None
        if abs(y - 2.8) < 0.18 and abs(x) < 0.8 and abs(abs(x) - 0.4) < 0.3:
            return tone(p["black"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def tailf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if y > 9.0:
        return tone(p["white"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("relemon")
    top = m.bone("relemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 4.0, 0), 4.8, bodyf, layers=4, ry=4.0)
    tl = m.bone("tail", bd, (0, 4, 4))
    ball(m, tl, (0, 7.0, 6.0), 3.2, tailf, layers=3, ry=3.6)
    spike(m, tl, (0, 10.4, 6.4), (0, 1, 0.3), 2.0, 2.6, tailf, tip=0.8)
    return m
