"""Darcmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the warrior angel. A slender angel with long blonde hair under a red hood and a silver winged
circlet, a gold breastplate over a red tunic with a long blue-and-gold diamond-patterned tabard, gold gauntlets and
tall gold boots, four pale feathered wings, a staff topped with a gold emblem in one hand and a sword in the other.
Its official design is kept as drawn. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digibody import humanoid
from _digidetail import armour, fabric, feathers, local, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a slender warrior angel with long blonde hair under a red hood, a gold breastplate, a blue diamond-patterned "
        "tabard, tall gold boots, four pale wings, a staff and a sword")
BASE = {"skin": (246, 220, 200), "skin_dark": (200, 170, 150), "hair": (250, 220, 120), "hair_dark": (210, 170, 60),
        "red": (200, 40, 40), "red_dark": (120, 14, 18), "gold": (236, 190, 60), "gold_dark": (160, 110, 20),
        "blue": (40, 60, 150), "blue_dark": (16, 24, 80), "white": (246, 246, 250), "wing": (250, 246, 220),
        "wing_dark": (210, 200, 160), "steel": (210, 214, 226), "steel_dark": (110, 114, 128), "brown": (130, 90, 50),
        "eye": (60, 120, 200)}
SHINY = {"red": (60, 140, 220), "red_dark": (20, 70, 150), "hair": (240, 240, 250), "hair_dark": (190, 190, 210)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark")
TUNIC = fabric(P, "red", "red_dark", axis="y", period=2.0)


def tabardf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if abs(((u - W / 2) * 0.8) % 2.4 - 1.2) + abs((v * 0.6) % 2.4 - 1.2) < 0.7:
        return tone(p["gold"], face), None
    return tone(p["blue"] if u > 0.5 and u < W - 0.5 else p["red"], face), None


def build():
    m = Model("darcmon")
    S = skin(P, "skin", dark="skin_dark")
    mats = {"skin": S, "chest": GOLD, "abs": TUNIC, "pelvis": TUNIC, "deltoid": TUNIC, "upper_arm": TUNIC,
            "forearm": GOLD, "hand": GOLD, "finger": GOLD, "thigh": TUNIC, "knee": GOLD, "shin": GOLD, "calf": GOLD,
            "foot": GOLD, "toe": GOLD}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.9, name="darcmon")
    bd = a["body"]
    m.box(bd, -2.6, 14.0, -4.4, 2.6, 34.0, -3.6, tabardf)                              # the long tabard
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.4, 60.4, S, cut=1)
    for sx in (-1, 1):
        m.box(hd, sx * 1.0 - 0.4, 57.4, -2.9, sx * 1.0 + 0.4, 58.0, -2.7, solid(P, "eye"))
        spike(m, hd, (sx * 2.4, 59.4, -1.0), (sx, 0.5, 0.2), 1.0, 2.6, metal(P, "steel", dark="steel_dark"))   # winged circlet
    m.round_box(hd, 0, 0.8, 3.2, 3.4, 56.0, 62.0, fabric(P, "red", "red_dark"), cut=1)   # red hood
    for i in range(10):                                                                 # long blonde hair
        ang = math.radians(-110 + i * 24)
        rod(m, hd, (2.6 * math.sin(ang), 58.0, -1.6 * math.cos(ang) + 1.0),
            (4.0 * math.sin(ang), 42.0, 3.0 + abs(math.cos(ang))), 2, strands(P, "hair", "hair_dark"), extend=0.3, t2=1)
    for side in (1, -1):                                                                # four pale wings
        for j, (y, sp) in enumerate(((50.0, 20.0), (44.0, 14.0))):
            feather_wing(m, bd, (side * 2.6, y, 3.6), sp, 8.0, 2, feathers(P, "wing", "wing_dark", size=(1.4, 2.8)),
                         side=side, sweep=25 + j * 10, droop=0.2 * j)
    ar = a["arm_right"]                                                                 # the staff
    h = ar["hand"]
    rod(m, ar["bone"], (h[0], h[1] - 10.0, h[2]), (h[0], h[1] + 24.0, h[2]), 1, solid(P, "brown"), extend=0)
    m.round_box(ar["bone"], h[0], h[2], 1.6, 1.6, h[1] + 24.0, h[1] + 27.0, GOLD, cut=1)
    for sx in (-1, 1):
        spike(m, ar["bone"], (h[0], h[1] + 26.0, h[2]), (sx, 0.6, 0), 1.0, 2.6, GOLD)
    al = a["arm_left"]                                                                  # the sword
    h = al["hand"]
    rod(m, al["bone"], (h[0], h[1], h[2]), (h[0] + 2.0, h[1] - 18.0, h[2] - 6.0), 1, metal(P, "steel", dark="steel_dark"),
        extend=0, t2=2)
    m.box(al["bone"], h[0] - 1.6, h[1] - 0.6, h[2] - 0.6, h[0] + 1.6, h[1] + 0.4, h[2] + 0.6, GOLD)
    return m
