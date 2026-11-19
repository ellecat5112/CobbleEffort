"""Peckmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the ninja bird: a fiery-crested bird-man in a violet ninja suit and black mask, a long yellow scarf
streaming behind, a blade strapped across its back, a wild red-orange crest of flame-like feathers and big yellow
taloned feet. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fabric, feathers, metal, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a fiery-crested ninja bird-man in a violet suit and black mask, a long yellow scarf, a blade on its back and yellow talons"
BASE = {"violet": (90, 60, 150), "violet_dark": (40, 24, 80), "black": (30, 28, 34), "yellow": (250, 210, 50),
        "yellow_dark": (190, 140, 20), "red": (230, 70, 40), "orange": (250, 150, 50), "beak": (240, 190, 60),
        "steel": (210, 214, 226), "eye": (250, 250, 250)}
SHINY = {"violet": (40, 110, 80), "violet_dark": (14, 60, 40), "red": (80, 150, 240), "orange": (160, 210, 250)}


def P(v):
    return pal(BASE, SHINY, v)


SUIT = fabric(P, "violet", "violet_dark")


def build():
    m = Model("peckmon")
    mats = {"skin": SUIT, "neck": solid(P, "black"), "hand": feathers(P, "orange", "red"),
            "finger": solid(P, "orange"), "foot": solid(P, "yellow"), "toe": solid(P, "yellow"),
            "talon": solid(P, "yellow_dark"), "shin": solid(P, "yellow"), "calf": solid(P, "yellow")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.8, leg_bulk=0.9, talons=True, digitigrade=True, name="peckmon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.6, 54.0, 59.4, feathers(P, "orange", "red"), cut=1)
    m.box(hd, -2.5, 56.6, -2.9, 2.5, 58.4, -2.7, solid(P, "black"))                        # black mask
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.6), 57.2, -2.95, max(sx * 0.6, sx * 1.6), 57.8, -2.9, solid(P, "eye"))
    spike(m, hd, (0, 56.0, -2.8), (0, -0.4, -1), 1.4, 4.0, solid(P, "beak"), tip=0.8)
    for i in range(8):                                                                   # flame crest
        ang = math.radians(-30 + i * 12)
        spike(m, hd, (0, 59.0, 0), (0, math.cos(ang), math.sin(ang) + 0.4), 1.6, 8.0 - abs(i - 3) * 0.8,
              solid(P, "red" if i % 2 else "orange"), tip=0.8)
    for j in range(5):                                                                   # yellow scarf
        m.box(bd, -2.0 - j * 0.5, 50.0 - j * 0.4, 3.0 + j * 3.0, 2.0 + j * 0.5, 52.0 - j * 0.4, 6.0 + j * 3.0,
              fabric(P, "yellow", "yellow_dark"), rotation=(-10, 0, 0), pivot=(0, 51.0, 3.0 + j * 3.0))
    rod(m, bd, (-6.0, 34.0, 4.0), (6.0, 54.0, 4.0), 1, metal(P, "steel"), extend=0.2, t2=2)   # blade on its back
    return m
