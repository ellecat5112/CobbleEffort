"""Locomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
steam locomotive: a big navy-blue steam engine with a riveted boiler, a round headlamp, a scowling face on its
smokebox front, a tall funnel puffing white steam, a cowcatcher, red-and-silver drive wheels with connecting rods and
a coal tender behind. 25 blocks long.

Front is -z, y is up. 30 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, slab_z
from _digidetail import armour, gem, metal, riveted, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(25, HEIGHT, 8.0)
KIND = "quadruped"
K = 3
LOOK = "a big navy-blue steam locomotive with a riveted boiler, a headlamp, a scowling face, a steaming funnel, a cowcatcher and red drive wheels"
BASE = {"navy": (50, 60, 110), "navy_dark": (18, 22, 50), "navy_light": (110, 120, 180), "silver": (200, 204, 216),
        "silver_dark": (90, 94, 106), "red": (200, 50, 40), "black": (30, 30, 34), "lamp": (255, 210, 120),
        "lamp_light": (255, 250, 220), "eye": (250, 220, 60), "steam": (240, 244, 250, 200), "brown": (110, 70, 40)}
SHINY = {"navy": (40, 110, 60), "navy_dark": (14, 50, 24), "navy_light": (110, 190, 130)}


def P(v):
    return pal(BASE, SHINY, v)


BOIL = riveted(P, "navy", "navy_dark", light="navy_light")
SIL = metal(P, "silver", dark="silver_dark")


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 2.0) < 0.8 and abs(y - 15.4 + sx * (x - sx * 2.0) * 0.3) < 0.4:
                return tone(p["eye"], face), p["eye"]
    return BOIL(x, y, z, face, variant, box=box, **k)


def wheel(m, bone, c, r):
    x, y, z = c
    for i in range(6):
        m.box(bone, x - 0.6, y - r, z - 0.6, x + 0.6, y + r, z + 0.6, solid(P, "red"), rotation=(i * 30.0, 0, 0), pivot=c)
    m.round_box(bone, x, z, 0.8, 0.8, y - 0.6, y + 0.6, SIL, cut=0)


def build():
    m = Model("locomon")
    top = m.bone("locomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0, 6.0, 16.0, 3.0, 7.0, armour(P, "black", "black"), cut=1)        # frame
    for i in range(6):                                                               # riveted boiler
        slab_z(m, bd, 0, 14.0, -16.0 + i * 4.0, -12.0 + i * 4.0 + 0.2, 5.4, 5.4, BOIL)
    m.round_box(bd, 0, -16.6, 5.0, 0.8, 9.0, 19.0, facef, cut=0)                       # smokebox face
    m.round_box(bd, 0, -17.6, 1.6, 0.8, 19.0, 22.0, gem(P, "lamp", "lamp_light"), cut=0)
    m.round_box(bd, 0, -10.0, 1.8, 1.8, 19.0, 26.0, SIL, cut=1)                         # funnel
    ball(m, bd, (2.0, 30.0, -6.0), 3.4, solid(P, "steam"), layers=3)
    ball(m, bd, (5.0, 33.0, 1.0), 4.0, solid(P, "steam"), layers=3)
    for j in range(5):                                                               # cowcatcher
        rod(m, bd, ((j - 2) * 2.0, 6.0, -17.0), ((j - 2) * 2.4, 1.0, -21.0), 1, SIL, extend=0, t2=1)
    m.round_box(bd, 0, 8.0, 5.4, 4.0, 7.0, 20.0, armour(P, "navy", "navy_dark"), cut=1)      # cab
    for sx in (-1, 1):                                                               # drive wheels + rods
        lg = m.bone("leg_left" if sx > 0 else "leg_right", top, (sx * 6.0, 4.0, 0))
        for k_, zc in enumerate((-10.0, -3.0, 4.0)):
            wheel(m, lg, (sx * 6.4, 4.0, zc), 3.8)
        rod(m, lg, (sx * 7.4, 4.0, -10.0), (sx * 7.4, 4.0, 4.0), 1, SIL, extend=0, t2=1)
    tb = m.bone("tender", bd, (0, 8, 22))                                            # coal tender
    m.round_box(tb, 0, 26.0, 5.6, 5.0, 2.0, 12.0, armour(P, "navy", "navy_dark"), cut=1)
    m.round_box(tb, 0, 26.0, 5.0, 4.4, 12.0, 13.6, solid(P, "black"), cut=1)
    return m
