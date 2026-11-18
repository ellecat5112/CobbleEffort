"""Mametyramon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
tiny dinosaur in a helmet: a small orange dinosaur wearing a big round steel helmet with a fanged visor mouth and green
fins, one blue eye peeking out, spiked steel bracelets, huge silver claws on its arms and feet, bandaged ankles and a
short orange tail with a green fin. 25 blocks tall.

Front is -z, y is up. 24 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, fabric, metal, skin, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(25, HEIGHT, 3.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 8}
LOOK = "a small orange dinosaur in a big round steel helmet with a fanged visor and green fins, spiked bracelets and huge silver claws"
BASE = {"orange": (240, 110, 40), "orange_dark": (160, 50, 14), "steel": (150, 154, 166), "steel_dark": (70, 74, 86),
        "steel_light": (210, 214, 224), "green": (40, 150, 70), "silver": (230, 232, 240), "silver_dark": (120, 126, 140),
        "eye": (60, 150, 230), "tooth": (250, 250, 246), "bandage": (236, 230, 216), "black": (30, 30, 34)}
SHINY = {"orange": (120, 180, 240), "orange_dark": (40, 100, 180)}


def P(v):
    return pal(BASE, SHINY, v)


SK = skin(P, "orange", dark="orange_dark")
HELM = metal(P, "steel", dark="steel_dark", light="steel_light")
SIL = metal(P, "silver", dark="silver_dark")


def build():
    m = Model("mametyramon")
    top = m.bone("mametyramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0.6, 3.6, 3.4, 5.0, 12.0, SK, cut=1)
    hd = m.bone("head", bd, (0, 12, -1))
    m.round_box(hd, 0, -1.0, 5.4, 5.4, 11.0, 21.0, HELM, cut=3)                        # big round helmet
    m.round_box(hd, 0, -6.4, 4.0, 0.8, 12.0, 15.0, solid(P, "black"), cut=0)
    for j in range(7):                                                               # fanged visor
        spike(m, hd, (-3.0 + j, 15.0, -6.6), (0, -1, 0), 0.8, 1.6, solid(P, "tooth"), tip=0.8)
        spike(m, hd, (-3.0 + j, 12.0, -6.6), (0, 1, 0), 0.8, 1.4, solid(P, "tooth"), tip=0.8)
    m.round_box(hd, 2.6, -6.6, 1.0, 0.3, 17.0, 18.6, solid(P, "eye"), cut=0)
    for j in range(3):                                                               # green fins
        spike(m, hd, (0, 21.0 - j * 1.6, -1.0 + j * 2.6), (0, 1, 0.5), 1.4, 3.0, solid(P, "green"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.6, 10.0, 0))
        rod(m, ab, (sx * 3.6, 10.0, 0), (sx * 6.0, 8.0, -2.0), 2, SK, extend=0.4)
        m.round_box(ab, sx * 6.0, -2.0, 2.0, 2.0, 7.0, 9.0, HELM, cut=1)
        for j in range(4):
            spike(m, ab, (sx * 6.0, 8.0, -2.0), (sx * 0.6, 0.8 - j * 0.5, 0), 0.8, 1.6, HELM, tip=0.8)
            spike(m, ab, (sx * 7.0 + (j - 1.5) * 0.6, 7.0, -3.0), (sx * 0.4, -0.3, -1), 0.9, 4.0, SIL, tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.2, 6.0, 0))
        rod(m, lg, (sx * 2.2, 6.4, 0), (sx * 2.6, 2.0, 0), 2, SK, extend=0.4)
        m.round_box(lg, sx * 2.6, 0, 1.4, 1.4, 2.0, 3.4, fabric(P, "bandage", "steel_dark"), cut=0)
        for j in range(3):
            spike(m, lg, (sx * 2.6 + (j - 1) * 0.9, 0.8, -1.4), (0, -0.2, -1), 0.9, 3.0, SIL, tip=0.8)
    tb = m.bone("tail", bd, (0, 7, 3))
    rod(m, tb, (0, 7.0, 3.0), (0, 9.0, 8.0), 2, SK, extend=0.4)
    spike(m, tb, (0, 9.0, 8.0), (0, 1, 0.6), 1.2, 2.4, solid(P, "green"), tip=0.8)
    return m
