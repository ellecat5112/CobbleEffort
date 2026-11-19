"""Xros Up Shoutmon (Pinochimon) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net, an anime still): Shoutmon Xros Up with Pinochimon: a wooden cross of planks strapped to its back, a yellow scarf, a harness of straps, and Pinochimon's great revolver-cylinder hammer in its hand. 1 blocks.

Front is -z, y is up. Child stage (by analogy: wikimon gives no level; the base Digimon's). Built on the Shoutmon model.
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

HEIGHT = 30
SCALE, HITBOX = sized(1, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Shoutmon with a wooden plank cross strapped to its back, a yellow scarf and a great revolver-cylinder hammer"
_X = {"wood": (140, 100, 60), "wood_dark": (80, 54, 30), "yellow": (250, 210, 60), "steel": (150, 150, 160), "steel_dark": (70, 70, 80), "strap": (40, 120, 140)}
_S = {"wood": (100, 100, 110), "wood_dark": (50, 50, 60)}


def P(v):
    return pal(_X, _S, v)


_mod, _body = base("_shoutmon", "xrosupshoutmonpinochimon", "small", "red")


def build():
    m = _body()
    b = [q for q in m.boxes if q.bone == "body"]
    yl = min(q.lo[1] for q in b); yh = max(q.lo[1] + q.size[1] for q in b)
    cy = (yl + yh) / 2
    for ang in (35, -35):
        m.box("body", -1.0, cy - 9.0, 3.4, 1.0, cy + 9.0, 4.6, leather(P, "wood", "wood_dark"), rotation=(0, 0, ang), pivot=(0, cy, 4.0))
    m.round_box("body", 0, 0, 3.6, 3.2, yh - 1.0, yh + 0.6, solid(P, "yellow"), cut=1)
    h = (-6.0, cy, -2.0)
    rod(m, "arm_right", (h[0], 1.0, h[2]), (h[0], cy + 12.0, h[2]), 1, metal(P, "steel"), extend=0.0)
    m.round_box("arm_right", h[0], h[2], 3.0, 3.0, cy + 12.0, cy + 18.0, metal(P, "steel", dark="steel_dark"), cut=1)
    return m
