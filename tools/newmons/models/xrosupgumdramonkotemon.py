"""Xros Up Gumdramon (Kotemon) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net, an anime still): Gumdramon Xros Up with Kotemon: kendo armour over its purple body, a dark navy face-guard grille, a padded breastplate and skirt, and a bamboo shinai. 1 blocks.

Front is -z, y is up. Child stage (by analogy: wikimon gives no level; the base Digimon's). Built on the Gumdramon model.
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

HEIGHT = 26
SCALE, HITBOX = sized(1, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Gumdramon in kendo armour with a dark navy face-guard grille, a padded breastplate and skirt, and a bamboo shinai"
_X = {"navy": (40, 46, 80), "navy_dark": (14, 16, 30), "cream": (240, 230, 200), "cream_dark": (190, 176, 140), "bamboo": (220, 200, 130), "red": (180, 40, 40), "steel": (180, 184, 196)}
_S = {"navy": (110, 40, 50), "navy_dark": (60, 14, 20)}


def P(v):
    return pal(_X, _S, v)


_mod, _body = base("gumdramon", "xrosupgumdramonkotemon")


def build():
    m = _body()
    b = [q for q in m.boxes if q.bone == "body"]
    yl = min(q.lo[1] for q in b); yh = max(q.lo[1] + q.size[1] for q in b)
    m.round_box("body", 0, 0, 4.0, 3.2, yl + (yh - yl) * 0.45, yh - 0.4, armour(P, "navy", "navy_dark"), cut=1)
    m.round_box("body", 0, 0, 4.4, 3.6, yl - 1.0, yl + (yh - yl) * 0.45, fabric(P, "navy", "navy_dark", axis="x", period=1.2), cut=1)
    hb = [q for q in m.boxes if q.bone == "head"]
    hz = min(q.lo[2] for q in hb); hy0 = min(q.lo[1] for q in hb); hy1 = max(q.lo[1] + q.size[1] for q in hb)
    for j in range(4):
        m.box("head", -3.0, hy0 + 2.0 + j * 1.6, hz - 0.6, 3.0, hy0 + 2.4 + j * 1.6, hz - 0.2, metal(P, "steel"))
    m.box("head", -0.2, hy0 + 1.6, hz - 0.6, 0.2, hy0 + 7.6, hz - 0.2, metal(P, "steel"))
    h = hand(m, "arm_right")
    rod(m, "arm_right", h, (h[0] - 1.0, h[1] + 14.0, h[2] - 3.0), 1, solid(P, "bamboo"), extend=0.0)
    return m
