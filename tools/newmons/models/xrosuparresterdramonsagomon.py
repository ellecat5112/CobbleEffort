"""Xros Up Arresterdramon (Sagomon) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net, an anime still): Arresterdramon Xros Up with Sagomon: dark grey monk's sleeves and trousers, golden-cuffed boots, and Sagomon's long staff topped with a golden crescent blade and a spade head. 15 blocks.

Front is -z, y is up. Adult stage (by analogy: wikimon gives no level; the base Digimon's). Built on the Arresterdramon model.
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
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Arresterdramon in dark grey monk's sleeves holding a long staff with a golden crescent blade and a spade head"
_X = {"grey": (70, 70, 80), "grey_dark": (30, 30, 36), "gold": (240, 200, 70), "black": (30, 30, 34), "wood": (60, 50, 40)}
_S = {"grey": (100, 60, 120), "grey_dark": (50, 24, 70)}


def P(v):
    return pal(_X, _S, v)


_mod, _body = base("arresterdramon", "xrosuparresterdramonsagomon", "make")


def build():
    m = _body()
    h = hand(m, "arm_right")
    rod(m, "arm_right", (h[0], 2.0, h[2]), (h[0], h[1] + 26.0, h[2]), 1, solid(P, "wood"), extend=0.0)
    for k in range(8):
        a = math.pi * (0.1 + k / 9)
        m.box("arm_right", h[0] + 5.0 * math.cos(a) - 0.8, h[1] + 28.0 + 5.0 * math.sin(a) - 0.8, h[2] - 0.4,
              h[0] + 5.0 * math.cos(a) + 0.8, h[1] + 28.0 + 5.0 * math.sin(a) + 0.8, h[2] + 0.4, metal(P, "gold"))
    m.box("arm_right", h[0] - 2.4, 1.0, h[2] - 0.6, h[0] + 2.4, 6.0, h[2] + 0.6, metal(P, "black"))
    return m
