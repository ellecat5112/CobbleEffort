"""Löwemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Legendary Warrior of darkness: a lean warrior in black lion-themed armour with gold trim, a lion
helm with a red visor and gold mane plates, a gold lion-face emblem on the chest, clawed gauntlets and greaves, a
gold-banded spear, and a great floating lion-head shield of bronze beside him. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage (Hybrid).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a lean warrior in black lion-themed armour with gold trim, a lion helm, a gold-banded spear and a floating bronze lion-head shield"
BASE = {"black": (40, 40, 48), "black_dark": (12, 12, 16), "black_light": (110, 110, 130), "gold": (240, 200, 70),
        "gold_dark": (160, 120, 20), "red": (220, 40, 40), "bronze": (200, 160, 140), "bronze_dark": (120, 90, 80),
        "navy": (50, 60, 110), "silver": (210, 214, 224), "silver_dark": (100, 104, 116)}
SHINY = {"black": (230, 230, 238), "black_dark": (150, 150, 166), "black_light": (255, 255, 255)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "black", "black_dark", light="black_light", trim="gold", trim_w=0.3)
GOLD = metal(P, "gold", dark="gold_dark")


def chestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and math.hypot(x, y - 46.0) < 2.0:
        return tone(p["gold"], face), None
    return ARM(x, y, z, face, variant, box=box, **k)


def shieldf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and box is not None:
        cx = box.lo[0] + box.size[0] / 2
        if abs(y - (box.lo[1] + box.size[1] * 0.55)) < 0.8 and abs(abs(x - cx) - 2.4) < 1.0:
            return tone(p["red"], face), p["red"]
        if abs(x - cx) < 3.0 and box.lo[1] + 1.0 < y < box.lo[1] + box.size[1] * 0.4:
            return tone(p["navy"], face), None
    return metal(P, "bronze", dark="bronze_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("lowemon")
    mats = {"skin": ARM, "chest": chestf, "abs": ARM, "pelvis": ARM, "neck": ARM, "deltoid": ARM, "upper_arm": ARM,
            "forearm": ARM, "hand": ARM, "finger": ARM, "claw": GOLD, "thigh": ARM, "knee": GOLD, "shin": ARM, "calf": ARM,
            "foot": ARM, "talon": GOLD}
    a = humanoid(m, mats, bulk=0.9, arm_bulk=0.9, leg_bulk=0.95, claws=True, talons=True, digitigrade=True, name="lowemon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.6, 3.2, 54.0, 60.4, ARM, cut=1)
    m.round_box(hd, 0, -3.8, 2.0, 0.3, 56.6, 58.0, solid(P, "red", glow=True), cut=0)
    for i in range(9):                                                               # gold mane plates
        ang = math.radians(-100 + i * 25)
        spike(m, hd, (2.6 * math.sin(ang), 58.0 + 1.6 * math.cos(ang), 1.0), (math.sin(ang), math.cos(ang) * 0.6 + 0.4, 0.6),
              1.4, 4.0, GOLD, tip=0.8)
    hr = a["arm_right"]                                                              # gold-banded spear
    hx, hy, hz = hr["hand"]
    rod(m, hr["bone"], (hx, hy - 18.0, hz), (hx, hy + 24.0, hz), 1, metal(P, "black_light", dark="black_dark"), extend=0, t2=1)
    for j in range(4):
        m.round_box(hr["bone"], hx, hz, 0.8, 0.8, hy + 6.0 + j * 4.0, hy + 7.0 + j * 4.0, GOLD, cut=0)
    for j in (-1, 0, 1):
        spike(m, hr["bone"], (hx, hy + 24.0, hz), (j * 0.4, 1, 0), 1.0, 5.0, metal(P, "silver", dark="silver_dark"), tip=0.8)
    sb = m.bone("shield", bd, (-16, 46, -2))                                          # floating lion-head shield
    m.box(sb, -22.0, 38.0, -3.0, -10.0, 54.0, -1.0, shieldf)
    for j in range(5):
        ang = math.radians(-60 + j * 30)
        spike(m, sb, (-16.0 + 5.0 * math.sin(ang), 46.0 + 7.0 * math.cos(ang), -2.0), (math.sin(ang), math.cos(ang), 0), 1.6,
              4.0, metal(P, "bronze", dark="bronze_dark"), tip=0.8)
    return m
