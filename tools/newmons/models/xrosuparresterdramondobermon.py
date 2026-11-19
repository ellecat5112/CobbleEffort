"""Xros Up Arresterdramon (Dobermon) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net, an anime still): Arresterdramon Xros Up with Dobermon: its body joined to the lean black body of a great dog behind, running on four long legs, with huge golden spiked gauntlets on its arms. 15 blocks.

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
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Arresterdramon joined to a lean black dog body on four long legs, with huge golden spiked gauntlets"
_X = {"black": (40, 38, 44), "black_dark": (14, 12, 16), "tan": (150, 110, 70), "gold": (240, 190, 60), "gold_dark": (170, 120, 20), "steel": (200, 204, 216)}
_S = {"black": (130, 90, 60), "black_dark": (70, 40, 20)}


def P(v):
    return pal(_X, _S, v)


_mod, _body = base("arresterdramon", "xrosuparresterdramondobermon", "make")


def build():
    m = _body()
    BLK = skin(P, "black", dark="black_dark")
    for i in range(5):
        m.round_box("body", 0, 6.0 + i * 3.2, 4.0, 1.8, 26.0, 33.0, BLK, cut=1)
    for sx in (-1, 1):
        for z in (6.0, 18.0):
            rod(m, "body", (sx * 3.4, 27.0, z), (sx * 3.6, 12.0, z + 1.0), 2, BLK, extend=0.4)
            rod(m, "body", (sx * 3.6, 12.0, z + 1.0), (sx * 3.6, 1.0, z), 1, BLK, extend=0.4)
            m.round_box("body", sx * 3.6, z - 1.0, 1.2, 2.0, 0.0, 1.4, solid(P, "tan"), cut=0)
    for nm in ("arm_left", "arm_right"):
        h = hand(m, nm)
        m.round_box(nm, h[0], h[2], 3.0, 3.0, h[1] - 1.0, h[1] + 6.0, metal(P, "gold", dark="gold_dark"), cut=1)
        spike(m, nm, (h[0], h[1] + 3.0, h[2] - 3.0), (0, 0, -1), 1.4, 4.0, metal(P, "steel"), tip=0.8)
    return m
