"""Petermon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the boy who never grew up: a lean fairy swordsman in a green tunic and leggings with a brown belt
and shoulder strap, tall brown boots, white gloves, a green feathered hat with a long red plume, long blond hair and a
yellow scarf trailing behind, a short sword in hand and a dagger at its hip. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fabric, leather, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a lean fairy swordsman in a green tunic with a brown belt, tall brown boots, a green plumed hat, long blond hair, "
        "a trailing yellow scarf and a short sword")
BASE = {"green": (60, 120, 60), "green_dark": (24, 70, 24), "brown": (130, 80, 40), "brown_dark": (70, 40, 16),
        "white": (240, 240, 244), "skin": (200, 160, 130), "skin_dark": (150, 110, 80), "hair": (240, 210, 110),
        "hair_dark": (190, 150, 60), "red": (200, 40, 40), "yellow": (240, 210, 80), "steel": (210, 214, 226),
        "eye": (200, 40, 70)}
SHINY = {"green": (60, 80, 150), "green_dark": (24, 30, 90)}


def P(v):
    return pal(BASE, SHINY, v)


TUNIC = fabric(P, "green", "green_dark")
LEATHER = leather(P, "brown", "brown_dark", stitch="hair")


def build():
    m = Model("petermon")
    mats = {"skin": TUNIC, "neck": skin(P, "skin", dark="skin_dark"), "hand": solid(P, "white"),
            "finger": solid(P, "white"), "shin": LEATHER, "calf": LEATHER, "foot": LEATHER, "toe": LEATHER,
            "knee": LEATHER}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.8, leg_bulk=0.85, name="petermon")
    bd = a["body"]
    m.round_box(bd, 0, 0.4, 4.2, 3.2, 33.0, 34.6, LEATHER, cut=1)                          # belt
    m.box(bd, -4.0, 36.0, -3.8, 4.0, 37.0, -3.4, LEATHER, rotation=(0, 0, 35), pivot=(0, 42.0, -3.6))   # strap
    for j in range(5):                                                                   # yellow scarf
        m.box(bd, 2.0 + j * 2.6, 50.0 - j * 0.8, 2.0 + j, 4.6 + j * 2.6, 52.0 - j * 0.8, 2.2 + j,
              fabric(P, "yellow", "hair_dark"), rotation=(0, -15, 10), pivot=(3.3 + j * 2.6, 51.0, 2.1 + j))
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 59.6, skin(P, "skin", dark="skin_dark"), cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.6), 57.2, -2.9, max(sx * 0.6, sx * 1.6), 57.8, -2.8, solid(P, "eye"))
    for i in range(9):                                                                   # long blond hair
        ang = math.radians(-80 + i * 20)
        rod(m, hd, (2.4 * math.sin(ang), 59.0, 0.8), (4.0 * math.sin(ang), 47.0, 4.0), 1, strands(P, "hair", "hair_dark"),
            extend=0.2, t2=2)
    m.round_box(hd, 0, 0, 4.0, 3.8, 59.4, 60.2, TUNIC, cut=1)                              # feathered hat
    m.round_box(hd, 0, 0.4, 2.6, 2.6, 60.2, 63.0, TUNIC, cut=1)
    pts = [(2.0, 62.0, 0), (5.0, 66.0, 2.0), (8.0, 66.0, 5.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, hd, p0, p1, 1, solid(P, "red"), extend=0.2, t2=2)
    ar = a["arm_right"]                                                                  # short sword
    h = ar["hand"]
    m.box(ar["bone"], h[0] - 1.6, h[1] - 0.4, h[2] - 1.0, h[0] + 1.6, h[1] + 0.4, h[2] + 1.0, metal(P, "hair"))
    rod(m, ar["bone"], (h[0], h[1], h[2] - 1.0), (h[0] - 2.0, h[1] + 12.0, h[2] - 4.0), 1, metal(P, "steel"),
        extend=0.2, t2=2)
    rod(m, bd, (4.0, 33.0, -1.0), (6.0, 26.0, -3.0), 1, metal(P, "steel"), extend=0.2)     # dagger at hip
    return m
