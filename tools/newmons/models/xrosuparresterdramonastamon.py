"""Xros Up Arresterdramon (Astamon) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net, an anime still): Arresterdramon Xros Up with Astamon: a long grey gangster coat over purple pinstripe trousers, a wild white mane, and a tommy gun in each hand. 15 blocks.

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

HEIGHT = 62
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Arresterdramon in a long grey gangster coat and purple pinstripes with a white mane and a tommy gun in each hand"
_X = {"coat": (170, 170, 176), "coat_dark": (90, 90, 100), "gun": (40, 40, 46), "wood": (120, 70, 40), "white": (240, 240, 246), "white_dark": (180, 180, 196)}
_S = {"coat": (120, 60, 60), "coat_dark": (60, 20, 20)}


def P(v):
    return pal(_X, _S, v)


_mod, _body = base("arresterdramon", "xrosuparresterdramonastamon", "make")


def build():
    m = _body()
    cape(m, "body", 52.0, 16.0, 40.0, fabric(P, "coat", "coat_dark"), z=4.6, flare=0.8, panels=7, seed=5)
    for j in range(7):
        ang = (j - 3) * 0.4
        spike(m, "head", (math.sin(ang) * 3.0, 59.0, 2.0), (math.sin(ang), 0.5, 1), 1.6, 8.0, strands(P, "white", "white_dark"), tip=0.8)
    for nm in ("arm_left", "arm_right"):
        h = hand(m, nm)
        m.box(nm, h[0] - 0.8, h[1] - 0.8, h[2] - 12.0, h[0] + 0.8, h[1] + 0.8, h[2] + 2.0, metal(P, "gun"))
        m.round_box(nm, h[0], h[2] - 5.0, 1.8, 1.8, h[1] - 3.6, h[1] - 0.8, metal(P, "gun"), cut=1)
        m.box(nm, h[0] - 0.6, h[1] - 0.6, h[2] + 2.0, h[0] + 0.6, h[1] + 1.4, h[2] + 6.0, solid(P, "wood"))
    return m
