"""Jijimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
village elder: a tiny old Digimon almost hidden under a great shaggy mop of white hair, a tattered brown loincloth,
big bare pink feet, little hands and a wooden staff topped with a giant yellow paw with grey pads. 35 blocks tall.

Front is -z, y is up. 30 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, fur, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(35, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a tiny old elder under a great shaggy mop of white hair with big bare feet and a staff topped by a giant yellow paw"
BASE = {"white": (246, 246, 246), "white_dark": (180, 180, 186), "skin": (250, 210, 190), "skin_dark": (200, 150, 130),
        "brown": (170, 130, 80), "brown_dark": (100, 70, 40), "yellow": (250, 210, 60), "yellow_dark": (200, 150, 20),
        "pad": (80, 80, 90), "wood": (140, 100, 60), "wood_dark": (80, 50, 24), "nose": (230, 150, 140)}
SHINY = {"white": (200, 210, 250), "white_dark": (130, 140, 200), "yellow": (240, 140, 200), "yellow_dark": (180, 70, 140)}


def P(v):
    return pal(BASE, SHINY, v)


HAIR = fur(P, "white", "white_dark", length=2.4)
SKIN = skin(P, "skin", dark="skin_dark")


def build():
    m = Model("jijimon")
    top = m.bone("jijimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 4.0, 3.4, 5.0, 11.0, fabric(P, "brown", "brown_dark"), cut=1)
    for i in range(7):                                                               # tattered loincloth hem
        ang = math.radians(-90 + i * 30)
        spike(m, bd, (3.6 * math.sin(ang), 5.4, -3.0 * math.cos(ang)), (math.sin(ang) * 0.3, -1, -math.cos(ang) * 0.3),
              1.6, 2.4, fabric(P, "brown", "brown_dark"), tip=0.8)
    hd = m.bone("head", bd, (0, 12, 0))
    ball(m, hd, (0, 18.0, 0.6), 8.0, HAIR, layers=6, squash=1.0)                        # great mop of hair
    for i in range(14):
        ang = 2 * math.pi * i / 14
        spike(m, hd, (7.0 * math.cos(ang), 18.0 + 7.0 * math.sin(ang), 0.6), (math.cos(ang), math.sin(ang), 0.2), 2.4,
              3.4, HAIR, tip=0.8)
    m.round_box(hd, 0, -7.6, 1.0, 0.8, 14.0, 15.6, solid(P, "nose"), cut=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                              # big bare feet
        lg = m.bone(nm, top, (sx * 2.0, 5.0, 0))
        rod(m, lg, (sx * 2.0, 5.4, 0), (sx * 2.6, 2.0, -0.6), 1, SKIN, extend=0.3, t2=2)
        m.round_box(lg, sx * 3.0, -2.0, 2.6, 4.0, 0.0, 2.4, SKIN, cut=1)
        for j in range(4):
            m.round_box(lg, sx * 3.0 + (j - 1.5) * 1.2, -6.2, 0.6, 0.4, 0.0, 1.4, SKIN, cut=0)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 6.0, 12.0, -4.0))
        m.round_box(ab, sx * 6.4, -5.0, 1.2, 1.2, 10.4, 12.6, SKIN, cut=0)
    ab = "arm_right"                                                                 # the paw staff
    rod(m, ab, (-6.4, 2.0, -5.4), (-8.0, 24.0, -6.0), 1, solid(P, "wood"), extend=0, t2=1)
    ball(m, ab, (-8.4, 27.0, -6.4), 3.6, skin(P, "yellow", dark="yellow_dark"), layers=3)
    m.round_box(ab, -8.4, -9.8, 1.4, 0.4, 25.4, 27.6, solid(P, "pad"), cut=0)
    for j in range(4):
        ang = math.radians(-60 + j * 40)
        m.round_box(ab, -8.4 + 3.0 * math.sin(ang), -9.6, 0.7, 0.4, 28.4 + 2.0 * math.cos(ang),
                    29.8 + 2.0 * math.cos(ang), solid(P, "pad"), cut=0)
    return m
