"""Xros Up Arresterdramon (Blossomon) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net, an anime still): Arresterdramon Xros Up with Blossomon: a skirt of broad green leaves, a yellow flower-face on its chest, green-and-red leaf wings, and four red flower heads with glowing centres on long vine stalks round it. 15 blocks.

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
LOOK = "Arresterdramon with a green leaf skirt, a yellow flower-face chest and four red flower heads on vines"
_X = {"leaf": (80, 160, 70), "leaf_dark": (30, 90, 30), "yellow": (250, 210, 60), "red": (190, 40, 60), "glow": (200, 255, 120), "vine": (60, 130, 60)}
_S = {"red": (220, 120, 200), "leaf": (60, 140, 160), "leaf_dark": (20, 80, 100)}


def P(v):
    return pal(_X, _S, v)


_mod, _body = base("arresterdramon", "xrosuparresterdramonblossomon", "make")


def build():
    m = _body()
    for i in range(8):
        ang = i * 2 * math.pi / 8
        spike(m, "body", (5.0 * math.sin(ang), 32.0, 4.0 * math.cos(ang)), (math.sin(ang) * 0.6, -1, math.cos(ang) * 0.6), 3.0, 12.0, skin(P, "leaf", dark="leaf_dark"), tip=0.8)
    ball(m, "body", (0, 44.0, -5.0), 3.0, solid(P, "yellow"), layers=2)
    for sx in (-1, 1):
        spike(m, "body", (sx * 3.0, 50.0, 4.0), (sx * 0.8, 0.8, 0.4), 2.4, 14.0, solid(P, "leaf"), tip=0.8)
        for j in range(2):
            stalk = [(sx * 6.0, 40.0, 0), (sx * 14.0, 46.0 - j * 14.0, -2.0), (sx * 20.0, 50.0 - j * 22.0, -1.0)]
            for p0, p1 in zip(stalk, stalk[1:]):
                rod(m, "body", p0, p1, 1, solid(P, "vine"), extend=0.2)
            c = stalk[-1]
            for k in range(6):
                a = k * math.pi / 3
                spike(m, "body", c, (math.cos(a), math.sin(a), 0), 1.6, 3.0, solid(P, "red"), tip=0.8)
            ball(m, "body", c, 1.4, solid(P, "glow", glow=True), layers=1)
    return m
