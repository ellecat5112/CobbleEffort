"""Shared builder for Kuzuhamon and Kuzuhamon: Miko Mode (CobbleEffort: Digital; hand-built at the detail standard after
the official art on wikimon.net): the fox priestess of the Devas' line. Kuzuhamon: a slender warrior in dark violet
armour with blue plates, a fox-eared helm with a black visor, a yin-yang emblem on the shoulder, a long tattered dark
cloak and a long silver shakujou staff hung with jangling rings. Miko Mode: a shrine maiden in a white kimono top and
loose black hakama with long black hair, a violet fox-eared cap and a staff. Shiny: crimson.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import cape, humanoid
from _digidetail import armour, fabric, metal, skin, solid, strands
from _route import pal, tone

BASE = {"violet": (60, 50, 100), "violet_dark": (20, 16, 44), "violet_light": (130, 120, 190), "blue": (70, 90, 170),
        "blue_dark": (30, 40, 100), "black": (30, 28, 34), "black_dark": (10, 10, 12), "silver": (220, 224, 234),
        "silver_dark": (110, 114, 126), "white": (246, 246, 250), "white_dark": (180, 182, 196), "skin": (240, 220, 210),
        "skin_dark": (190, 160, 150), "eye": (240, 220, 60), "red": (210, 40, 50)}
SHINY = {"violet": (140, 30, 40), "violet_dark": (70, 10, 14), "violet_light": (220, 110, 110), "blue": (200, 120, 50)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "violet", "violet_dark", light="violet_light", trim="blue", trim_w=0.3)
SIL = metal(P, "silver", dark="silver_dark")


def yinyangf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        return tone(p["white"] if (x - box.lo[0]) > box.size[0] / 2 else p["black"], face), None
    return ARM(x, y, z, face, variant, box=box, **k)


def staff(m, bone, base_pt, top_pt):
    rod(m, bone, base_pt, top_pt, 1, SIL, extend=0, t2=1)
    x, y, z = top_pt
    for i in range(8):                                                               # ring head
        a0, a1 = 2 * math.pi * i / 8, 2 * math.pi * (i + 1) / 8
        rod(m, bone, (x + 3.0 * math.sin(a0), y + 3.0 + 3.0 * math.cos(a0), z), (x + 3.0 * math.sin(a1),
            y + 3.0 + 3.0 * math.cos(a1), z), 1, SIL, extend=0.2, t2=1)
    for j in (-1, 1):                                                                # jangling rings
        for t in range(2):
            m.round_box(bone, x + j * (3.4 + t * 1.2), z, 0.9, 0.9, y + 1.0 - t * 1.6, y + 2.4 - t * 1.6, SIL, cut=0)
    spike(m, bone, base_pt, (0, -1, 0), 0.9, 3.0, SIL, tip=0.8)


def make(name, miko=False):
    def build():
        m = Model(name)
        if not miko:
            mats = {"skin": ARM, "chest": ARM, "abs": fabric(P, "black", "black_dark"), "pelvis": ARM, "neck": ARM,
                    "deltoid": yinyangf, "upper_arm": ARM, "forearm": armour(P, "blue", "blue_dark"), "hand": ARM,
                    "finger": ARM, "thigh": ARM, "knee": armour(P, "blue", "blue_dark"), "shin": ARM, "calf": ARM,
                    "foot": ARM, "toe": ARM}
        else:
            WHITE = fabric(P, "white", "white_dark")
            HAK = fabric(P, "black", "black_dark", period=1.6)
            SK = skin(P, "skin", dark="skin_dark")
            mats = {"skin": WHITE, "chest": WHITE, "abs": WHITE, "pelvis": HAK, "neck": SK, "deltoid": WHITE,
                    "upper_arm": WHITE, "forearm": WHITE, "hand": SK, "finger": SK, "thigh": HAK, "knee": HAK,
                    "shin": HAK, "calf": HAK, "foot": solid(P, "white"), "toe": solid(P, "white")}
        a = humanoid(m, mats, bulk=0.8, arm_bulk=0.82, leg_bulk=0.85 if not miko else 1.0, name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        if not miko:
            m.round_box(hd, 0, -0.4, 2.6, 3.0, 54.0, 60.4, ARM, cut=1)
            m.round_box(hd, 0, -3.2, 2.2, 0.3, 56.4, 58.2, solid(P, "black"), cut=0)
            m.box(hd, -1.4, 57.0, -3.6, 1.4, 57.6, -3.5, solid(P, "eye", glow=True))
            cape(m, bd, 53.0, 14.0, 46.0, fabric(P, "black", "black_dark"), z=4.0, flare=0.9, panels=8, sweep=(8.0, 4.0))
        else:
            m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 60.0, skin(P, "skin", dark="skin_dark"), cut=1)
            m.box(hd, -1.6, 57.6, -2.9, -0.6, 58.0, -2.8, solid(P, "black"))
            m.box(hd, 0.6, 57.6, -2.9, 1.6, 58.0, -2.8, solid(P, "black"))
            m.round_box(hd, 0, 0.4, 2.8, 2.8, 59.0, 61.6, ARM, cut=1)                    # violet fox cap
            for i in range(9):                                                       # long black hair
                ang = math.radians(-100 + i * 25)
                rod(m, hd, (2.2 * math.sin(ang), 60.0, 0.6 + 1.4 * math.cos(ang)), (3.0 * math.sin(ang), 30.0, 3.4), 1,
                    strands(P, "black", "black_dark"), extend=0.3, t2=2)
            for sx in (-1, 1):                                                       # wide kimono sleeves
                m.round_box(a["arm_left" if sx > 0 else "arm_right"]["bone"], sx * 7.6, 0, 2.6, 3.6, 36.0, 46.0,
                            fabric(P, "white", "white_dark"), cut=1)
        for sx in (-1, 1):                                                           # fox ears
            spike(m, hd, (sx * 1.8, 60.4 if not miko else 61.2, 0.4), (sx * 0.3, 1, 0.2), 1.4, 4.4, ARM, tip=0.8)
        hr = a["arm_right"]
        hx, hy, hz = hr["hand"]
        staff(m, hr["bone"], (hx, hy - 30.0, hz), (hx, hy + 18.0, hz))
        return m

    return build
