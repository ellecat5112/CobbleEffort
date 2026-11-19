"""Xingtianmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the headless oni warrior: a squat armoured giant whose face is a fanged green mask on its chest,
blue spirit-fire burning where its head should be, a black horn, a red-and-gold war axe held high, a huge tall shield
of blue and black, fur-trimmed armour, spiked greaves and clawed feet. 25 blocks.

Front is -z, y is up. Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, fur, metal, plane, solid
from _route import pal, tone

HEIGHT = 57
SCALE, HITBOX = sized(25, HEIGHT, 8.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a headless oni warrior with a fanged green mask face on its chest, blue spirit-fire above, a red war axe and a tall blue-and-black shield"
BASE = {"green": (90, 140, 70), "green_dark": (40, 80, 30), "gold": (230, 186, 60), "gold_dark": (160, 110, 20),
        "red": (200, 40, 40), "steel": (200, 204, 216), "steel_dark": (100, 104, 116), "blue": (60, 90, 170),
        "black": (30, 30, 36), "fur": (240, 236, 220), "fur_dark": (180, 170, 150), "fire": (120, 220, 255, 200),
        "tooth": (250, 250, 240), "mouth": (100, 14, 20), "eye": (250, 220, 60)}
SHINY = {"green": (150, 80, 150), "green_dark": (90, 30, 90), "fire": (255, 140, 80, 200)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "green", "green_dark", trim="gold", panel=(3.0, 3.0))
STEEL = metal(P, "steel", dark="steel_dark")


def chestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            if math.hypot(a - sx * 2.4, b - 47.0) < 1.0:
                return p["eye"], p["eye"]
        if 38.0 < b < 42.6 and abs(a) < 4.0:
            if (a * 1.2) % 1.0 < 0.5 and abs(b - 40.3) > 0.8:
                return p["tooth"], None
            return p["mouth"], None
    return ARM(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("xingtianmon")
    mats = {"skin": STEEL, "chest": chestf, "abs": chestf, "pelvis": ARM, "deltoid": STEEL, "upper_arm": STEEL,
            "forearm": ARM, "hand": STEEL, "thigh": fur(P, "fur", "fur_dark"), "knee": STEEL, "shin": STEEL,
            "calf": STEEL, "foot": STEEL, "talon": solid(P, "black"), "neck": STEEL}
    a = humanoid(m, mats, bulk=1.6, arm_bulk=1.4, leg_bulk=1.4, talons=True, name="xingtianmon")
    bd = a["body"]
    m.box(bd, -3.0, 14.0, -5.8, 3.0, 31.0, -5.0, solid(P, "red"))
    fb = m.bone("fire", bd, (0, 54, 0))                                                 # spirit-fire in place of a head
    for j in range(5):
        spike(m, fb, ((j - 2) * 1.6, 52.0, 0), ((j - 2) * 0.2, 1, 0.1), 2.4, 8.0 - abs(j - 2) * 1.6,
              solid(P, "fire", glow=True), tip=0.8)
    spike(m, bd, (6.0, 52.0, 0), (0.4, 1, 0.3), 2.0, 9.0, solid(P, "black"), tip=0.8)
    for nm in ("leg_left", "leg_right"):
        k = a[nm]["knee"]
        spike(m, a[nm]["bone"], (k[0], k[1], k[2] - 3.0), (0, 0.2, -1), 1.4, 3.0, metal(P, "gold"), tip=0.8)
    h = a["arm_right"]["hand"]                                                          # war axe held high
    rb = a["arm_right"]["bone"]
    rod(m, rb, (h[0], h[1] - 4.0, h[2]), (h[0], h[1] + 22.0, h[2]), 1, metal(P, "gold"), extend=0.0)
    m.box(rb, h[0] - 0.6, h[1] + 14.0, h[2] - 6.0, h[0] + 0.6, h[1] + 22.0, h[2] - 0.6, solid(P, "red"))
    m.box(rb, h[0] - 0.7, h[1] + 14.0, h[2] - 7.0, h[0] + 0.7, h[1] + 22.0, h[2] - 6.0, STEEL)
    h = a["arm_left"]["hand"]                                                           # tall shield
    m.box(a["arm_left"]["bone"], h[0] - 3.0, 2.0, h[2] - 8.0, h[0] + 5.0, h[1] + 20.0, h[2] - 6.6,
          armour(P, "blue", "black", trim="black", panel=(4.0, 4.0)))
    return m
