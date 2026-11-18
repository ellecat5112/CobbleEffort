"""Pyonmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a round fluffy cream-yellow fur-ball with a small brown face of tiny eyes and a dot mouth, and one
long pale stalk growing up from its crown with a green tip. 0.35 blocks.

Front is -z, y is up. 18 units tall; Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _digi import sized
from _digibeast import ball
from _digidetail import fur, skin, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.35, HEIGHT, 1.4)
KIND = "floater"
K = 4
LOOK = "a round fluffy cream-yellow fur-ball with a small brown face and one long pale stalk with a green tip"
BASE = {"cream": (250, 230, 150), "cream_dark": (210, 180, 90), "brown": (110, 70, 40), "black": (20, 16, 14),
        "eye": (130, 150, 170), "stalk": (240, 236, 170), "stalk_dark": (200, 190, 110), "green": (110, 120, 50)}
SHINY = {"cream": (220, 220, 236), "cream_dark": (160, 160, 190)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and math.hypot(x, (y - 3.6) * 1.1) < 3.0:
        for sx in (-1, 1):
            if math.hypot(x - sx * 1.2, y - 4.2) < 0.5:
                return tone(p["eye"], face), None
        if math.hypot(x, y - 3.0) < 0.3:
            return tone(p["black"], face), None
        return tone(p["brown"], face), None
    return fur(P, "cream", "cream_dark", length=1.0, density=1.4)(x, y, z, face, variant, box=box, **k)


def stalkf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if y > 16.0:
        return tone(p["green"], face), None
    return skin(P, "stalk", dark="stalk_dark", var=0.02)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("pyonmon")
    top = m.bone("pyonmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    ball(m, bd, (0, 4.6, 0.4), 4.8, bodyf, layers=4, ry=4.4)
    rod(m, bd, (0, 8.0, 0.4), (1.2, 17.6, 0.0), 3, stalkf, extend=0.4)
    return m
