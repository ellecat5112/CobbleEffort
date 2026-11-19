"""Xros Up Omega Shoutmon (Dorulumon) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net, an anime still): Omega Shoutmon Xros Up with Dorulumon: two massive orange-and-white wolf cannon pods mounted over its shoulders, each with a long grey barrel, and grey wolf-clawed armour on its legs. 25 blocks.

Front is -z, y is up. Perfect stage (by analogy: wikimon gives no level; the base Digimon's). Built on the Omega Shoutmon model.
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

HEIGHT = 65
SCALE, HITBOX = sized(25, HEIGHT, 8.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Omega Shoutmon with two massive orange-and-white wolf cannon pods over its shoulders and wolf-clawed leg armour"
_X = {"orange": (220, 110, 60), "orange_dark": (140, 60, 20), "white": (240, 240, 246), "steel": (120, 124, 136), "steel_dark": (50, 54, 66), "yellow": (250, 210, 60), "claw": (60, 56, 60)}
_S = {"orange": (90, 130, 200), "orange_dark": (40, 70, 140)}


def P(v):
    return pal(_X, _S, v)


_mod, _body = base("_omegashoutmon", "xrosupomegashoutmondorulumon", "make")


def build():
    m = _body()
    for sx in (-1, 1):
        m.round_box("body", sx * 13.0, 2.0, 5.0, 6.0, 44.0, 58.0, armour(P, "orange", "orange_dark", trim="white"), cut=2)
        rod(m, "body", (sx * 13.0, 56.0, 2.0), (sx * 13.0, 66.0, -6.0), 2, metal(P, "steel", dark="steel_dark"), extend=0.0)
        m.box("body", sx * 13.0 - 3.0, 48.0, -4.2, sx * 13.0 + 3.0, 51.0, -3.8, solid(P, "yellow"))
    for nm in ("leg_left", "leg_right"):
        bs = [b for b in m.boxes if b.bone == nm]
        x = sum(b.lo[0] + b.size[0] / 2 for b in bs) / len(bs)
        for t in range(3):
            spike(m, nm, (x + (t - 1) * 1.6, 1.0, -3.4), (0, -0.2, -1), 1.2, 4.0, solid(P, "claw"), tip=0.8)
    return m
