"""Shamamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little green goblin shaman: a hunched green imp with a spiky green mohawk, pointed ears, a big toothy
grin, a studded brown leather vest over a blue loincloth, big clawed hands and feet, and a heavy wooden club studded
with iron bolts raised overhead. 1 block.

Front is -z, y is up. 64 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fabric, leather, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(1, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a hunched little green goblin with a spiky mohawk, a toothy grin, a studded leather vest and a bolt-studded wooden club"
BASE = {"green": (80, 140, 60), "green_dark": (30, 80, 24), "mohawk": (120, 220, 60), "brown": (120, 80, 50),
        "brown_dark": (70, 44, 24), "blue": (60, 100, 180), "blue_dark": (24, 50, 120), "wood": (150, 100, 60),
        "wood_dark": (90, 56, 30), "steel": (180, 184, 196), "tooth": (250, 250, 236), "eye": (250, 220, 60),
        "mouth": (90, 20, 20)}
SHINY = {"green": (140, 100, 170), "green_dark": (80, 40, 110), "mohawk": (250, 120, 200)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "green", dark="green_dark")


def build():
    m = Model("shamamon")
    mats = {"skin": SKIN, "chest": leather(P, "brown", "brown_dark", stitch="steel"), "abs": leather(P, "brown", "brown_dark"),
            "pelvis": fabric(P, "blue", "blue_dark", axis="y"), "claw": solid(P, "tooth"), "talon": solid(P, "tooth")}
    a = humanoid(m, mats, bulk=0.9, arm_bulk=1.1, leg_bulk=0.9, claws=True, talons=True, name="shamamon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 3.4, 3.6, 53.0, 61.0, SKIN, cut=1)
    m.box(hd, -2.6, 54.0, -4.7, 2.6, 56.0, -4.5, solid(P, "mouth"))
    for j in range(6):
        m.box(hd, -2.4 + j * 0.9, 55.0, -4.8, -1.7 + j * 0.9, 56.0, -4.6, solid(P, "tooth"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.4), 57.6, -4.7, max(sx * 0.8, sx * 2.4), 58.6, -4.5, solid(P, "eye"))
        spike(m, hd, (sx * 3.2, 58.0, -0.6), (sx * 1, 0.4, 0.3), 1.2, 4.0, SKIN, tip=0.8)   # pointed ears
    for j in range(6):                                                                   # spiky mohawk
        spike(m, hd, (0, 61.0, -2.6 + j * 1.0), (0, 1, 0.2), 1.0, 3.0 + (j % 2), strands(P, "mohawk", "green_dark"),
              tip=0.8)
    for j in range(5):
        m.box(bd, -4.0 + j * 2.0, 46.0, -4.4, -3.2 + j * 2.0, 46.8, -4.0, metal(P, "steel"))   # vest studs
    w = a["arm_right"]["wrist"]                                                          # bolt-studded club overhead
    ab = a["arm_right"]["bone"]
    rod(m, ab, (w[0], w[1] - 2.0, w[2]), (w[0] + 2.0, w[1] + 14.0, w[2] + 2.0), 3, leather(P, "wood", "wood_dark"),
        extend=0.4)
    for j in range(3):
        spike(m, ab, (w[0] + 1.4 + j * 0.4, w[1] + 8.0 + j * 2.4, w[2] + 0.4), (-1, 0, -0.3), 0.8, 1.6, metal(P, "steel"),
              tip=0.8)
    return m
