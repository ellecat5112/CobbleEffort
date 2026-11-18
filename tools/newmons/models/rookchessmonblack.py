"""Rook Chessmon (Black) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the black castle of the chessboard: a squat iron tower of a body crowned with crenellated
battlements and turret domes, a great riveted cannon for one arm, a heavy black wedge of a shield-fist for the other,
and stout jointed steel legs. 25 blocks.

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, riveted, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 5}
LOOK = "a squat black iron castle-tower of a body with battlements and turret domes, a riveted cannon arm and a black wedge shield-fist"
BASE = {"iron": (70, 72, 80), "iron_dark": (24, 26, 30), "steel": (180, 184, 196), "steel_dark": (90, 94, 108),
        "green": (60, 160, 90), "eye": (250, 80, 40), "black": (20, 20, 24)}
SHINY = {"iron": (230, 230, 236), "iron_dark": (160, 160, 176)}


def P(v):
    return pal(BASE, SHINY, v)


IRON = riveted(P, "iron", "iron_dark")
STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("rookchessmonblack")
    top = m.bone("rookchessmonblack", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 0, 7.0, 6.0, 12.0, 30.0, IRON, cut=2)                               # tower body
    m.round_box(bd, 0, 0, 8.0, 7.0, 28.0, 31.0, IRON, cut=2)
    for i in range(8):                                                                   # battlements
        ang = 2 * math.pi * i / 8
        cx, cz = 6.6 * math.cos(ang), 5.6 * math.sin(ang)
        m.box(bd, cx - 1.4, 31.0, cz - 1.4, cx + 1.4, 34.0, cz + 1.4, IRON)
    hd = m.bone("head", bd, (0, 31, 0))
    ball(m, hd, (0, 34.0, 0), 3.0, STEEL, layers=3)                                        # turret domes
    spike(m, hd, (0, 36.6, 0), (0, 1, 0), 1.0, 3.0, STEEL, tip=0.8)
    m.box(hd, -1.6, 33.4, -3.1, 1.6, 34.2, -2.9, solid(P, "eye", glow=True))
    for sx in (-1, 1):
        ball(m, bd, (sx * 5.0, 33.0, 2.0), 1.8, STEEL, layers=2)
        m.round_box(bd, sx * 3.0, -6.2, 0.8, 0.4, 20.0, 22.0, solid(P, "green"), cut=0)
    ab = m.bone("arm_right", bd, (-8.0, 24.0, 0))                                        # riveted cannon arm
    rod(m, ab, (-8.0, 24.0, 0), (-18.0, 22.0, -4.0), 5, IRON, extend=0.6)
    rod(m, ab, (-18.0, 22.0, -4.0), (-26.0, 22.0, -6.0), 3, STEEL, extend=0.4)
    m.round_box(ab, -26.4, -6.0, 0.6, 1.4, 21.0, 23.0, solid(P, "black"), cut=0)
    ab2 = m.bone("arm_left", bd, (8.0, 24.0, 0))                                         # wedge shield-fist
    rod(m, ab2, (8.0, 24.0, 0), (12.0, 18.0, -2.0), 3, STEEL, extend=0.4)
    m.box(ab2, 10.0, 8.0, -10.0, 22.0, 18.0, 2.0, armour(P, "iron", "iron_dark"),
          rotation=(0, -20, 0), pivot=(14.0, 13.0, -4.0))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 12.0, 0))
        ball(m, lg, (sx * 4.0, 10.0, 0), 2.4, STEEL, layers=2)
        rod(m, lg, (sx * 4.0, 10.0, 0), (sx * 4.6, 3.0, -1.0), 3, IRON, extend=0.4)
        m.round_box(lg, sx * 4.6, -1.6, 3.0, 4.0, 0.0, 3.0, IRON, cut=1)
    return m
