"""Habakirimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the sword god: a powerful lavender-skinned warrior-god with flowing white hair under a golden
sun-crown, a beard, silver armour on his shoulders and legs studded with violet orbs, a red sash, gold bangles, and a
huge sawtoothed sacred sword held high, wind swirling from his open hand. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, fabric, gem, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a powerful lavender-skinned warrior-god with flowing white hair under a golden sun-crown, silver armour with "
        "violet orbs, a red sash and a huge sawtoothed sacred sword")
BASE = {"skin": (170, 160, 220), "skin_dark": (110, 100, 170), "skin_light": (220, 210, 250), "silver": (214, 218, 228),
        "silver_dark": (110, 114, 126), "gold": (240, 200, 60), "gold_dark": (160, 120, 20), "orb": (130, 70, 180),
        "orb_light": (220, 180, 250), "red": (200, 30, 40), "red_dark": (120, 10, 16), "hair": (240, 240, 246),
        "hair_dark": (180, 180, 196), "eye": (250, 220, 60), "wind": (140, 200, 250, 120)}
SHINY = {"skin": (220, 170, 130), "skin_dark": (160, 110, 70), "skin_light": (250, 210, 180)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "skin", dark="skin_dark", light="skin_light")
SILVER = armour(P, "silver", "silver_dark", trim="gold", trim_w=0.3)
GOLD = metal(P, "gold", dark="gold_dark")


def build():
    m = Model("habakirimon")
    mats = {"skin": SKIN, "deltoid": SILVER, "pelvis": fabric(P, "red", "red_dark"), "thigh": SILVER, "knee": SILVER,
            "shin": SILVER, "calf": SILVER, "foot": SKIN, "talon": solid(P, "silver"), "claw": solid(P, "silver")}
    a = humanoid(m, mats, bulk=1.15, arm_bulk=1.2, leg_bulk=1.1, claws=True, talons=True, name="habakirimon")
    bd = a["body"]
    for sx in (-1, 1):
        m.round_box(bd, sx * 8.6, 0.4, 3.6, 4.4, 46.0, 53.0, SILVER, cut=1)
        m.round_box(bd, sx * 8.6, -4.0, 1.2, 0.4, 48.6, 51.0, gem(P, "orb", "orb_light"), cut=0)
    m.round_box(bd, 0, -1.0, 6.0, 4.6, 33.0, 35.0, fabric(P, "red", "red_dark"), cut=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 3.0, 53.6, 60.0, SKIN, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.8), 57.4, -3.5, max(sx * 0.6, sx * 1.8), 58.2, -3.3, solid(P, "eye"))
    for j in range(5):
        spike(m, hd, ((j - 2) * 0.8, 54.6, -2.6), (0, -1, -0.2), 1.0, 4.0, strands(P, "hair", "hair_dark"), tip=0.8)
    for i in range(9):                                                                 # golden sun-crown
        ang = math.radians(20 + i * 17.5)
        spike(m, hd, (3.0 * math.cos(ang), 59.0 + 1.6 * math.sin(ang), 0.4), (math.cos(ang), math.sin(ang), 0), 1.0,
              4.0, GOLD, tip=0.8)
    for i in range(10):                                                                # flowing white hair
        ang = math.radians(-110 + i * 24)
        rod(m, hd, (2.4 * math.sin(ang), 59.0, 1.0 + math.cos(ang) + 1.0), (4.0 * math.sin(ang), 46.0, 6.0), 1,
            strands(P, "hair", "hair_dark"), extend=0.3, t2=2)
    for nm in ("arm_left", "arm_right"):
        w = a[nm]["wrist"]
        m.round_box(a[nm]["bone"], w[0], w[2], 1.8, 1.8, w[1] + 0.4, w[1] + 1.6, GOLD, cut=0)
    ar, h = a["arm_right"]["bone"], a["arm_right"]["hand"]                              # sawtoothed sacred sword
    m.box(ar, h[0] - 0.5, h[1] - 2.0, h[2] - 2.6, h[0] + 0.5, h[1] + 34.0, h[2] + 0.6, metal(P, "silver", dark="silver_dark"))
    for j in range(8):
        spike(m, ar, (h[0], h[1] + 4.0 + j * 4.0, h[2] - 2.6), (0, 0.6, -1), 0.9, 2.6, GOLD, tip=0.8)
    m.round_box(ar, h[0], h[2] - 1.0, 2.6, 1.6, h[1] - 0.6, h[1] + 0.6, GOLD, cut=0)
    al, hl = a["arm_left"]["bone"], a["arm_left"]["hand"]                               # swirling wind
    for j in range(6):
        a0, a1 = j * 0.9, (j + 1) * 0.9
        rod(m, al, (hl[0] + 3.0 * math.cos(a0), hl[1] + j * 1.4, hl[2] - 3.0 * math.sin(a0)),
            (hl[0] + 3.0 * math.cos(a1), hl[1] + (j + 1) * 1.4, hl[2] - 3.0 * math.sin(a1)), 1, solid(P, "wind"),
            extend=0.3, t2=2)
    return m
