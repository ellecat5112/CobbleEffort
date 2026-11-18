"""Madomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
little dog king: a round white-and-brown puppy with huge floppy brown ears, a red velvet crown with a gold rim, a white
fur collar, a short red cape, big paw-print pads, and two tiny ghost-and-skull charms floating beside it. Child stage
(no level on wikimon), 1 block tall.

Front is -z, y is up. 28 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, fur, metal, skin, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1.0, HEIGHT, 3.0)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 8}
LOOK = "a round white-and-brown puppy king with huge floppy brown ears, a red crown, a fur collar and a short red cape"
BASE = {"white": (250, 250, 250), "white_dark": (200, 200, 210), "brown": (170, 110, 60), "brown_dark": (110, 66, 30),
        "red": (200, 30, 40), "red_dark": (120, 10, 20), "gold": (240, 200, 70), "gold_dark": (170, 120, 20),
        "eye": (24, 20, 20), "pink": (240, 140, 150), "blue": (90, 160, 240), "green": (160, 230, 160)}
SHINY = {"brown": (60, 60, 70), "brown_dark": (24, 24, 30)}


def P(v):
    return pal(BASE, SHINY, v)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 1.6, y - 17.4) < 0.6:
                return tone(p["eye"], face), None
        if abs(y - 15.4) < 0.4 and abs(x) < 0.6:
            return tone(p["pink"], face), None
        if abs(x) > 1.4 and y > 16.0:
            return tone(p["brown"], face), None
    return fur(P, "white", "white_dark", length=0.6)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("madomon")
    top = m.bone("madomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 8.0, 0), 4.6, fur(P, "white", "white_dark", length=0.6), layers=4)
    m.round_box(bd, 0, 0, 3.6, 3.4, 11.0, 13.0, fur(P, "white", "white_dark", length=1.2), cut=1)     # fur collar
    m.round_box(bd, 0, 3.4, 3.6, 0.6, 4.0, 12.0, fabric(P, "red", "red_dark"), cut=0)                # cape
    hd = m.bone("head", bd, (0, 13, 0))
    m.round_box(hd, 0, 0, 3.6, 3.2, 13.0, 20.4, headf, cut=2)
    for sx in (-1, 1):                                                               # huge floppy ears
        pts = [(sx * 3.4, 19.0, 0), (sx * 9.0, 17.0, 1.0), (sx * 12.0, 12.0, 1.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 2, fur(P, "brown", "brown_dark", length=1.4), extend=0.6, t2=4)
    m.round_box(hd, 0, 0, 2.6, 2.6, 20.0, 23.4, fabric(P, "red", "red_dark"), cut=1)                  # crown
    m.round_box(hd, 0, 0, 2.8, 2.8, 20.0, 21.0, metal(P, "gold", dark="gold_dark"), cut=1)
    spike(m, hd, (0, 23.4, 0), (0, 1, 0), 0.9, 1.6, metal(P, "gold", dark="gold_dark"), tip=0.8)
    m.round_box(top, -7.0, -3.0, 1.2, 1.0, 9.0, 11.6, solid(P, "blue"), cut=0)                       # ghost charm
    m.round_box(top, -4.0, -4.0, 1.0, 0.8, 9.0, 11.0, solid(P, "green"), cut=0)                      # skull charm
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.0, 4.0, 0))
        m.round_box(lg, sx * 2.4, -1.0, 1.8, 2.4, 0.0, 4.0, fur(P, "white", "white_dark"), cut=1)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.0, 9.0, 0))
        m.round_box(ab, sx * 5.0, -1.0, 1.4, 1.4, 7.0, 10.0, fur(P, "white", "white_dark"), cut=0)
    return m
