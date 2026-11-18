"""King Etemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
Etemon crowned king: a muscular ape in shining golden armour with a "king" emblem on the chest and a championship
belt, dark shades and a grinning muzzle under a big red velvet crown with a gold orb, a long red cape trimmed with
white fur, blue fur-topped boots, and a swirling blue planet orb held in one hand. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import armour, fabric, fur, gem, metal, skin, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 3.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a muscular ape in shining golden armour with a king emblem, shades, a big red crown, a fur-trimmed red cape, blue boots and a planet orb"
BASE = {"gold": (250, 210, 70), "gold_dark": (170, 120, 20), "gold_light": (255, 245, 180), "red": (200, 30, 40),
        "red_dark": (120, 10, 18), "white": (250, 250, 250), "white_dark": (190, 190, 200), "blue": (60, 90, 190),
        "blue_dark": (24, 40, 110), "black": (24, 24, 30), "muzzle": (240, 220, 180), "orb": (120, 190, 250),
        "orb_light": (230, 245, 255)}
SHINY = {"gold": (220, 224, 236), "gold_dark": (130, 136, 156), "gold_light": (255, 255, 255), "red": (90, 30, 140),
         "red_dark": (40, 10, 70)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark", light="gold_light")


def chestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 2.0 and 45.0 < y < 49.0 and (abs(y - 47.0) < 0.3 or abs(x) < 0.25):
        return tone(p["red"], face), None
    return GOLD(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("kingetemon")
    mats = {"skin": GOLD, "chest": chestf, "abs": GOLD, "pelvis": metal(P, "gold", dark="gold_dark"), "neck": GOLD,
            "deltoid": GOLD, "upper_arm": GOLD, "forearm": GOLD, "hand": GOLD, "finger": GOLD, "thigh": GOLD,
            "knee": GOLD, "shin": fur(P, "blue", "blue_dark"), "calf": fur(P, "blue", "blue_dark"),
            "foot": fur(P, "blue", "blue_dark"), "toe": fur(P, "blue", "blue_dark")}
    a = humanoid(m, mats, bulk=1.15, arm_bulk=1.2, leg_bulk=1.05, name="kingetemon")
    bd = a["body"]
    m.round_box(bd, 0, -0.2, 5.0, 3.8, 33.0, 36.6, metal(P, "gold", dark="gold_dark"), cut=1)   # championship belt
    m.round_box(bd, 0, -4.0, 2.0, 0.4, 33.4, 36.2, gem(P, "red", "gold_light", glow=False), cut=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                              # fur boot tops
        kn = a[nm]["knee"]
        m.round_box(a[nm]["bone"], kn[0], kn[2], 2.8, 2.8, kn[1] - 4.0, kn[1] - 2.4, fur(P, "white", "white_dark"), cut=1)
    cape(m, bd, 53.0, 16.0, 44.0, fabric(P, "red", "red_dark"), z=4.0, flare=0.8, panels=8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 3.0, 3.2, 54.0, 61.0, GOLD, cut=1)
    m.round_box(hd, 0, -3.4, 2.2, 0.8, 54.4, 57.4, skin(P, "muzzle", dark="gold_dark"), cut=1)
    m.round_box(hd, 0, -3.6, 2.6, 0.3, 58.0, 59.0, solid(P, "black"), cut=0)                   # shades
    m.box(hd, -1.6, 55.0, -4.3, 1.6, 55.4, -4.2, solid(P, "white"))
    ball(m, hd, (0, 64.0, 0.4), 4.4, fabric(P, "red", "red_dark"), layers=4, squash=0.8)        # red crown
    m.round_box(hd, 0, 0.4, 4.0, 4.0, 60.4, 62.0, fur(P, "white", "white_dark"), cut=1)
    m.round_box(hd, 0, 0.4, 1.0, 1.0, 67.0, 69.0, gem(P, "gold", "gold_light", glow=False), cut=0)
    hl = a["arm_left"]                                                               # planet orb
    lx, ly, lz = hl["hand"]
    ball(m, hl["bone"], (lx + 1.0, ly + 4.0, lz - 2.0), 3.6, gem(P, "orb", "orb_light"), layers=3)
    return m
