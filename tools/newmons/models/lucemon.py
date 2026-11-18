"""Lucemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
angel child: a small boyish angel with fluffy blond hair, blue eyes, a white wrap-robe with a pale violet cross sash,
gold armlets and anklets, bare feet, and six pairs of white feathered wings spread round him like a star. Child stage,
1 block tall.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digidetail import fabric, feathers, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 3.0)
KIND = "floater"
K = 4
LOOK = "a small boyish angel with fluffy blond hair, a white wrap-robe, gold armlets and six pairs of white feathered wings"
BASE = {"white": (248, 248, 252), "white_dark": (190, 190, 210), "skin": (250, 226, 210), "skin_dark": (210, 170, 150),
        "hair": (250, 220, 120), "hair_dark": (200, 160, 60), "violet": (180, 150, 210), "gold": (240, 200, 70),
        "gold_dark": (160, 120, 20), "eye": (60, 130, 230)}
SHINY = {"hair": (230, 230, 240), "hair_dark": (170, 170, 190), "white": (250, 236, 210), "white_dark": (210, 190, 150)}


def P(v):
    return pal(BASE, SHINY, v)


SK = skin(P, "skin", dark="skin_dark")
ROBE = fabric(P, "white", "white_dark")


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 1.2, y - 21.4) < 0.6:
                return tone(p["eye"], face), None
    return SK(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("lucemon")
    top = m.bone("lucemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 0, 2.6, 2.0, 8.0, 17.4, ROBE, cut=1)
    m.round_box(bd, 0, -2.1, 0.6, 0.2, 9.0, 17.0, solid(P, "violet"), cut=0)
    hd = m.bone("head", bd, (0, 17, 0))
    m.round_box(hd, 0, 0, 2.6, 2.4, 17.4, 23.4, facef, cut=1)
    for i in range(11):                                                              # fluffy blond hair
        ang = math.radians(-110 + i * 22)
        spike(m, hd, (2.2 * math.sin(ang), 22.6, 0.6 + 1.4 * math.cos(ang)), (math.sin(ang) * 0.8, 0.6, 0.4), 1.6, 2.6,
              strands(P, "hair", "hair_dark"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 2.6, 16.0, 0))
        rod(m, ab, (sx * 2.6, 16.0, 0), (sx * 4.0, 11.6, -0.6), 1, SK, extend=0.3, t2=1)
        m.round_box(ab, sx * 3.6, -0.4, 0.8, 0.8, 13.0, 13.8, metal(P, "gold", dark="gold_dark"), cut=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.2, 8.0, 0))
        rod(m, lg, (sx * 1.2, 8.4, 0), (sx * 1.4, 1.0, 0), 1, SK, extend=0.3, t2=1)
        m.round_box(lg, sx * 1.4, 0, 0.8, 0.8, 2.0, 2.8, metal(P, "gold", dark="gold_dark"), cut=0)
    for side in (1, -1):                                                             # six pairs of wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 1.6, 15.0, 2.0))
        for j, (dr, sw) in enumerate(((10, 40), (-6, 10), (-24, -20))):
            feather_wing(m, wb, (side * 1.6, 15.0, 2.0 + j * 0.4), 10.0 - j, 4.0, 1, feathers(P, "white", "white_dark"),
                         side=side, sweep=sw, droop=dr)
    return m
