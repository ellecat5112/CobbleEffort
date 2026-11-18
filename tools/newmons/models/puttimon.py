"""Puttimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little white cherub blob with a tall curled tuft, big glossy black eyes, a happy pink smile and
two small golden-feathered wings. 0.35 blocks.

Front is -z, y is up. 16 units tall; Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, fan
from _digidetail import feathers, skin, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.35, HEIGHT, 2.0)
KIND = "floater"
K = 4
LOOK = "a little white cherub blob with a tall curled tuft, big glossy black eyes, a pink smile and small golden wings"
BASE = {"white": (246, 248, 255), "white_dark": (200, 210, 230), "black": (20, 20, 26), "glint": (255, 255, 255),
        "pink": (240, 90, 110), "gold": (240, 210, 120), "gold_dark": (190, 150, 60)}
SHINY = {"white": (255, 236, 236), "white_dark": (230, 190, 196), "gold": (200, 220, 250), "gold_dark": (140, 160, 210)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "white", dark="white_dark", var=0.02)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 2.2 + 0.4, y - 5.0) < 0.35:
                return tone(p["glint"], face), None
            if math.hypot(x - sx * 2.2, (y - 4.6) * 0.8) < 1.2:
                return tone(p["black"], face), None
        if abs(y - 3.2) < 0.4 and abs(x) < 0.9:
            return tone(p["pink"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("puttimon")
    top = m.bone("puttimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    ball(m, bd, (0, 4.6, 0), 4.8, bodyf, layers=4, ry=3.8)
    spike(m, bd, (0, 8.0, 0.4), (0, 1, 0.1), 2.2, 6.0, SKIN, tip=0.8)                      # curled tuft
    rod(m, bd, (0, 11.0, 0.6), (1.0, 11.6, 0.8), 1, SKIN, extend=0.2, t2=1)
    for sx in (-1, 1):
        fan(m, bd, (sx * 4.0, 6.0, 1.0), 3, 5.0, 1.4, 10, 50, feathers(P, "gold", "gold_dark"), plane="xy", side=sx)
    return m
