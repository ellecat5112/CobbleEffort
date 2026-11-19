"""Xros Up Mervamon (Beelzebumon) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net, an anime still): Mervamon Xros Up with Beelzebumon: great black feathered wings, black leather straps and gauntlets, and a huge red-and-silver greatsword engraved with runes. 35 blocks.

Front is -z, y is up. Ultimate stage (by analogy: wikimon gives no level; the base Digimon's). Built on the Mervamon model.
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

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 8.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Mervamon with great black feathered wings, black leather gauntlets and a huge red-and-silver rune greatsword"
_X = {"black": (40, 38, 50), "black_dark": (14, 12, 20), "red": (200, 40, 40), "steel": (220, 224, 236), "steel_dark": (110, 114, 130), "rune": (40, 20, 20)}
_S = {"black": (220, 220, 230), "black_dark": (150, 150, 170)}


def P(v):
    return pal(_X, _S, v)


_mod, _body = base("_mervamon", "xrosupmervamonbeelzebumon", "make")


def build():
    m = _body()
    from _digidetail import feathers
    for sx in (-1, 1):
        wb = m.bone("wing_x_" + ("left" if sx > 0 else "right"), "body", (sx * 3.0, 48.0, 4.0))
        feather_wing(m, wb, (sx * 3.0, 48.0, 4.0), 26.0, 16.0, 3, feathers(P, "black", "black_dark"), side=sx, sweep=25, droop=-6.0)
    h = hand(m, "arm_left")
    m.box("arm_left", h[0] - 0.6, h[1] - 0.6, h[2] - 3.0, h[0] + 0.6, h[1] + 0.6, h[2] + 3.0, metal(P, "steel"))
    m.box("arm_left", h[0] - 1.6, h[1] + 0.6, h[2] - 0.8, h[0] + 1.6, h[1] + 28.0, h[2] + 0.8, metal(P, "steel", dark="steel_dark"),
          rotation=(0, 0, -30), pivot=(h[0], h[1], h[2]))
    m.box("arm_left", h[0] - 0.8, h[1] + 3.0, h[2] - 1.0, h[0] + 0.8, h[1] + 24.0, h[2] + 1.0, solid(P, "red"),
          rotation=(0, 0, -30), pivot=(h[0], h[1], h[2]))
    return m
