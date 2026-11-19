"""Waspmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a cyborg wasp drone: a small armoured thorax striped gold and black with clawed legs, a red-eyed
insect head, four striped metal blade-wings with glowing blue edges, and a big round striped abdomen with red spikes
ending in a drill stinger. 15 blocks.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(15, HEIGHT, 3.4)
KIND = "floater"
K = 3
LOOK = "a cyborg wasp drone with striped gold-and-black armour, striped blade-wings and a big round abdomen with a drill stinger"
BASE = {"gold": (220, 170, 60), "gold_dark": (150, 100, 20), "black": (34, 32, 30), "red": (220, 40, 40),
        "blue": (110, 200, 255), "steel": (190, 194, 206), "steel_dark": (90, 94, 106), "eye": (255, 60, 40)}
SHINY = {"gold": (150, 200, 230), "gold_dark": (70, 120, 170)}


def P(v):
    return pal(BASE, SHINY, v)


def stripef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (y % 3.0) < 1.0:
        return tone(p["black"], face), None
    return metal(P, "gold", dark="gold_dark")(x, y, z, face, variant, box=box, **k)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if box is not None and (y - box.lo[1]) < 0.8:
        return p["blue"], p["blue"]
    return tone(p["black"] if (abs(x) % 4.0) < 1.6 else p["gold"], face), None


def build():
    m = Model("waspmon")
    top = m.bone("waspmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    m.round_box(bd, 0, 0, 2.6, 2.6, 18.0, 24.0, stripef, cut=1)                           # thorax
    ball(m, bd, (0, 11.0, 1.0), 6.0, stripef, layers=5)                                   # round abdomen
    for j in range(6):
        ang = j * math.pi / 3
        spike(m, bd, (5.6 * math.cos(ang), 11.0, 1.0 + 5.6 * math.sin(ang)), (math.cos(ang), 0.2, math.sin(ang)), 1.2,
              2.0, solid(P, "red"), tip=0.8)
    spike(m, bd, (0, 5.0, 1.0), (0, -1, 0), 2.0, 5.0, metal(P, "steel", dark="steel_dark"), tip=0.8)   # drill stinger
    hd = m.bone("head", bd, (0, 24, 0))
    m.round_box(hd, 0, -0.6, 2.4, 2.4, 24.0, 28.0, metal(P, "gold", dark="gold_dark"), cut=1)
    for sx in (-1, 1):
        ball(m, hd, (sx * 1.6, 26.6, -2.6), 0.9, solid(P, "eye", glow=True), layers=1)
        rod(m, hd, (sx * 1.0, 28.0, -1.0), (sx * 3.0, 32.0, -3.0), 1, solid(P, "black"), extend=0.2)
    for sx in (-1, 1):                                                                    # four blade-wings
        for j, ang in enumerate((35, 10)):
            wb = m.bone("wing_%s_%d" % ("left" if sx > 0 else "right", j), bd, (sx * 2.0, 23.0, 2.0))
            x0, x1 = sorted((sx * 2.0, sx * (16.0 - j * 3.0)))
            m.box(wb, x0, 22.0 - j * 3.0, 2.0 + j, x1, 25.0 - j * 3.0, 2.8 + j, wingf, rotation=(0, 0, sx * ang),
                  pivot=(sx * 2.0, 23.0, 2.4 + j))
    for i in range(3):                                                                    # clawed legs
        for sx in (-1, 1):
            lg = m.bone("leg_%s_%d" % ("left" if sx > 0 else "right", i), bd, (sx * 2.0, 19.0, -1.0 + i))
            rod(m, lg, (sx * 2.0, 19.0, -1.0 + i), (sx * 5.0, 16.0, -2.0 + i), 1, solid(P, "black"), extend=0.2)
            spike(m, lg, (sx * 5.0, 16.0, -2.0 + i), (sx * 0.3, -1, -0.2), 0.8, 2.0, solid(P, "gold"), tip=0.8)
    return m
