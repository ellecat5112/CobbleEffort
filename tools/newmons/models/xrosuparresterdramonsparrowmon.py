"""Xros Up Arresterdramon (Sparrowmon) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net, an anime still): Arresterdramon Xros Up with Sparrowmon: great golden jet wings with long swept blades, a visored silver helm and a golden jet-booster pack. 15 blocks.

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
SCALE, HITBOX = sized(15, HEIGHT, 8.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Arresterdramon with great golden jet wings, long swept blades, a visored silver helm and a golden booster pack"
_X = {"gold": (250, 210, 60), "gold_dark": (190, 140, 20), "silver": (220, 224, 236), "visor": (90, 200, 255)}
_S = {"gold": (120, 200, 255), "gold_dark": (60, 130, 200)}


def P(v):
    return pal(_X, _S, v)


_mod, _body = base("arresterdramon", "xrosuparresterdramonsparrowmon", "make")


def build():
    m = _body()
    for sx in (-1, 1):
        m.box("body", min(sx * 3.0, sx * 24.0), 46.0, 4.0, max(sx * 3.0, sx * 24.0), 50.0, 5.0, metal(P, "gold", dark="gold_dark"),
              rotation=(0, 0, sx * 12), pivot=(sx * 3.0, 48.0, 4.5))
        spike(m, "body", (sx * 22.0, 52.0, 4.5), (sx, 0.1, 0), 1.0, 8.0, metal(P, "silver"), tip=0.8)
    m.round_box("body", 0, 6.0, 3.0, 2.4, 38.0, 50.0, metal(P, "gold", dark="gold_dark"), cut=1)
    m.box("head", -2.8, 57.6, -4.6, 2.8, 59.0, -4.0, solid(P, "visor", glow=True))
    return m
