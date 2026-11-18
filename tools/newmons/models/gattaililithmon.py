"""Gattai Lilithmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net, its design kept as drawn): the Demon Lord of lust combined: a slender figure in black
armour with gold trim and jewelled ornaments, a horned golden headdress with long black hair, great tattered purple
bat wings and cape, armoured boots, and a long whip ending in a spiky white mask. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage (no level on wikimon).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing
from _digibody import cape, humanoid
from _digidetail import armour, fabric, gem, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a slender figure in black gold-trimmed armour, a horned golden headdress, long black hair, great purple bat "
        "wings and cape, and a long whip ending in a spiky white mask")
BASE = {"black": (36, 32, 44), "black_dark": (12, 10, 18), "black_light": (100, 90, 120), "gold": (230, 190, 70),
        "gold_dark": (150, 110, 20), "purple": (110, 60, 150), "purple_dark": (50, 20, 80), "skin": (220, 190, 200),
        "skin_dark": (160, 130, 150), "hair": (30, 26, 34), "hair_dark": (10, 8, 14), "gem": (200, 30, 60),
        "gem_light": (255, 140, 160), "mask": (230, 236, 250), "mask_dark": (150, 160, 190), "eye": (200, 30, 60),
        "steel": (180, 184, 196), "steel_dark": (90, 94, 106)}
SHINY = {"purple": (190, 40, 50), "purple_dark": (100, 10, 20), "black": (230, 230, 240), "black_dark": (150, 150, 170),
         "black_light": (255, 255, 255)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "black", "black_dark", light="black_light", trim="gold", trim_w=0.25)
SKIN = skin(P, "skin", dark="skin_dark")
MASK = metal(P, "mask", dark="mask_dark")


def build():
    m = Model("gattaililithmon")
    mats = {"skin": ARM, "neck": SKIN, "hand": ARM, "finger": ARM, "claw": solid(P, "black_dark")}
    a = humanoid(m, mats, bulk=0.75, arm_bulk=0.8, leg_bulk=0.85, claws=True, name="gattaililithmon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.2, 2.6, 53.6, 59.4, SKIN, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.6), 57.0, -2.9, max(sx * 0.6, sx * 1.6), 57.6, -2.7, solid(P, "eye"))
        spike(m, hd, (sx * 2.2, 59.6, 0), (sx * 0.8, 1, 0.2), 1.4, 5.0, metal(P, "gold", dark="gold_dark"), tip=0.8)
    m.round_box(hd, 0, 0.0, 2.6, 2.8, 58.8, 61.0, metal(P, "gold", dark="gold_dark"), cut=1)   # golden headdress
    m.round_box(hd, 0, -2.9, 0.8, 0.3, 59.4, 60.6, gem(P, "gem", "gem_light"), cut=0)
    for i in range(9):                                                                        # long black hair
        ang = math.radians(-100 + i * 25)
        rod(m, hd, (2.2 * math.sin(ang), 59.0, 0.4 + math.cos(ang) + 1.0), (3.0 * math.sin(ang), 46.0, 3.6), 1,
            strands(P, "hair", "hair_dark"), extend=0.3, t2=2)
    for j in range(3):                                                                         # jewelled ornaments
        m.round_box(bd, (j - 1) * 3.0, -3.8, 0.7, 0.3, 46.0 - abs(j - 1) * 1.0, 47.4 - abs(j - 1) * 1.0,
                    gem(P, "gem", "gem_light"), cut=0)
    cape(m, bd, 51.0, 16.0, 44.0, fabric(P, "purple", "purple_dark"), z=4.0, flare=1.0)
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 48.0, 4.0))
        bat_wing(m, wb, (side * 3.0, 48.0, 4.0), 22.0, 14.0, 4, metal(P, "black", dark="black_dark"),
                 fabric(P, "purple", "purple_dark"), side=side, sweep=20)
    ar, h = a["arm_right"]["bone"], a["arm_right"]["hand"]                                     # the whip and mask
    pts = [(h[0], h[1], h[2] - 1.0), (h[0] - 6.0, h[1] + 8.0, h[2] - 6.0), (h[0] - 12.0, h[1] + 2.0, h[2] - 8.0),
           (h[0] - 14.0, h[1] - 12.0, h[2] - 6.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, ar, p0, p1, 1, metal(P, "steel", dark="steel_dark"), extend=0.2, t2=1)
    c = pts[-1]
    m.round_box(ar, c[0], c[2], 2.4, 2.0, c[1] - 6.0, c[1], MASK, cut=1)
    for i in range(9):
        ang = math.radians(i * 40)
        spike(m, ar, (c[0] + 2.0 * math.cos(ang), c[1] - 3.0 + 2.4 * math.sin(ang), c[2]),
              (math.cos(ang), math.sin(ang), 0.3), 1.0, 3.6, MASK, tip=0.8)
    return m
