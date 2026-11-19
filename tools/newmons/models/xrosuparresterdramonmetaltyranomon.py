"""Xros Up Arresterdramon (Metal Tyranomon) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net, an anime still): Arresterdramon Xros Up with Metal Tyranomon: bulked out with heavy black armour plates and spiked pauldrons, a steel-jawed helm, and two enormous black claw-cannons with golden talons for arms. 15 blocks.

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
LOOK = "Arresterdramon in heavy black armour with a steel-jawed helm and two enormous black claw-cannons with golden talons"
_X = {"black": (50, 50, 58), "black_dark": (16, 16, 20), "gold": (240, 190, 60), "steel": (200, 204, 216), "steel_dark": (100, 104, 116)}
_S = {"black": (150, 150, 160), "black_dark": (80, 80, 90)}


def P(v):
    return pal(_X, _S, v)


_mod, _body = base("arresterdramon", "xrosuparresterdramonmetaltyranomon", "make")


def build():
    m = _body()
    BLK = armour(P, "black", "black_dark", panel=(3.0, 3.0))
    m.round_box("body", 0, 0, 7.0, 5.4, 38.0, 52.0, BLK, cut=2)
    for sx in (-1, 1):
        m.round_box("body", sx * 9.0, 0, 4.4, 4.4, 46.0, 54.0, BLK, cut=2)
        spike(m, "body", (sx * 10.0, 54.0, 0), (sx * 0.3, 1, 0), 1.6, 5.0, metal(P, "steel"), tip=0.8)
    m.round_box("head", 0, -5.0, 2.6, 1.6, 54.0, 56.4, metal(P, "steel", dark="steel_dark"), cut=1)
    for nm in ("arm_left", "arm_right"):
        h = hand(m, nm)
        sx = 1 if nm == "arm_left" else -1
        ball(m, nm, (h[0] + sx * 2.0, h[1] + 2.0, h[2]), 6.0, BLK, layers=4)
        for t in range(3):
            spike(m, nm, (h[0] + sx * 2.0 + (t - 1) * 3.0, h[1] - 3.0, h[2] - 4.0), (0, -0.5, -1), 1.6, 5.0, metal(P, "gold"), tip=0.8)
    return m
