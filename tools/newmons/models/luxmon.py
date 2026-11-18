"""Luxmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
little blindfolded angel: a slim figure in a white zip-up bodysuit with gold trim, shaggy blond hair, a white
blindfold, a fang grin, a brown-and-white striped helmet with little white wings, big violet gloves, white
feathered wings at its back and big bronze riveted shoes. Child stage, 1 block tall.

Front is -z, y is up. 32 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digidetail import fabric, feathers, leather, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 32
SCALE, HITBOX = sized(1.0, HEIGHT, 2.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a slim blindfolded angel in a white bodysuit with blond hair, a striped winged helmet, big violet gloves, white wings and bronze shoes"
BASE = {"white": (248, 248, 252), "white_dark": (190, 190, 210), "gold": (230, 190, 70), "hair": (250, 220, 120),
        "hair_dark": (200, 160, 60), "brown": (150, 110, 70), "brown_dark": (90, 60, 30), "violet": (180, 90, 200),
        "violet_dark": (110, 40, 130), "bronze": (190, 150, 90), "bronze_dark": (120, 90, 40), "skin": (250, 226, 210),
        "skin_dark": (210, 170, 150), "tooth": (250, 250, 250)}
SHINY = {"violet": (90, 170, 230), "violet_dark": (30, 100, 170), "brown": (60, 60, 70), "brown_dark": (24, 24, 30)}


def P(v):
    return pal(BASE, SHINY, v)


SUIT = fabric(P, "white", "white_dark")


def helmf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["white"] if abs(x) < 0.8 else p["brown"], face), None


def build():
    m = Model("luxmon")
    top = m.bone("luxmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0, 2.4, 1.8, 9.0, 18.0, SUIT, cut=1)
    m.round_box(bd, 0, -1.9, 0.4, 0.2, 10.0, 18.0, solid(P, "gold"), cut=0)
    hd = m.bone("head", bd, (0, 18, 0))
    m.round_box(hd, 0, 0, 2.6, 2.4, 18.0, 24.0, skin(P, "skin", dark="skin_dark"), cut=1)
    m.round_box(hd, 0, 0, 2.8, 2.6, 21.0, 22.4, solid(P, "white"), cut=1)                    # blindfold
    spike(m, hd, (0.8, 19.2, -2.4), (0, -1, -0.2), 0.8, 1.2, solid(P, "tooth"), tip=0.8)
    for i in range(9):                                                               # shaggy blond hair
        ang = math.radians(-100 + i * 25)
        spike(m, hd, (2.4 * math.sin(ang), 22.0, 0.6 + 1.2 * math.cos(ang)), (math.sin(ang) * 0.6, -1, 0.3), 1.4, 4.0,
              strands(P, "hair", "hair_dark"), tip=0.8)
    m.round_box(hd, 0, 0.2, 3.2, 3.0, 22.4, 26.6, helmf, cut=2)                          # striped helmet
    for sx in (-1, 1):
        spike(m, hd, (sx * 3.0, 25.0, 0.4), (sx, 0.6, 0.4), 1.2, 3.6, feathers(P, "white", "white_dark"), tip=0.8)
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 1.6, 16.0, 1.8))
        feather_wing(m, wb, (side * 1.6, 16.0, 1.8), 8.0, 4.0, 1, feathers(P, "hair", "white"), side=side, sweep=20, droop=6.0)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # big violet gloves
        ab = m.bone(nm, bd, (sx * 2.4, 17.0, 0))
        rod(m, ab, (sx * 2.4, 17.0, 0), (sx * 4.6, 12.6, -1.0), 1, SUIT, extend=0.3, t2=1)
        m.round_box(ab, sx * 5.4, -1.0, 1.8, 1.6, 9.6, 12.8, leather(P, "violet", "violet_dark"), cut=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                              # bronze shoes
        lg = m.bone(nm, top, (sx * 1.2, 9.0, 0))
        rod(m, lg, (sx * 1.2, 9.4, 0), (sx * 1.6, 2.4, 0), 1, SUIT, extend=0.3, t2=1)
        m.round_box(lg, sx * 1.8, -1.2, 1.8, 3.0, 0.0, 2.4, metal(P, "bronze", dark="bronze_dark"), cut=1)
    return m
