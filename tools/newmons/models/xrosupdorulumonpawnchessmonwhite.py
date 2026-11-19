"""Xros Up Dorulumon (Pawn Chessmon (White)) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net, an anime still): Dorulumon Xros Up with a white Pawn Chessmon: plated in white knight armour, a visored helm with a gold unicorn horn over its rust-red mane, and a golden drill lance on its foreleg. 15 blocks.

Front is -z, y is up. Adult stage (by analogy: wikimon gives no level; the base Digimon's). Built on the Dorulumon model.
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
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Dorulumon plated in white knight armour with a visored helm, a gold unicorn horn and a golden drill lance"
_X = {"white": (236, 236, 242), "white_dark": (160, 164, 180), "gold": (240, 196, 60), "gold_dark": (170, 120, 20)}
_S = {"white": (60, 60, 70), "white_dark": (20, 20, 28)}


def P(v):
    return pal(_X, _S, v)


_mod, _body = base("dorulumon", "xrosupdorulumonpawnchessmonwhite")


def build():
    m = _body()
    WH = armour(P, "white", "white_dark", trim="gold", panel=(3.0, 3.0))
    b = [q for q in m.boxes if q.bone == "body"]
    z0 = min(q.lo[2] for q in b); z1 = max(q.lo[2] + q.size[2] for q in b)
    yt = max(q.lo[1] + q.size[1] for q in b)
    for i in range(4):
        z = z0 + 3.0 + i * (z1 - z0 - 6.0) / 3
        m.round_box("body", 0, z, 5.0, 2.0, yt - 2.0, yt + 1.0, WH, cut=1)
    t = top(m, "head")
    m.round_box("head", t[0], t[2], 3.0, 3.4, t[1] - 3.0, t[1] + 0.6, WH, cut=1)
    spike(m, "head", (t[0], t[1], t[2] - 2.0), (0, 0.7, -1), 1.2, 6.0, metal(P, "gold", dark="gold_dark"), tip=0.8)
    lp = [q for q in m.boxes if q.bone == "leg_front_left"]
    x = sum(q.lo[0] + q.size[0] / 2 for q in lp) / len(lp)
    spike(m, "leg_front_left", (x, 10.0, z0 + 2.0), (0, 0, -1), 3.0, 12.0, metal(P, "gold", dark="gold_dark"), tip=0.8)
    return m
