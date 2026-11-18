"""Shared builder for Knightmon and Knightmon Wise Sword Mode (CobbleEffort: Digital; hand-built at the detail standard
after the official art on wikimon.net): the knight: a bulky silver plate-armoured knight with a visored great helm, a
red emblem on a white crest over its breastplate, a violet tabard, studded pauldrons and greaves, and a huge golden
studded greatsword. Wise Sword Mode: a yellow scarf, a brown cloak, a great golden blade-staff with a jewelled
pommel and a curved sabre at its side. Shiny: blackened steel.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import cape, humanoid
from _digidetail import armour, fabric, gem, metal, riveted, solid
from _route import pal, tone

BASE = {"silver": (210, 214, 226), "silver_dark": (100, 104, 120), "silver_light": (255, 255, 255),
        "gold": (240, 200, 70), "gold_dark": (160, 120, 20), "gold_light": (255, 240, 170), "violet": (90, 70, 160),
        "violet_dark": (40, 30, 90), "white": (246, 246, 250), "red": (210, 40, 40), "yellow": (240, 210, 70),
        "yellow_dark": (180, 140, 20), "brown": (140, 110, 60), "brown_dark": (80, 60, 30), "black": (24, 24, 30),
        "blade": (230, 236, 246), "blade_dark": (120, 130, 150)}
SHINY = {"silver": (70, 72, 84), "silver_dark": (24, 24, 30), "silver_light": (150, 150, 170)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "silver", "silver_dark", light="silver_light", trim="gold", trim_w=0.25, rivets=True)
GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")


def chestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 2.6 and 43.0 < y < 49.0:
        if math.hypot(x, y - 46.0) < 1.2:
            return tone(p["red"], face), None
        return tone(p["white"], face), None
    return ARM(x, y, z, face, variant, box=box, **k)


def make(name, wise=False):
    def build():
        m = Model(name)
        mats = {"skin": ARM, "chest": chestf, "abs": fabric(P, "violet", "violet_dark"), "pelvis": ARM, "neck": ARM,
                "deltoid": ARM, "upper_arm": ARM, "forearm": ARM, "hand": ARM, "finger": ARM, "thigh": ARM,
                "knee": GOLD, "shin": ARM, "calf": ARM, "foot": ARM, "toe": ARM}
        a = humanoid(m, mats, bulk=1.3, arm_bulk=1.25, leg_bulk=1.2, name=name)
        bd = a["body"]
        m.round_box(bd, 0, -3.8, 3.4, 0.6, 18.0, 34.0, fabric(P, "violet", "violet_dark", seam="gold"), cut=0)  # tabard
        for sx in (-1, 1):                                                         # studded pauldrons
            m.round_box(bd, sx * 8.6, 0, 3.6, 4.0, 46.0, 53.0, ARM, cut=2)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 2.8, 3.0, 54.0, 61.0, ARM, cut=1)                    # great helm
        for j in range(3):
            m.box(hd, -2.0, 56.6 + j * 0.9, -3.5, 2.0, 57.0 + j * 0.9, -3.3, solid(P, "black"))
        spike(m, hd, (0, 60.6, -0.6), (0, 1, 0.2), 1.0, 3.0, GOLD, tip=0.8)
        hr = a["arm_right"]
        hx, hy, hz = hr["hand"]
        if not wise:                                                               # huge golden greatsword
            m.round_box(hr["bone"], hx, hz, 1.0, 1.0, hy - 2.0, hy + 3.0, GOLD, cut=0)
            m.round_box(hr["bone"], hx, hz, 4.6, 1.2, hy + 3.0, hy + 4.6, GOLD, cut=0)
            m.round_box(hr["bone"], hx, hz - 0.4, 3.0, 0.8, hy - 38.0, hy - 2.0, riveted(P, "gold", "gold_dark", spacing=2.6),
                        cut=0)
            spike(m, hr["bone"], (hx, hy - 38.0, hz - 0.4), (0, -1, 0), 3.0, 4.0, metal(P, "blade", dark="blade_dark"),
                  tip=0.8)
        else:                                                                      # blade-staff, scarf, cloak, sabre
            rod(m, hr["bone"], (hx, hy - 30.0, hz), (hx, hy + 14.0, hz), 1, GOLD, extend=0, t2=1)
            m.round_box(hr["bone"], hx, hz - 0.4, 3.2, 0.8, hy - 22.0, hy + 4.0, GOLD, cut=0)
            m.round_box(hr["bone"], hx, hz - 1.4, 0.8, 0.3, hy - 14.0, hy - 12.0, gem(P, "red", "white"), cut=0)
            spike(m, hr["bone"], (hx, hy + 14.0, hz), (0, 1, 0), 1.4, 4.0, GOLD, tip=0.8)
            m.round_box(bd, 0, 0.4, 3.4, 3.4, 51.0, 54.0, fabric(P, "yellow", "yellow_dark"), cut=1)
            rod(m, bd, (-2.0, 53.0, -3.0), (-14.0, 58.0, -4.0), 1, fabric(P, "yellow", "yellow_dark"), extend=0.3, t2=3)
            cape(m, bd, 53.0, 16.0, 46.0, fabric(P, "brown", "brown_dark"), z=4.0, flare=0.7, panels=8)
            hl = a["arm_left"]
            lx, ly, lz = hl["hand"]
            for j in range(4):
                rod(m, hl["bone"], (lx + 1.0 + j * 0.6, ly - 4.0 - j * 7.0, lz), (lx + 1.6 + j * 0.8, ly - 11.0 - j * 7.0, lz),
                    1, metal(P, "blade", dark="blade_dark"), extend=0.2, t2=2)
        return m

    return build
