"""Susanoomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the god born of the ten legendary spirits: a towering warrior in gold-and-crimson lacquered armour
over blue greaves, a golden sun-halo crown behind a horned mask-helm, a flaming swirl of red-gold on its chest, broad
golden pauldrons, white gloves and golden clawed boots, and the great beam sword Ame-no-Murakumo. 35 blocks.

Front is -z, y is up. 74 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 74
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a towering god-warrior in gold-and-crimson armour over blue greaves with a golden sun-halo crown and a great beam sword"
BASE = {"gold": (236, 196, 70), "gold_dark": (150, 110, 20), "red": (150, 40, 40), "red_dark": (80, 14, 14),
        "blue": (60, 80, 170), "blue_dark": (20, 30, 90), "white": (246, 246, 250), "beam": (200, 240, 255, 210),
        "eye": (90, 220, 250)}
SHINY = {"red": (60, 60, 70), "red_dark": (20, 20, 26), "gold": (210, 214, 226), "gold_dark": (120, 124, 140)}


def P(v):
    return pal(BASE, SHINY, v)


def platef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and 40.0 < y < 50.0 and abs(x) < 4.0:
        r = math.hypot(x, y - 45.0)
        a = math.atan2(y - 45.0, x)
        if abs(((r - a * 0.8) % 2.4) - 1.2) < 0.4:
            return tone(p["gold"], face), None
    return armour(P, "red", "red_dark", trim="gold", trim_w=0.35)(x, y, z, face, variant, box=box, **k)


GOLD = metal(P, "gold", dark="gold_dark")


def build():
    m = Model("susanoomon")
    mats = {"skin": platef, "shin": armour(P, "blue", "blue_dark", trim="gold", trim_w=0.3),
            "calf": armour(P, "blue", "blue_dark"), "thigh": armour(P, "blue", "blue_dark"), "foot": GOLD,
            "hand": solid(P, "white"), "finger": solid(P, "white"), "talon": GOLD}
    a = humanoid(m, mats, bulk=1.15, arm_bulk=1.1, leg_bulk=1.1, talons=True, name="susanoomon")
    bd = a["body"]
    for sx in (-1, 1):
        m.round_box(bd, sx * 9.0, 0, 4.0, 4.0, 45.0, 53.0, GOLD, cut=1)
        spike(m, bd, (sx * 11.0, 52.0, 0), (sx * 1, 0.6, 0), 1.6, 5.0, GOLD, tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.8, 3.0, 54.0, 60.0, GOLD, cut=1)
    m.box(hd, -1.8, 57.0, -3.7, 1.8, 57.8, -3.5, solid(P, "eye", glow=True))
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 60.0, -1.0), (sx * 0.6, 1, 0.3), 1.4, 6.0, GOLD, tip=0.8)
    hb = m.bone("halo", hd, (0, 60, 3))                                                  # golden sun-halo crown
    for i in range(12):
        ang = 2 * math.pi * i / 12
        spike(m, hb, (0, 60.0, 3.0), (math.cos(ang), math.sin(ang), 0), 1.4, 7.0, GOLD, tip=0.8)
    w = a["arm_right"]["wrist"]                                                          # beam sword
    m.box(a["arm_right"]["bone"], w[0] - 0.8, w[1] + 2.0, w[2] - 2.2, w[0] + 0.8, w[1] + 40.0, w[2] - 0.6,
          solid(P, "beam", glow=True), rotation=(-20, 0, 0), pivot=(w[0], w[1], w[2]))
    m.box(a["arm_right"]["bone"], w[0] - 3.0, w[1], w[2] - 2.6, w[0] + 3.0, w[1] + 2.0, w[2] - 0.2, GOLD)
    return m
