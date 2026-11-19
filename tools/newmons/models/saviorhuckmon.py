"""Savior Huckmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the saviour knight: a slender dragon-man in gleaming silver-white armour with a horned
dragon helm and a cyan visor, a great fan of crimson blade-feathers sweeping from its back like a cape of fire, a long
red feathered tail, and a red energy sabre trailing a crimson arc. 25 blocks.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, feathers, metal, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a slender dragon-knight in silver-white armour with a horned helm, a great fan of crimson blade-feathers and a red energy sabre"
BASE = {"silver": (236, 238, 246), "silver_dark": (150, 156, 176), "red": (210, 30, 40), "red_dark": (120, 10, 16),
        "steel": (200, 204, 216), "visor": (90, 220, 250), "glow": (255, 80, 60, 210)}
SHINY = {"red": (60, 120, 230), "red_dark": (20, 50, 150), "glow": (90, 160, 255, 210)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "silver", "silver_dark", trim="red", trim_w=0.2)
FEATH = feathers(P, "red", "red_dark")


def build():
    m = Model("saviorhuckmon")
    mats = {"skin": PLATE, "talon": metal(P, "steel"), "claw": metal(P, "steel")}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.85, talons=True, claws=True, digitigrade=True,
                 name="saviorhuckmon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 2.6, 3.4, 54.0, 60.0, PLATE, cut=1)
    m.round_box(hd, 0, -4.4, 1.4, 1.2, 54.4, 57.0, PLATE, cut=0)
    m.box(hd, -1.8, 57.4, -4.5, 1.8, 58.2, -4.3, solid(P, "visor", glow=True))
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 60.0, 0), (sx * 0.4, 1, 0.8), 1.4, 7.0, PLATE, tip=0.8)
        spike(m, bd, (sx * 8.0, 50.0, 0), (sx * 1, 0.6, 0), 1.6, 5.0, PLATE, tip=0.8)
    wb = m.bone("feathers", bd, (0, 50, 4))                                              # fan of blade-feathers
    for sx in (-1, 1):
        for j in range(6):
            ang = math.radians(5 + j * 16)
            spike(m, wb, (sx * 3.0, 50.0, 4.0 + j * 0.3), (sx * math.cos(ang), math.sin(ang), 0.5), 2.0, 22.0 + j * 2.0,
                  FEATH, tip=0.8)
    tl = m.bone("tail", bd, (0, 32, 3))
    pts = [(0, 32.0, 3.0), (2.0, 20.0, 12.0), (4.0, 10.0, 22.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 2, PLATE, extend=0.4)
    for j in range(4):
        spike(m, tl, pts[-1], ((j - 1.5) * 0.3, -0.2, 1), 1.4, 7.0, FEATH, tip=0.8)
    w = a["arm_right"]["wrist"]                                                          # red energy sabre + arc
    m.box(a["arm_right"]["bone"], w[0] - 0.5, w[1] - 30.0, w[2] - 2.0, w[0] + 0.5, w[1] - 2.0, w[2] - 0.6,
          solid(P, "glow", glow=True), rotation=(-20, 0, 0), pivot=(w[0], w[1], w[2]))
    return m
