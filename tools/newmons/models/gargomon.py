"""Gargomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the gargoyle beast: a long-limbed white beast-machine bound in steel bands and golden bolts, a
narrow gargoyle head under a dark visor, great white feathered wings, a whip-like blue tail and huge clawed hands and
feet tipped blue. 15 blocks tall.

Front is -z, y is up. 48 units tall; Adult stage (Armor on wikimon).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digidetail import feathers, metal, skin, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a long-limbed white gargoyle beast bound in steel bands and golden bolts, a dark-visored head, great white "
        "feathered wings, a blue whip tail and blue-tipped claws")
BASE = {"white": (240, 240, 246), "white_dark": (170, 174, 196), "steel": (170, 176, 190), "steel_dark": (80, 86, 100),
        "gold": (230, 190, 70), "gold_dark": (150, 110, 20), "blue": (60, 90, 190), "blue_dark": (20, 40, 110),
        "visor": (40, 40, 50)}
SHINY = {"white": (60, 60, 70), "white_dark": (24, 24, 30), "blue": (200, 40, 50)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = skin(P, "white", dark="white_dark")
STEEL = metal(P, "steel", dark="steel_dark")
GOLD = metal(P, "gold", dark="gold_dark")


def limb(m, bone, pts, t):
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, bone, p0, p1, t, HIDE, extend=0.6)
    for p in pts[1:-1]:
        m.round_box(bone, p[0], p[2], t * 0.7, t * 0.7, p[1] - 1.0, p[1] + 1.0, STEEL, cut=1)


def build():
    m = Model("gargomon")
    top = m.bone("gargomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 24, 0))
    m.round_box(bd, 0, -2.0, 5.0, 6.0, 22.0, 32.0, HIDE, cut=2)
    for j in range(3):
        m.round_box(bd, 0, -2.0 + j * 3.6 - 3.0, 5.4, 1.0, 24.0, 30.0, STEEL, cut=0)
    m.round_box(bd, 0, -8.6, 2.6, 0.8, 26.0, 29.0, metal(P, "visor"), cut=0)
    hd = m.bone("head", bd, (0, 30, -8))
    m.round_box(hd, 0, -11.0, 2.4, 3.4, 28.0, 32.4, HIDE, cut=1)
    m.round_box(hd, 0, -12.0, 2.6, 2.0, 31.0, 33.0, solid(P, "visor"), cut=1)
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 32.4, -10.0), (sx * 0.4, 1, 0.6), 1.2, 4.0, HIDE, tip=0.8)
    for sx, nm, front in ((1, "leg_front_left", True), (-1, "leg_front_right", True), (1, "leg_back_left", False),
                          (-1, "leg_back_right", False)):
        z0 = -6.0 if front else 4.0
        lg = m.bone(nm, bd, (sx * 5.0, 26.0, z0))
        knee = (sx * 9.0, 18.0, z0 - 2.0)
        limb(m, lg, [(sx * 5.0, 27.0, z0), knee, (sx * 8.0, 6.0, z0 - 3.0), (sx * 8.0, 2.0, z0 - 4.0)], 3)
        m.round_box(lg, sx * 8.0, z0 - 5.0, 3.0, 3.4, 0.0, 4.0, HIDE, cut=1)
        m.round_box(lg, knee[0], knee[2], 2.0, 2.0, knee[1] - 1.2, knee[1] + 1.2, GOLD, cut=1)
        for j in range(3):
            spike(m, lg, (sx * 8.0 + (j - 1) * 1.6, 0.8, z0 - 8.0), (0, -0.2, -1), 1.0, 3.0, solid(P, "blue"), tip=0.8)
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 4.0, 32.0, 0))
        feather_wing(m, wb, (side * 4.0, 32.0, 0), 20.0, 8.0, 3, feathers(P, "white", "white_dark", size=(1.4, 2.6)),
                     side=side, sweep=10, droop=14.0)
    tb = m.bone("tail", bd, (0, 26, 6))
    pts = [(0, 26.0, 6.0), (4.0, 30.0, 12.0), (8.0, 34.0, 14.0), (12.0, 32.0, 10.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 1, solid(P, "blue"), extend=0.4, t2=2)
    return m
