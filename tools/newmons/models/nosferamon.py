"""Nosferamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the vampire hunter-queen: a slender figure in a long high-collared navy coat with violet trim and
gold buttons, black gloves, armoured boots with clawed feet, long golden hair under a black top hat with a violet
band, pale face, great pink bat wings on silver struts, and a long rifle trailing a ribbon of cyan light. 35 blocks
tall.

Front is -z, y is up. 66 units tall; Ultimate stage. Built covered (a full coat).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing
from _digibody import humanoid
from _digidetail import armour, fabric, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a slender vampire hunter in a long high-collared navy coat, golden hair under a black top hat, great pink bat "
        "wings on silver struts and a long rifle")
BASE = {"navy": (40, 44, 90), "navy_dark": (14, 16, 40), "violet": (140, 80, 190), "gold": (230, 190, 70),
        "skin": (236, 226, 230), "skin_dark": (180, 170, 180), "hair": (246, 220, 140), "hair_dark": (190, 150, 70),
        "black": (28, 26, 32), "pink": (240, 120, 200), "pink_dark": (170, 60, 140), "silver": (210, 214, 226),
        "silver_dark": (110, 116, 130), "cyan": (110, 240, 250, 190), "eye": (220, 30, 60)}
SHINY = {"navy": (110, 30, 40), "navy_dark": (50, 10, 14), "pink": (120, 200, 250), "pink_dark": (50, 130, 200)}


def P(v):
    return pal(BASE, SHINY, v)


COAT = fabric(P, "navy", "navy_dark", seam="violet")


def build():
    m = Model("nosferamon")
    mats = {"skin": COAT, "neck": COAT, "hand": solid(P, "black"), "finger": solid(P, "black"),
            "shin": armour(P, "silver", "silver_dark", trim="violet"), "calf": armour(P, "silver", "silver_dark"),
            "foot": metal(P, "silver"), "talon": metal(P, "silver")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.8, leg_bulk=0.85, talons=True, name="nosferamon")
    bd = a["body"]
    for j in range(4):                                                                   # long coat skirt
        r = 4.6 + j * 1.0
        m.round_box(bd, 0, 0.6, r, r * 0.8, 31.0 - (j + 1) * 4.0, 31.4 - j * 4.0, COAT, cut=1)
    m.round_box(bd, 0, 0.4, 3.0, 3.0, 50.0, 55.0, COAT, cut=1)                            # high collar
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 59.6, skin(P, "skin", dark="skin_dark"), cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.6), 57.0, -2.9, max(sx * 0.6, sx * 1.6), 57.6, -2.8, solid(P, "eye"))
    for i in range(9):                                                                   # long golden hair
        ang = math.radians(-80 + i * 20)
        rod(m, hd, (2.4 * math.sin(ang), 59.0, 0.8 + math.cos(ang)), (4.0 * math.sin(ang), 42.0, 4.0), 1,
            strands(P, "hair", "hair_dark"), extend=0.2, t2=2)
    m.round_box(hd, 0, 0, 4.6, 4.4, 59.6, 60.4, solid(P, "black"), cut=1)                 # top hat
    m.round_box(hd, 0, 0, 2.8, 2.8, 60.4, 64.6, solid(P, "black"), cut=1)
    m.round_box(hd, 0, 0, 2.9, 2.9, 61.0, 61.8, solid(P, "violet"), cut=1)
    wb = m.bone("wings", bd, (0, 49, 3))
    for side in (1, -1):                                                                 # pink bat wings
        bat_wing(m, wb, (side * 3.0, 49.0, 3.0), 26.0, 18.0, 5, metal(P, "silver", dark="silver_dark"),
                 fabric(P, "pink", "pink_dark"), side=side, sweep=15)
    ar = a["arm_right"]                                                                  # long rifle
    h = ar["hand"]
    rod(m, ar["bone"], (h[0] + 2.0, h[1] + 1.0, h[2] + 4.0), (h[0] - 12.0, h[1] - 6.0, h[2] - 12.0), 1,
        solid(P, "black"), extend=0.2, t2=2)
    for j in range(5):                                                                   # ribbon of cyan light
        m.box(ar["bone"], h[0] - 14.0 - j * 3.0, h[1] - 7.0 - j * 0.6, h[2] - 13.0, h[0] - 11.0 - j * 3.0,
              h[1] - 6.4 - j * 0.6, h[2] - 13.0, solid(P, "cyan", glow=True))
    return m
