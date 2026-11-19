"""Zudomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the hammer walrus: a hulking blue-grey beast-man with a shaggy orange-brown mane and beard, long
ivory tusks and a single horn, a huge green spiked turtle shell on its back held by leather straps, a giant steel
hammer, clawed hands and feet, and a flowing red tail tuft. 25 blocks.

Front is -z, y is up. 60 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, fur, leather, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 63
SCALE, HITBOX = sized(25, HEIGHT, 8.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a hulking blue-grey walrus beast-man with an orange mane, ivory tusks and a horn, a green spiked shell and a giant steel hammer"
BASE = {"grey": (130, 150, 180), "grey_dark": (60, 76, 110), "orange": (220, 130, 60), "orange_dark": (150, 70, 20),
        "ivory": (246, 240, 220), "green": (70, 120, 80), "green_dark": (24, 60, 30), "leather": (120, 80, 50),
        "steel": (200, 204, 216), "steel_dark": (100, 104, 116), "red": (220, 60, 40), "eye": (250, 220, 60),
        "claw": (240, 236, 220)}
SHINY = {"grey": (190, 160, 200), "grey_dark": (120, 90, 140), "green": (130, 90, 50), "green_dark": (70, 40, 20)}


def P(v):
    return pal(BASE, SHINY, v)


GREY = skin(P, "grey", dark="grey_dark")
MANE = fur(P, "orange", "orange_dark", length=2.0)


def build():
    m = Model("zudomon")
    mats = {"skin": GREY, "chest": GREY, "abs": GREY, "pelvis": leather(P, "leather", "orange_dark"), "deltoid": MANE,
            "upper_arm": GREY, "forearm": GREY, "hand": GREY, "finger": GREY, "claw": solid(P, "claw"), "thigh": MANE,
            "knee": GREY, "shin": GREY, "calf": GREY, "foot": GREY, "talon": solid(P, "claw"), "neck": MANE}
    a = humanoid(m, mats, bulk=1.6, arm_bulk=1.5, leg_bulk=1.4, claws=True, talons=True, name="zudomon")
    bd = a["body"]
    ball(m, bd, (0, 44.0, 6.0), 10.0, armour(P, "green", "green_dark", panel=(4.0, 4.0)), layers=4, squash=0.7)  # shell
    for i in range(7):
        ang = (i - 3) * 0.45
        spike(m, bd, (math.sin(ang) * 7.0, 50.0 - abs(i - 3) * 2.0, 10.0), (math.sin(ang) * 0.6, 0.6, 1), 2.6, 8.0,
              armour(P, "green", "green_dark"), tip=0.8)
    for sx in (-1, 1):
        rod(m, bd, (sx * 6.0, 52.0, -4.6), (-sx * 4.0, 32.0, -5.0), 1, leather(P, "leather", "orange_dark"), extend=0.0)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 3.6, 4.0, 53.0, 60.0, MANE, cut=2)
    m.round_box(hd, 0, -4.6, 2.6, 1.6, 53.6, 57.6, GREY, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.6), 57.4, -5.6, max(sx * 1.0, sx * 2.6), 58.2, -5.2, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 1.6, 54.0, -5.8), (sx * 0.2, -1, -0.3), 1.2, 7.0, solid(P, "ivory"), tip=0.8)
    spike(m, hd, (0, 59.6, -3.0), (0, 0.6, -1), 1.6, 9.0, solid(P, "ivory"), tip=0.8)
    for j in range(5):
        spike(m, hd, ((j - 2) * 1.2, 53.4, -4.0), ((j - 2) * 0.2, -1, -0.3), 1.2, 4.0, MANE, tip=0.8)
    h = a["arm_right"]["hand"]                                                          # giant hammer
    rb = a["arm_right"]["bone"]
    rod(m, rb, (h[0], h[1] - 4.0, h[2]), (h[0], h[1] + 16.0, h[2]), 1, leather(P, "leather", "orange_dark"), extend=0.0)
    m.round_box(rb, h[0], h[2], 3.6, 5.6, h[1] + 14.0, h[1] + 22.0, metal(P, "steel", dark="steel_dark"), cut=1)
    tl = m.bone("tail", bd, (0, 30, 6))
    for j in range(4):
        spike(m, tl, (0, 30.0, 6.0), ((j - 1.5) * 0.4, -0.3, 1), 1.6, 10.0, strands(P, "red", "orange_dark"), tip=0.8)
    return m
