"""Sakuttomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a round glossy golden baby with two black-edged blade ears swept up like knives, small tufted feet,
narrowed brown eyes and a zigzag grin. 0.5 blocks.

Front is -z, y is up. 18 units tall; Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, skin, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.5, HEIGHT, 2.0)
KIND = "floater"
K = 4
LOOK = "a round glossy golden baby with two black-edged blade ears swept up like knives, narrowed eyes and a zigzag grin"
BASE = {"gold": (250, 220, 70), "gold_dark": (200, 150, 20), "gold_light": (255, 245, 180), "black": (30, 26, 20),
        "eye": (110, 70, 40), "white": (255, 255, 255)}
SHINY = {"gold": (200, 210, 230), "gold_dark": (130, 140, 170), "gold_light": (240, 246, 255)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.8) < 1.0 and abs(y - 6.0 - (x * sx - 1.8) * 0.3) < 0.5:
                return tone(p["eye"], face), None
        if abs(y - 3.6 - 0.4 * abs(math.sin(x * 2.4))) < 0.2 and abs(x) < 2.0:
            return tone(p["black"], face), None
    return skin(P, "gold", dark="gold_dark", light="gold_light", var=0.02)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("sakuttomon")
    top = m.bone("sakuttomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    ball(m, bd, (0, 5.4, 0), 5.0, bodyf, layers=4, ry=4.6)
    for sx in (-1, 1):                                                                   # blade ears
        m.box(bd, min(sx * 2.4, sx * 3.4), 9.0, -2.0, max(sx * 2.4, sx * 3.4), 17.0, 2.0, metal(P, "gold", dark="black"),
              rotation=(0, 0, -sx * 25), pivot=(sx * 2.9, 9.0, 0))
        spike(m, bd, (sx * 2.0, 1.0, -1.0), (sx * 0.4, -1, -0.4), 1.2, 1.6, bodyf, tip=0.8)
    return m
