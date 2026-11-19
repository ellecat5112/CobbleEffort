"""Xros Up Astamon (Triceramon) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net, an anime still): Astamon Xros Up with Triceramon: a Triceramon head worn as a great horned pauldron on one shoulder, a long grey coat lined with red, and armoured clawed boots. 25 blocks.

Front is -z, y is up. Perfect stage (by analogy: wikimon gives no level; the base Digimon's). Built on the Astamon model.
"""
from __future__ import annotations

import math

from _boxmodel import rod, spike
from _digi import sized
from _digibeast import ball, bat_wing, feather_wing
from _digibody import cape
from _digidetail import armour, fabric, fur, leather, metal, skin, solid, strands
from _route import pal, tone
from _xrosup import base, hand, top

HEIGHT = 61
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Astamon with a horned Triceramon head as a great pauldron, a long red-lined grey coat and armoured clawed boots"
_X = {"coat": (170, 170, 176), "coat_dark": (90, 90, 100), "teal": (70, 110, 110), "teal_dark": (30, 60, 60), "horn": (220, 210, 190), "gem": (80, 220, 230), "lining": (110, 20, 30)}
_S = {"teal": (120, 80, 60), "teal_dark": (60, 30, 20)}


def P(v):
    return pal(_X, _S, v)


_mod, _body = base("astamon", "xrosupastamontriceramon")


def build():
    m = _body()
    cape(m, "body", 52.0, 18.0, 46.0, fabric(P, "coat", "coat_dark"), z=4.6, flare=0.9, panels=8, seed=12)
    m.round_box("body", -9.0, 0, 5.0, 5.4, 44.0, 54.0, armour(P, "teal", "teal_dark"), cut=2)
    for j in range(3):
        spike(m, "body", (-9.0 + (j - 1) * 2.4, 53.0, -2.0), ((j - 1) * 0.2, 1, -0.3), 1.6, 8.0, solid(P, "horn"), tip=0.8)
    ball(m, "body", (-9.0, 49.0, -5.6), 1.0, solid(P, "gem", glow=True), layers=1)
    return m
