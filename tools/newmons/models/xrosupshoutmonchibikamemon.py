"""Xros Up Shoutmon (Chibi Kamemon) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net, an anime still): Shoutmon Xros Up with Chibi Kamemon: a blue cap pulled down over its head, a green turtle shell on its back, an orange shell-plate with a yellow disc on its belly and white wrist and leg guards. 1 blocks.

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

HEIGHT = 27
SCALE, HITBOX = sized(1, HEIGHT, 1.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Shoutmon in a blue cap with a green turtle shell on its back and an orange belly plate with a yellow disc"
_X = {"blue": (60, 90, 170), "blue_dark": (24, 40, 100), "green": (60, 120, 60), "green_dark": (24, 70, 24), "orange": (230, 120, 50), "yellow": (250, 210, 60), "white": (240, 240, 246)}
_S = {"blue": (170, 60, 60), "blue_dark": (100, 20, 20)}


def P(v):
    return pal(_X, _S, v)


_mod, _body = base("_shoutmon", "xrosupshoutmonchibikamemon", "small", "red")


def build():
    m = _body()
    t = top(m, "head")
    hb = [q for q in m.boxes if q.bone == "head"]
    hy0 = min(q.lo[1] for q in hb)
    m.round_box("head", 0, 0, 4.4, 4.4, t[1] - 4.0, t[1] - 0.6, leather(P, "blue", "blue_dark"), cut=2)
    m.box("head", -4.0, t[1] - 4.0, -6.0, 4.0, t[1] - 3.2, -4.0, leather(P, "blue", "blue_dark"))
    b = [q for q in m.boxes if q.bone == "body"]
    yl = min(q.lo[1] for q in b); yh = max(q.lo[1] + q.size[1] for q in b)
    ball(m, "body", (0, (yl + yh) / 2, 3.4), 4.0, armour(P, "green", "green_dark", panel=(2.0, 2.0)), layers=3, squash=0.6)
    m.round_box("body", 0, -3.0, 3.0, 0.6, yl + 1.0, yh - 1.0, solid(P, "orange"), cut=0)
    ball(m, "body", (0, (yl + yh) / 2, -3.8), 1.4, solid(P, "yellow"), layers=1)
    return m
