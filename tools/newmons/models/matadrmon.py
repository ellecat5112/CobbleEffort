"""Matadrmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
undead matador: a gaunt figure in a red suit patterned with black, a skull face with a long beak-like nose and a
crest of yellow-orange spikes, a flowing pink cape bristling with long silver blades, a green cravat, red-soled
shoes and a long thin rapier. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import fabric, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a gaunt undead matador in a black-patterned red suit with a skull face, a spiky crest, a pink cape bristling with blades and a rapier"
BASE = {"red": (200, 40, 40), "red_dark": (110, 14, 18), "black": (30, 28, 30), "pink": (230, 90, 140), "pink_dark": (150, 40, 90),
        "bone": (230, 226, 206), "bone_dark": (160, 150, 120), "yellow": (250, 200, 50), "orange": (240, 120, 40),
        "green": (90, 200, 90), "silver": (220, 224, 234), "silver_dark": (110, 114, 126), "eye": (240, 40, 40)}
SHINY = {"red": (40, 60, 160), "red_dark": (14, 20, 80), "pink": (240, 200, 80), "pink_dark": (170, 130, 20)}


def P(v):
    return pal(BASE, SHINY, v)


def suitf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "south") and abs(math.hypot(x, (y % 8.0) - 4.0) - 2.0) < 0.4:
        return tone(p["black"], face), None
    return fabric(P, "red", "red_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("matadrmon")
    mats = {"skin": suitf, "chest": suitf, "abs": suitf, "pelvis": suitf, "neck": skin(P, "bone", dark="bone_dark"),
            "deltoid": suitf, "upper_arm": suitf, "forearm": suitf, "hand": skin(P, "bone", dark="bone_dark"),
            "finger": skin(P, "bone", dark="bone_dark"), "thigh": suitf, "knee": suitf, "shin": suitf, "calf": suitf,
            "foot": solid(P, "black"), "toe": solid(P, "red")}
    a = humanoid(m, mats, bulk=0.78, arm_bulk=0.8, leg_bulk=0.82, name="matadrmon")
    bd = a["body"]
    m.round_box(bd, 0, -3.2, 1.4, 0.6, 48.0, 51.0, solid(P, "green"), cut=0)                   # cravat
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 60.4, skin(P, "bone", dark="bone_dark"), cut=1)
    spike(m, hd, (0, 57.0, -2.6), (0, -0.3, -1), 1.2, 6.0, skin(P, "bone", dark="bone_dark"), tip=0.8)   # long nose
    m.box(hd, -1.6, 58.0, -2.9, -0.6, 58.8, -2.8, solid(P, "eye", glow=True))
    m.box(hd, 0.6, 58.0, -2.9, 1.6, 58.8, -2.8, solid(P, "eye", glow=True))
    for i in range(7):                                                               # spiky crest
        spike(m, hd, ((i - 3) * 0.6, 60.0, 0.4), ((i - 3) * 0.25, 1, 0.4), 1.2, 6.0 - abs(i - 3) * 0.6,
              strands(P, "yellow", "orange"), tip=0.8)
    cape(m, bd, 53.0, 16.0, 44.0, fabric(P, "pink", "pink_dark"), z=4.0, flare=1.0, panels=8, sweep=(8.0, 2.0))
    for j in range(8):                                                               # silver blades in the cape
        spike(m, bd, (-6.0 + j * 1.8, 30.0 - j * 1.4, 6.0), ((j - 3.5) * 0.12, -1, 0.3), 0.8, 18.0,
              metal(P, "silver", dark="silver_dark"), tip=0.8)
    hr = a["arm_right"]                                                              # long rapier
    hx, hy, hz = hr["hand"]
    rod(m, hr["bone"], (hx, hy, hz), (hx - 18.0, hy - 16.0, hz - 6.0), 1, metal(P, "silver", dark="silver_dark"), extend=0, t2=1)
    return m
