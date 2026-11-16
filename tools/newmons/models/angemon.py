"""Angemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): an angel warrior. A powerfully muscled bare chest under a draped violet cloth sash and belt, a silver
helm hiding its eyes, long golden hair, six great white wings, a gold Holy Rod, violet arm wraps with gold rings and
white boots with gold cuffs. 15 blocks tall.

Front is -z, y is up. 74 units tall (the wings); Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid, shell
from _digidetail import Bulge, armour, fabric, feathers, local, metal, skin, solid, strands, torso_bulges
from _route import pal, tone

HEIGHT = 74
SCALE, HITBOX = sized(15, HEIGHT, 1.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("an angel warrior: a muscled bare chest under a violet sash, a silver helm, long golden hair, six white wings, "
        "a gold Holy Rod, violet arm wraps and white boots with gold cuffs")
BASE = {"skin": (246, 226, 214), "skin_dark": (190, 150, 140), "skin_light": (255, 246, 240), "violet": (130, 110, 200),
        "violet_dark": (70, 56, 130), "silver": (200, 204, 216), "silver_dark": (100, 104, 120), "gold": (236, 196, 70),
        "gold_dark": (160, 120, 30), "white": (250, 250, 252), "white_dark": (190, 196, 214), "hair": (250, 220, 120),
        "hair_dark": (200, 150, 60), "vein": (220, 186, 176)}
SHINY = {"violet": (210, 80, 110), "violet_dark": (130, 30, 60), "hair": (240, 240, 250), "hair_dark": (180, 180, 200),
         "white": (240, 230, 250), "white_dark": (180, 160, 210)}


def P(v):
    return pal(BASE, SHINY, v)


CHEST = skin(P, "skin", dark="skin_dark", light="skin_light", bulges=torso_bulges(0, 50.5, 5.2, abs_rows=3),
             vein_key="vein", vein_rects=(((-5, 36, 5, 50), ("north",), 3),), vein_count=2, var=0.03)
ARM = skin(P, "skin", dark="skin_dark", light="skin_light", var=0.03,
           bulges=[Bulge("north", sx * 8.4, 42.0, 1.6, 3.4, light=0.3, shadow=0.4) for sx in (-1, 1)])
SASH = fabric(P, "violet", "violet_dark", axis="y", period=2.4)
SILVER = armour(P, "silver", "silver_dark")
GOLD = metal(P, "gold", dark="gold_dark")
BOOT = armour(P, "white", "white_dark", trim="gold")
HAIR = strands(P, "hair", "hair_dark")
WING = feathers(P, "white", "white_dark", size=(1.4, 3.0), flow=(0, -1))


def build():
    m = Model("angemon")
    mats = {"skin": ARM, "chest": CHEST, "abs": CHEST, "pelvis": SASH, "neck": ARM, "deltoid": ARM, "upper_arm": ARM,
            "forearm": SASH, "hand": ARM, "finger": ARM, "thigh": SASH, "knee": SASH, "shin": BOOT, "calf": BOOT,
            "foot": BOOT, "toe": BOOT}
    a = humanoid(m, mats, bulk=1.05, arm_bulk=1.1, leg_bulk=1.0, name="angemon", hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.4, 2.6, 54.6, 60.8, skin(P, "skin", dark="skin_dark"), cut=1)
    m.box(hd, -2.6, 57.0, -2.9, 2.6, 61.2, 2.0, SILVER)                                  # silver helm over the eyes
    for sx in (-1, 1):
        rod(m, hd, (sx * 2.4, 59.0, 0), (sx * 4.2, 61.0, 2.0), 1, SILVER, extend=0.2, t2=2)
    hr = m.bone("mane", hd, (0, 60, 2))
    for i in range(9):                                           # long golden hair
        x = -3.0 + i * 0.75
        rod(m, hr, (x, 60.0, 1.6), (x * 1.4, 38.0 - (i % 3) * 3, 5.0), 2, HAIR, extend=0.3)
    # the violet sash: over the left shoulder, across the chest, a belt and a long fall in front
    rod(m, bd, (5.6, 52.0, -3.6), (-4.6, 34.0, -4.2), 3, SASH, extend=0.4, t2=1)
    m.box(bd, -5.0, 31.0, -4.4, 5.0, 33.6, 4.0, SASH)
    m.box(bd, -2.4, 33.0, -4.8, 0.0, 33.6, -4.0, GOLD)
    m.box(bd, -2.0, 12.0, -4.6, 2.0, 31.0, -4.0, SASH, rotation=(-6, 0, 0), pivot=(0, 31.0, -4.3))
    for nm in ("arm_left", "arm_right"):                          # gold rings on the arm wraps
        w = a[nm]["wrist"]
        rod(m, a[nm]["bone"], w, (w[0], w[1] + 1.4, w[2]), 4, GOLD, extend=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        kn = a[nm]["knee"]
        m.round_box(a[nm]["bone"], kn[0], 0.0, 2.4, 2.6, 11.0, 13.0, GOLD, cut=1)         # gold boot cuffs
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):        # six wings: three per side
        wb = m.bone(nm, bd, (sx * 3.0, 49.0, 3.0))
        for j, (ang, ln) in enumerate(((35, 24.0), (10, 28.0), (-20, 20.0))):
            r = math.radians(ang)
            tip = (sx * (3.0 + ln * math.cos(r)), 49.0 + ln * math.sin(r) + 6, 6.0 + j)
            rod(m, wb, (sx * 3.0, 49.0, 3.0 + j * 0.5), tip, 2, WING, extend=0.3)
            for i in range(10):
                t = (i + 0.5) / 10
                p = tuple(sx * 3.0 * (1 - t) + tip[0] * t if q == 0 else (49.0 * (1 - t) + tip[1] * t if q == 1 else
                          (3.0 + j * 0.5) * (1 - t) + tip[2] * t) for q in range(3))
                fl = 6.0 + 6.0 * t
                m.box(wb, p[0] - 2.0, p[1] - fl, p[2], p[0] + 2.0, p[1], p[2], WING,
                      rotation=(-8, 0, -sx * (20 + 20 * t)), pivot=p)
    ar = a["arm_right"]                                          # the Holy Rod
    h = ar["hand"]
    rb = m.bone("staff", ar["bone"], h)
    rod(m, rb, (h[0] - 4.0, h[1] - 16.0, h[2] - 4.0), (h[0] + 4.0, h[1] + 16.0, h[2] + 4.0), 1, GOLD, extend=0)
    for e in ((h[0] - 4.0, h[1] - 16.0, h[2] - 4.0), (h[0] + 4.0, h[1] + 16.0, h[2] + 4.0)):
        m.box(rb, e[0] - 0.8, e[1] - 0.8, e[2] - 0.8, e[0] + 0.8, e[1] + 0.8, e[2] + 0.8, GOLD)
    return m
