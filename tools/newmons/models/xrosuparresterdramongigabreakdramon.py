"""Xros Up Arresterdramon (Giga Breakdramon) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net, an anime still): Arresterdramon Xros Up with Giga Breakdramon: riding a massive purple-and-green tracked war-machine base with a spiked crusher blade, huge golden mechanical fists, and gold drill spikes on its shoulders. 15 blocks.

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
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Arresterdramon riding a massive purple-and-green tracked war-machine base with huge golden mechanical fists"
_X = {"purple": (110, 60, 170), "purple_dark": (50, 24, 90), "green": (40, 110, 90), "gold": (240, 190, 60), "gold_dark": (170, 120, 20), "steel": (200, 204, 216)}
_S = {"purple": (170, 60, 60), "purple_dark": (90, 20, 20)}


def P(v):
    return pal(_X, _S, v)


_mod, _body = base("arresterdramon", "xrosuparresterdramongigabreakdramon", "make")


def build():
    m = _body()
    PUR = armour(P, "purple", "purple_dark", panel=(3.0, 3.0))
    m.round_box("body", 0, 2.0, 12.0, 9.0, 0.0, 12.0, PUR, cut=2)
    m.round_box("body", 0, 2.0, 9.0, 7.0, 12.0, 20.0, armour(P, "green", "purple_dark"), cut=2)
    m.box("body", -12.0, 1.0, -10.0, 12.0, 8.0, -8.0, metal(P, "steel"))
    for j in range(6):
        spike(m, "body", (-10.0 + j * 4.0, 4.0, -10.0), (0, 0, -1), 1.4, 3.0, metal(P, "steel"), tip=0.8)
    for nm in ("arm_left", "arm_right"):
        h = hand(m, nm)
        ball(m, nm, h, 4.0, metal(P, "gold", dark="gold_dark"), layers=3)
    for sx in (-1, 1):
        spike(m, "body", (sx * 8.0, 52.0, 0), (sx * 0.4, 1, 0.2), 1.6, 7.0, metal(P, "gold"), tip=0.8)
    return m
