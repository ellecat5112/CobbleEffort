"""Xros Up Tuwarmon (Superstarmon) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net, an anime still): Tuwarmon Xros Up with Superstarmon: a great golden star worn as a breastplate and crest, red scarves streaming from its shoulders, and one huge yellow star-studded fist. 15 blocks.

Front is -z, y is up. Adult stage (by analogy: wikimon gives no level; the base Digimon's). Built on the Tuwarmon model.
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

HEIGHT = 66
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Tuwarmon with a great golden star breastplate and crest, red scarves and one huge yellow star-studded fist"
_X = {"star": (250, 210, 50), "star_dark": (190, 140, 20), "red": (210, 40, 40), "green": (60, 200, 90)}
_S = {"star": (200, 210, 240), "star_dark": (130, 140, 190)}


def P(v):
    return pal(_X, _S, v)


_mod, _body = base("_tuwar", "xrosuptuwarmonsuperstarmon", "make")


def build():
    m = _body()
    ST = metal(P, "star", dark="star_dark")
    for k in range(5):
        a = math.pi / 2 + k * 2 * math.pi / 5
        spike(m, "body", (0, 44.0, -5.0), (math.cos(a), math.sin(a), 0), 3.0, 9.0, ST, tip=0.8)
    ball(m, "body", (0, 44.0, -5.0), 3.0, ST, layers=2)
    for sx in (-1, 1):
        for j in range(3):
            m.box("body", sx * (7.0 + j * 3.0) - 1.4, 50.0 + j, 3.0, sx * (7.0 + j * 3.0) + 1.4, 52.0 + j, 4.0, solid(P, "red"))
    h = hand(m, "arm_left")
    ball(m, "arm_left", (h[0], h[1] + 4.0, h[2]), 5.0, ST, layers=3)
    ball(m, "arm_left", (h[0] - 4.0, h[1] + 6.0, h[2] - 3.0), 1.0, solid(P, "green", glow=True), layers=1)
    return m
