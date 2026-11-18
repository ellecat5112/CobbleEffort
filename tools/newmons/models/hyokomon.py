"""Hyokomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
chick samurai: a round yellow chick with stubby wings, an orange beak, a red brush-like topknot crest, a white
headband, a little straw-sandalled pair of feet and a short katana slung at its side. Child stage, 1 block tall.

Front is -z, y is up. 20 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import feathers, metal, solid, strands
from _route import pal, tone

HEIGHT = 20
SCALE, HITBOX = sized(1.0, HEIGHT, 1.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 12}
LOOK = "a round yellow chick samurai with a red brush topknot, a white headband, an orange beak and a short katana"
BASE = {"yellow": (250, 220, 70), "yellow_dark": (200, 160, 20), "orange": (240, 140, 40), "red": (220, 50, 40),
        "red_dark": (140, 20, 14), "white": (250, 250, 250), "eye": (20, 20, 24), "shine": (255, 255, 255),
        "steel": (220, 224, 232), "steel_dark": (110, 114, 126), "hilt": (60, 40, 30), "straw": (220, 190, 120)}
SHINY = {"yellow": (240, 240, 246), "yellow_dark": (170, 172, 190), "red": (60, 90, 220), "red_dark": (20, 40, 140)}


def P(v):
    return pal(BASE, SHINY, v)


FEATH = feathers(P, "yellow", "yellow_dark", size=(1.0, 1.6))


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.0, y - 11.0)
            if d < 0.35:
                return tone(p["shine"], face), None
            if d < 1.0:
                return tone(p["eye"], face), None
    if 13.6 < y < 14.8:
        return tone(p["white"], face), None                                     # headband
    return FEATH(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("hyokomon")
    top = m.bone("hyokomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    ball(m, bd, (0, 9.6, 0), 6.0, bodyf, layers=5)
    hd = m.bone("head", bd, (0, 14, 0))
    spike(m, hd, (0, 9.4, -5.6), (0, -0.2, -1), 1.8, 2.6, solid(P, "orange"), tip=0.8)
    for i in range(5):                                                              # red brush topknot
        spike(m, hd, (0, 15.0, -0.6 + i * 0.6), ((i - 2) * 0.15, 1, 0.4 + i * 0.2), 1.4, 4.0 - abs(i - 2) * 0.4,
              strands(P, "red", "red_dark"), tip=0.8)
    for sx in (-1, 1):
        spike(m, hd, (0, 14.2, 5.4), (sx * 0.4, -0.6, 1), 0.8, 2.6, solid(P, "white"), tip=0.8)   # headband tails
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                             # stubby wings
        ab = m.bone(nm, bd, (sx * 5.6, 10.0, 0))
        spike(m, ab, (sx * 5.6, 10.0, 0), (sx, -0.6, 0.2), 2.0, 3.4, FEATH, tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.0, 4.0, 0))
        rod(m, lg, (sx * 2.0, 4.6, 0), (sx * 2.2, 1.0, 0), 1, solid(P, "orange"), extend=0.3)
        m.round_box(lg, sx * 2.2, -1.0, 1.4, 2.0, 0.0, 0.8, solid(P, "straw"), cut=0)
    rod(m, bd, (-4.6, 6.0, 1.6), (-2.6, 10.0, 6.0), 1, solid(P, "hilt"), extend=0, t2=1)         # katana at its side
    rod(m, bd, (-5.4, 4.4, -0.4), (-4.6, 6.0, 1.6), 1, metal(P, "steel", dark="steel_dark"), extend=0, t2=1)
    return m
