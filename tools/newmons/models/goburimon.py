"""Goburimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
goblin: a hunched green imp with a red mohawk, pointed ears, a big-toothed grin, a studded leather collar and a torn
brown vest, swinging a wooden club studded with bolts. Child stage, 1 block tall.

Front is -z, y is up. 32 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fabric, leather, metal, skin, solid, strands, twisted
from _route import pal, tone

HEIGHT = 32
SCALE, HITBOX = sized(1.0, HEIGHT, 1.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 12}
LOOK = "a hunched green goblin with a red mohawk, pointed ears, a toothy grin, a studded collar and a bolt-studded wooden club"
BASE = {"green": (90, 180, 60), "green_dark": (40, 110, 20), "red": (220, 40, 40), "red_dark": (140, 14, 18),
        "vest": (150, 100, 60), "vest_dark": (90, 56, 24), "black": (36, 32, 36), "steel": (200, 204, 214),
        "steel_dark": (100, 104, 116), "wood": (140, 90, 50), "wood_dark": (90, 56, 24), "eye": (250, 220, 60),
        "tooth": (250, 250, 240), "mouth": (100, 20, 30), "claw": (240, 236, 220)}
SHINY = {"green": (120, 130, 200), "green_dark": (60, 70, 140)}


def P(v):
    return pal(BASE, SHINY, v)


SK = skin(P, "green", dark="green_dark")


def build():
    m = Model("goburimon")
    top = m.bone("goburimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0.4, 3.6, 3.0, 9.0, 18.0, fabric(P, "vest", "vest_dark"), cut=1)
    m.round_box(bd, 0, -0.2, 2.6, 2.4, 9.0, 17.6, SK, cut=1)
    m.round_box(bd, 0, 0.4, 3.2, 3.0, 17.4, 18.8, leather(P, "black", "black", stitch="steel"), cut=1)   # studded collar
    hd = m.bone("head", bd, (0, 19, -1))
    m.round_box(hd, 0, -1.6, 3.4, 3.2, 18.4, 25.0, SK, cut=2)
    m.box(hd, -2.4, 19.4, -4.9, 2.4, 20.8, -4.6, solid(P, "mouth"))
    for j in range(5):
        m.box(hd, -2.2 + j * 0.95, 20.0, -5.0, -1.6 + j * 0.95, 20.8, -4.8, solid(P, "tooth"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.0), 22.6, -4.9, max(sx * 0.8, sx * 2.0), 23.4, -4.7, solid(P, "eye"))
        spike(m, hd, (sx * 3.2, 22.6, -1.0), (sx, 0.3, 0.3), 1.4, 4.0, SK, tip=0.8)          # pointed ears
    for j in range(6):                                                                      # red mohawk
        spike(m, hd, (0, 24.6, -3.0 + j * 1.0), (0, 1, 0.3), 1.0, 3.6, strands(P, "red", "red_dark"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.4, 17.0, -1.0))
        rod(m, ab, (sx * 3.4, 17.0, -1.0), (sx * 6.0, 12.0, -3.0), 2, SK, extend=0.4)
        m.round_box(ab, sx * 6.4, -3.4, 1.8, 1.8, 9.0, 12.0, SK, cut=1)
    ar = "arm_right"                                                                          # bolt-studded club
    rod(m, ar, (-6.4, 11.0, -4.0), (-4.0, 26.0, -6.0), 2, twisted(P, "wood", "wood_dark"), extend=0, t2=3)
    m.round_box(ar, -3.6, -6.4, 2.2, 2.2, 23.0, 29.0, twisted(P, "wood", "wood_dark"), cut=1)
    for j in range(3):
        spike(m, ar, (-3.6 + (j - 1) * 1.2, 26.0 + j, -8.6), (0, 0, -1), 0.8, 1.0, metal(P, "steel", dark="steel_dark"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.0, 10.0, 0))
        rod(m, lg, (sx * 2.0, 10.0, 0), (sx * 2.6, 2.0, -0.6), 2, SK, extend=0.4)
        m.round_box(lg, sx * 2.6, -1.4, 1.6, 2.2, 0.0, 1.8, SK, cut=1)
        for j in range(2):
            spike(m, lg, (sx * 2.6 + (j - 0.5) * 1.2, 0.5, -3.6), (0, -0.2, -1), 0.7, 1.2, solid(P, "claw"))
    return m
