"""Meicoomon's Unnamed Baby Form (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard
after the official art on wikimon.net): a round pale-yellow cat head with no body, a white face patch, two pointed
ears tipped brown, big green eyes, a wide happy open mouth with two fangs, and a long tail striped yellow and brown
rising from the back. 0.5 blocks tall.

Front is -z, y is up. 16 units tall; Baby II stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import solid
from _meicoo import P, YEL, cat_eye
from _route import tone

HEIGHT = 16
SCALE, HITBOX = sized(0.5, HEIGHT, 1.2)
KIND = "floater"
K = 3
LOOK = "a round pale-yellow cat head with pointed brown-tipped ears, big green eyes, a wide happy mouth and a striped tail"


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 3.0 + (6.0 - y) * 0.5 and y < 6.0:
        return tone(p["white"], face), None                                            # white face patch
    return YEL(x, y, z, face, variant, box=box, **k)


def tailf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs((y % 2.4) - 1.2) < 0.5:
        return tone((110, 70, 40), face), None
    return YEL(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("meicoomonsunnamedbabyform")
    top = m.bone("meicoomonsunnamedbabyform", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 5.0, 0), 6.4, headf, layers=5, ry=4.6, squash=0.8)
    for sx in (-1, 1):
        cat_eye(m, bd, sx * 1.0, 5.0, -5.15, sx, w=2.0, h=2.2)
        spike(m, bd, (sx * 4.4, 8.6, 0), (sx * 0.3, 1, 0), 2.6, 3.4, YEL, tip=0.8)
        spike(m, bd, (sx * 4.9, 10.8, 0), (sx * 0.3, 1, 0), 1.2, 1.6, solid(P, "black"), tip=0.8)
        spike(m, bd, (sx * 1.2, 2.6, -5.0), (0, -1, 0), 0.8, 0.8, solid(P, "white"), tip=0.8)
    m.round_box(bd, 0, -5.0, 2.2, 0.3, 1.4, 3.4, solid(P, "mouth"), cut=0)
    m.box(bd, -1.2, 1.4, -5.35, 1.2, 2.0, -5.25, solid(P, "pink"))
    tb = m.bone("tail", bd, (3.0, 7.0, 3.0))
    pts = [(3.0, 7.0, 3.0), (4.6, 10.0, 4.0), (5.4, 13.0, 4.4), (5.2, 16.0, 4.6)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 2, tailf, extend=0.4)
    return m
