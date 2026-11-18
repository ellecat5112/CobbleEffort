"""Meicoomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a small golden-orange cat striped black like a tiger, with a big round head, spiky black-tipped
fur round its face, a white fluffy chest, a black zigzag mark on its brow, big green eyes, white paws, a short fluffy
tail and two very long ribbon ears banded orange and black that curl up over it, ending in little claws. 15 blocks
tall.

Front is -z, y is up. 40 units tall (the ribbons included); Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import solid
from _meicoo import FUR, P, WHITE, cat_eye, ribbon, striped
from _route import tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a small golden-orange cat striped black with a big round head, a white fluffy chest, big green eyes, a zigzag "
        "brow mark and two very long orange-and-black ribbon ears curling up over it")
BODY = striped()


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(y - 21.5 - 0.8 * abs((x * 1.2) % 2.0 - 1.0)) < 0.3 and abs(x) < 2.6:
        return tone(p["black"], face), None                                           # zigzag brow mark
    return BODY(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("meicoomon")
    top = m.bone("meicoomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 9.0, 0.5), 4.2, BODY, layers=4, ry=4.6)                                # body
    ball(m, bd, (0, 10.0, -2.2), 3.0, WHITE, layers=4, ry=3.6, squash=0.5)                 # fluffy chest
    hd = m.bone("head", bd, (0, 14, 0))
    ball(m, hd, (0, 18.0, -0.4), 6.6, headf, layers=6, ry=5.6, squash=0.85)                # big round head
    for sx in (-1, 1):
        cat_eye(m, hd, sx * 0.7, 17.0, -5.85, sx, w=2.2, h=2.6)
        for j in range(4):                                                                # spiky cheek fur
            spike(m, hd, (sx * 5.4, 15.0 + j * 1.6, -1.0), (sx * 1, -0.3 + j * 0.25, 0.3), 1.6, 3.6 - j * 0.4,
                  WHITE if j < 2 else solid(P, "black"), tip=0.8)
        spike(m, hd, (sx * 3.6, 22.4, 0.0), (sx * 0.5, 1, 0.1), 2.4, 3.6, FUR, tip=0.8)     # little cat ears
    m.box(hd, -0.5, 15.4, -5.9, 0.5, 16.0, -5.6, solid(P, "pink"))
    m.box(hd, -1.0, 14.0, -5.6, 1.0, 14.8, -5.4, solid(P, "mouth"))
    for i in range(6):                                                                    # black-tipped crown spikes
        ang = math.radians(-60 + i * 24)
        spike(m, hd, (4.0 * math.sin(ang), 22.0, 1.0), (math.sin(ang), 0.9, 0.6), 1.6, 3.4, solid(P, "black"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.6, 11.0, -0.5))
        rod(m, ab, (sx * 3.6, 11.0, -0.5), (sx * 5.4, 7.0, -3.0), 2, BODY, extend=0.4)
        m.round_box(ab, sx * 5.6, -3.4, 1.4, 1.4, 4.8, 7.4, WHITE, cut=0)
        for j in range(3):
            spike(m, ab, (sx * 5.6 + (j - 1) * 0.8, 5.2, -4.6), (0, -0.6, -1), 0.8, 1.2, solid(P, "claw"), tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lb = m.bone(nm, top, (sx * 2.4, 6.0, 0.8))
        rod(m, lb, (sx * 2.4, 7.0, 0.8), (sx * 2.8, 2.0, 0.0), 3, BODY, extend=0.4)
        m.round_box(lb, sx * 2.8, -1.0, 1.6, 2.2, 0.0, 2.0, WHITE, cut=0)
    tb = m.bone("tail", bd, (0, 7, 4))
    rod(m, tb, (0, 7.0, 4.0), (0, 10.0, 8.0), 2, BODY, extend=0.4)
    ball(m, tb, (0, 11.0, 9.0), 1.6, WHITE, layers=2)
    eb = m.bone("ears", hd, (0, 22, 1))                                                   # long ribbon ears
    for sx in (-1, 1):
        pts = [(sx * 3.0, 22.0, 1.0), (sx * 6.0, 28.0, 2.0), (sx * 9.0, 33.0, 4.0), (sx * 8.0, 38.0, 6.0),
               (sx * 4.0, 40.0, 7.0), (sx * 1.0, 37.0, 7.0)]
        ribbon(m, eb, pts, 2)
    return m
