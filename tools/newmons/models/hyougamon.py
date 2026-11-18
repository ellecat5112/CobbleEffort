"""Hyougamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the ice ogre: a hulking pale-blue oni with frost-white hair, a single icy horn, tusked jaw, a
spiked collar, a fur loincloth, shaggy white fur cuffs on its arms and legs and a great club of ice. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fur, gem, leather, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a hulking pale-blue ice oni with frost-white hair, an icy horn, tusks, a spiked collar, fur cuffs and an ice club"
BASE = {"blue": (150, 190, 230), "blue_dark": (70, 110, 170), "blue_light": (220, 236, 250), "white": (246, 248, 252),
        "white_dark": (180, 196, 220), "ice": (180, 230, 255, 200), "ice_light": (240, 252, 255, 230),
        "brown": (120, 90, 70), "brown_dark": (60, 40, 30), "steel": (200, 204, 216), "steel_dark": (100, 104, 116),
        "eye": (250, 230, 60), "mouth": (40, 40, 70), "tusk": (250, 250, 240)}
SHINY = {"blue": (170, 220, 170), "blue_dark": (80, 140, 90), "ice": (200, 255, 210, 200)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "blue", dark="blue_dark", light="blue_light")
FUR = fur(P, "white", "white_dark")
ICE = gem(P, "ice", "ice_light", glow=False)


def build():
    m = Model("hyougamon")
    mats = {"skin": SKIN, "chest": SKIN, "abs": SKIN, "pelvis": FUR, "neck": SKIN, "deltoid": SKIN,
            "upper_arm": SKIN, "forearm": FUR, "hand": SKIN, "finger": SKIN, "claw": solid(P, "tusk"), "thigh": SKIN,
            "knee": SKIN, "shin": FUR, "calf": FUR, "foot": SKIN, "talon": solid(P, "tusk")}
    a = humanoid(m, mats, bulk=1.25, arm_bulk=1.2, leg_bulk=1.15, claws=True, talons=True, name="hyougamon")
    bd = a["body"]
    m.round_box(bd, 0, 0.4, 3.0, 3.0, 50.0, 53.0, metal(P, "steel", dark="steel_dark"), cut=1)  # spiked collar
    for i in range(10):
        ang = 2 * math.pi * i / 10
        spike(m, bd, (3.2 * math.cos(ang), 51.4, 0.4 + 3.2 * math.sin(ang)), (math.cos(ang), 0.2, math.sin(ang)), 0.9,
              2.4, metal(P, "steel", dark="steel_dark"), tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 3.0, 3.0, 53.6, 60.6, SKIN, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.2), 57.8, -3.3, max(sx * 0.8, sx * 2.2), 58.8, -3.0, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 1.6, 54.6, -3.0), (sx * 0.2, 1, -0.4), 0.9, 2.4, solid(P, "tusk"), tip=0.8)  # tusks
    m.box(hd, -1.8, 54.4, -3.3, 1.8, 55.4, -3.0, solid(P, "mouth"))
    spike(m, hd, (0, 60.4, -1.4), (0, 1, -0.2), 2.0, 7.0, ICE, tip=0.8)                    # single icy horn
    for i in range(11):                                                             # frost-white hair
        ang = math.radians(-100 + i * 20)
        spike(m, hd, (3.0 * math.sin(ang), 59.4, 0.6 + 2.4 * math.cos(ang)), (math.sin(ang) * 0.8, 0.4, 0.6), 1.8,
              6.0, strands(P, "white", "white_dark"), tip=0.8)
    hnd = a["arm_right"]["hand"]                                                     # great ice club
    cb = a["arm_right"]["bone"]
    rod(m, cb, (hnd[0], hnd[1] - 2.0, hnd[2]), (hnd[0] - 1.6, hnd[1] + 5.0, hnd[2] - 2.0), 2,
        leather(P, "brown", "brown_dark"), extend=0.6)
    top_ = (hnd[0] - 5.0, hnd[1] + 18.0, hnd[2] - 4.0)
    rod(m, cb, (hnd[0] - 1.6, hnd[1] + 5.0, hnd[2] - 2.0), top_, 5, ICE, extend=1.0)
    for j in range(5):
        ang = 2 * math.pi * j / 5
        spike(m, cb, (top_[0] + 2.6 * math.cos(ang), top_[1] - 2.0, top_[2] + 2.6 * math.sin(ang)),
              (math.cos(ang), 0.3, math.sin(ang)), 1.0, 3.0, ICE, tip=0.8)
    return m
