"""Jyarimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
Baby I red-orange slime blob with a shiny round body, big glossy black eyes, a tiny wavy mouth and two long swept-back
bat-like horns. A third of a block tall.

Front is -z, y is up. 14 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 14
SCALE, HITBOX = sized(0.35, HEIGHT, 1.0)
KIND = "floater"
K = 4
LOOK = "a red-orange slime blob with big glossy black eyes, a tiny wavy mouth and two long swept-back horns"
BASE = {"red": (240, 90, 60), "red_dark": (180, 40, 30), "red_light": (255, 190, 160), "eye": (20, 20, 24),
        "shine": (255, 255, 255), "mouth": (100, 30, 30)}
SHINY = {"red": (90, 200, 240), "red_dark": (30, 120, 190), "red_light": (200, 240, 255)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.2, y - 6.4)
            if math.hypot(x - sx * 2.2 + 0.4, y - 7.0) < 0.4:
                return tone(p["shine"], face), None
            if d < 1.3:
                return tone(p["eye"], face), None
        if abs(y - 4.0 - 0.3 * abs(math.sin(x * 2.0))) < 0.2 and abs(x) < 1.2:
            return tone(p["mouth"], face), None
    return skin(P, "red", dark="red_dark", light="red_light")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("jyarimon")
    top = m.bone("jyarimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    ball(m, bd, (0, 5.4, 0), 5.0, bodyf, layers=4, squash=0.9)
    hd = m.bone("head", bd, (0, 9, 0))
    for sx in (-1, 1):                                                               # swept horns
        spike(m, hd, (sx * 2.4, 9.0, 1.0), (sx * 0.6, 0.9, 0.6), 2.0, 6.0, skin(P, "red", dark="red_dark"), tip=0.8)
    return m
