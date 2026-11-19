"""Xros Up Ballistamon (Revolmon) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net, an anime still): Ballistamon Xros Up with Revolmon: a wide orange cowboy hat on its head, a red bandana streaming behind, and two huge silver revolver barrels fitted over its arms. 15 blocks.

Front is -z, y is up. Adult stage (by analogy: wikimon gives no level; the base Digimon's). Built on the Ballistamon model.
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

HEIGHT = 55
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Ballistamon in a wide orange cowboy hat and red bandana with two huge silver revolver barrels over its arms"
_X = {"hat": (230, 150, 50), "hat_dark": (170, 100, 20), "red": (210, 30, 40), "steel": (210, 214, 226), "steel_dark": (110, 114, 126)}
_S = {"hat": (120, 90, 60), "hat_dark": (70, 50, 30)}


def P(v):
    return pal(_X, _S, v)


_mod, _body = base("ballistamon", "xrosupballistamonrevolmon", "make")


def build():
    m = _body()
    t = top(m, "head")
    m.round_box("head", t[0], t[2], 9.0, 9.0, t[1] - 0.6, t[1] + 0.6, leather(P, "hat", "hat_dark"), cut=4)
    m.round_box("head", t[0], t[2], 4.6, 4.6, t[1] + 0.6, t[1] + 5.6, leather(P, "hat", "hat_dark"), cut=2)
    for j in range(4):
        m.box("body", -10.0 - j * 3.0, 40.0 - j * 1.0, 2.0, -7.0 - j * 3.0, 42.0 - j * 1.0, 3.0, solid(P, "red"))
    for nm in ("arm_left", "arm_right"):
        h = hand(m, nm)
        rod(m, nm, (h[0], h[1], h[2] + 2.0), (h[0], h[1], h[2] - 14.0), 3, metal(P, "steel", dark="steel_dark"), extend=0.0)
        m.round_box(nm, h[0], h[2] - 1.0, 3.4, 3.4, h[1] - 3.4, h[1] + 3.4, metal(P, "steel", dark="steel_dark"), cut=1)
    return m
