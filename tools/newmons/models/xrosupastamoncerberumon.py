"""Xros Up Astamon (Cerberumon) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net, an anime still): Astamon Xros Up with Cerberumon: its legs clad in black wolf-hide armour ending in great ivory claws, black clawed gauntlets and a streaming red scarf. 25 blocks.

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
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Astamon with black wolf-hide armoured legs and claws, black clawed gauntlets and a streaming red scarf"
_X = {"black": (40, 38, 44), "black_dark": (14, 12, 16), "ivory": (240, 230, 210), "red": (210, 30, 40)}
_S = {"black": (120, 80, 50), "black_dark": (60, 30, 14)}


def P(v):
    return pal(_X, _S, v)


_mod, _body = base("astamon", "xrosupastamoncerberumon")


def build():
    m = _body()
    BLK = fur(P, "black", "black_dark", length=1.6)
    for nm in ("leg_left", "leg_right"):
        bs = [b for b in m.boxes if b.bone == nm]
        x = sum(b.lo[0] + b.size[0] / 2 for b in bs) / len(bs)
        m.round_box(nm, x, 0.4, 3.0, 3.4, 2.0, 16.0, BLK, cut=1)
        for t in range(3):
            spike(m, nm, (x + (t - 1) * 1.6, 1.0, -3.4), (0, -0.2, -1), 1.2, 4.0, solid(P, "ivory"), tip=0.8)
    for nm in ("arm_left", "arm_right"):
        h = hand(m, nm)
        m.round_box(nm, h[0], h[2], 2.6, 2.6, h[1] - 1.0, h[1] + 5.0, BLK, cut=1)
    for j in range(4):
        m.box("body", 2.0 + j * 3.0, 50.0 + j * 0.6, 2.0, 5.0 + j * 3.0, 52.0 + j * 0.6, 3.0, solid(P, "red"), rotation=(0, 0, 10), pivot=(2.0 + j * 3.0, 51.0, 2.5))
    return m
