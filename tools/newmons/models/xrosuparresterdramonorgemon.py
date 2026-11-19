"""Xros Up Arresterdramon (Orgemon) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net, an anime still): Arresterdramon Xros Up with Orgemon: a green ogre vest, a wild white mane with an eye-patch strap, and Orgemon's great bone club in hand. 15 blocks.

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
LOOK = "Arresterdramon in a green ogre vest with a wild white mane and a great bone club"
_X = {"green": (90, 170, 70), "green_dark": (40, 100, 30), "white": (240, 240, 246), "white_dark": (180, 180, 196), "bone": (240, 230, 200), "bone_dark": (180, 160, 120)}
_S = {"green": (170, 90, 160), "green_dark": (100, 40, 90)}


def P(v):
    return pal(_X, _S, v)


_mod, _body = base("arresterdramon", "xrosuparresterdramonorgemon", "make")


def build():
    m = _body()
    m.round_box("body", 0, 0, 6.0, 4.4, 36.0, 50.0, fabric(P, "green", "green_dark"), cut=2)
    for j in range(9):
        ang = (j - 4) * 0.4
        spike(m, "head", (math.sin(ang) * 3.0, 59.0, 2.0), (math.sin(ang), 0.6, 1), 1.6, 9.0, strands(P, "white", "white_dark"), tip=0.8)
    h = hand(m, "arm_left")
    rod(m, "arm_left", (h[0], h[1] - 2.0, h[2]), (h[0] + 6.0, h[1] + 16.0, h[2] - 2.0), 2, skin(P, "bone", dark="bone_dark"), extend=0.0)
    ball(m, "arm_left", (h[0] + 6.4, h[1] + 17.0, h[2] - 2.0), 2.6, skin(P, "bone", dark="bone_dark"), layers=2)
    return m
