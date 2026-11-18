"""Shared builder for Pawn Chessmon (Black) and Pawn Chessmon (White) (CobbleEffort: Digital; hand-built after the
official art on wikimon.net): the chess pawn soldiers: a round pawn-shaped body and a knight's helm with a gold barred
visor and a spike on top, a round gold-rimmed shield on one arm, a steel spear in the other hand, ball-jointed limbs
and pointed curled feet. Black or white enamel with gold trim.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import armour, metal, solid
from _route import pal, tone

BASE = {"black": (44, 44, 50), "black_dark": (14, 14, 18), "white": (240, 238, 228), "white_dark": (180, 176, 160),
        "gold": (240, 196, 70), "gold_dark": (160, 120, 20), "steel": (200, 204, 216), "steel_dark": (100, 104, 116),
        "visor": (20, 20, 24)}
SHINY = {"black": (60, 70, 140), "black_dark": (20, 26, 80), "white": (250, 220, 180), "white_dark": (200, 160, 110)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, white=False):
    key, dark = ("white", "white_dark") if white else ("black", "black_dark")
    BODY = armour(P, key, dark, trim="gold", trim_w=0.25)
    GOLD = metal(P, "gold", dark="gold_dark")

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 8, 0))
        ball(m, bd, (0, 12.0, 0), 4.6, BODY, layers=4, ry=4.4)                           # pawn body
        m.round_box(bd, 0, 0, 3.6, 3.6, 16.0, 17.0, GOLD, cut=1)                         # gold collar
        hd = m.bone("head", bd, (0, 17, 0))
        ball(m, hd, (0, 21.0, 0), 4.0, BODY, layers=4, ry=4.0)                           # knight's helm
        for j in range(5):                                                             # barred gold visor
            m.box(hd, -2.6 + j * 1.2, 19.0, -4.2, -2.0 + j * 1.2, 22.6, -3.8, GOLD)
        m.box(hd, -2.8, 19.0, -4.0, 2.8, 22.6, -3.7, solid(P, "visor"))
        spike(m, hd, (0, 25.0, 0), (0, 1, 0), 1.6, 5.0, metal(P, "steel"), tip=0.8)
        spike(m, hd, (-3.6, 22.0, 0), (-1, 0.2, 0), 1.0, 2.0, BODY, tip=0.8)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab = m.bone(nm, bd, (sx * 4.4, 14.0, 0))
            ball(m, ab, (sx * 4.6, 14.0, 0), 1.4, GOLD, layers=2)
            rod(m, ab, (sx * 4.6, 14.0, 0), (sx * 6.0, 10.0, -1.0), 2, BODY, extend=0.3)
            ball(m, ab, (sx * 6.2, 9.4, -1.2), 1.4, GOLD, layers=2)
        for i in range(10):                                                            # round shield
            ang = 2 * math.pi * i / 10
            m.box("arm_left", 7.4 + 3.4 * math.cos(ang) - 0.9, 11.0 + 3.4 * math.sin(ang) - 0.9, -4.0, 7.4 + 3.4 * math.cos(ang) + 0.9,
                  11.0 + 3.4 * math.sin(ang) + 0.9, -3.2, GOLD)
        ball(m, "arm_left", (7.4, 11.0, -3.4), 2.6, BODY, layers=2, squash=0.3)
        rod(m, "arm_right", (-6.2, 0.0, -1.2), (-6.2, 26.0, -1.2), 1, metal(P, "steel", dark="steel_dark"), extend=0.2)
        spike(m, "arm_right", (-6.2, 26.0, -1.2), (0, 1, 0), 1.6, 5.0, metal(P, "steel"), tip=0.8)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, top, (sx * 2.0, 8.0, 0))
            rod(m, lg, (sx * 2.0, 8.0, 0), (sx * 2.4, 2.0, 0), 2, BODY, extend=0.3)
            rod(m, lg, (sx * 2.4, 1.0, 0.6), (sx * 2.8, 1.6, -4.0), 2, BODY, extend=0.3)
        return m

    return build
