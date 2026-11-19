"""Xros Up Submarimon (Plesiomon) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net, an anime still): Submarimon Xros Up with Plesiomon: its submarine body gains Plesiomon's long white neck and graceful crested head, sweeping white flippers banded blue and a trailing tail fin. 15 blocks.

Front is -z, y is up. Adult stage (by analogy: wikimon gives no level; the base Digimon's). Built on the Submarimon model.
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

HEIGHT = 33
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "floater"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Submarimon with Plesiomon's long white neck and crested head, sweeping white flippers banded blue and a tail fin"
_X = {"white": (240, 242, 248), "white_dark": (180, 186, 204), "blue": (60, 90, 180), "gold": (240, 200, 70), "eye": (60, 140, 230)}
_S = {"white": (220, 200, 150), "white_dark": (170, 140, 90)}


def P(v):
    return pal(_X, _S, v)


_mod, _body = base("submarimon", "xrosupsubmarimonplesiomon")


def build():
    m = _body()
    WH = skin(P, "white", dark="white_dark")
    b = m.boxes
    zf = min(q.lo[2] for q in b); yt = max(q.lo[1] + q.size[1] for q in b)
    nk = m.bone("neck", "body", (0, yt - 2.0, zf + 6.0))
    pts = [(0, yt - 2.0, zf + 6.0), (0, yt + 4.0, zf + 2.0), (0, yt + 9.0, zf - 2.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, nk, p0, p1, 2, WH, extend=0.6)
    hx, hy, hz = pts[-1]
    m.round_box(nk, 0, hz - 3.0, 1.6, 3.6, hy - 1.0, hy + 2.0, WH, cut=1)
    for sx in (-1, 1):
        m.box(nk, sx * 1.5 - 0.3, hy + 0.6, hz - 4.6, sx * 1.5 + 0.3, hy + 1.4, hz - 3.6, solid(P, "eye", glow=True))
    spike(m, nk, (0, hy + 2.0, hz - 1.0), (0, 0.6, 1), 1.2, 5.0, metal(P, "gold"), tip=0.8)
    for sx in (-1, 1):
        m.box("body", min(sx * 4.0, sx * 18.0), 4.0, zf + 6.0, max(sx * 4.0, sx * 18.0), 5.0, zf + 12.0, WH,
              rotation=(0, sx * -20, sx * -8), pivot=(sx * 4.0, 4.5, zf + 9.0))
    return m
