"""Hexeblaumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the ice witch-knight: a slender knight in blue-and-white armour trimmed gold, a white fur collar,
a crimson cloak lined with dark spots, a great fan of jagged ice-crystal blades bursting from its back, a long ice
lance and freezing mist. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import armour, fabric, fur, gem, metal, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a slender knight in blue-and-white armour trimmed gold, a white fur collar, a crimson cloak and a great fan of "
        "jagged ice-crystal blades with a long ice lance")
BASE = {"blue": (40, 90, 200), "blue_dark": (14, 40, 120), "blue_light": (120, 170, 250), "white": (240, 244, 250),
        "white_dark": (180, 186, 200), "gold": (240, 200, 70), "red": (190, 30, 40), "red_dark": (110, 10, 16),
        "ice": (170, 230, 255), "ice_light": (240, 252, 255), "eye": (90, 220, 250)}
SHINY = {"blue": (140, 40, 160), "blue_dark": (70, 14, 90), "blue_light": (210, 140, 230)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "blue", "blue_dark", light="blue_light", trim="gold", trim_w=0.3)
ICE = gem(P, "ice", "ice_light", glow=False)


def build():
    m = Model("hexeblaumon")
    mats = {"skin": ARM, "chest": armour(P, "white", "white_dark", trim="gold"), "abs": ARM, "claw": ICE, "talon": ICE}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.9, leg_bulk=0.95, claws=True, talons=True, digitigrade=True,
                 name="hexeblaumon")
    bd = a["body"]
    m.round_box(bd, 0, 0, 5.6, 4.4, 49.0, 53.0, fur(P, "white", "white_dark", length=1.2), cut=2)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.4, 3.0, 53.6, 60.0, ARM, cut=1)
    m.box(hd, -1.8, 57.2, -3.7, 1.8, 57.8, -3.5, solid(P, "eye", glow=True))
    spike(m, hd, (0, 59.6, -1.0), (0, 1, 0.4), 1.6, 6.0, ICE, tip=0.8)
    cape(m, bd, 52.0, 16.0, 40.0, fabric(P, "red", "red_dark"), z=5.0, flare=1.0)
    for i in range(11):                                                                    # fan of ice blades
        ang = math.radians(10 + i * 16)
        spike(m, bd, (3.0 * math.cos(ang), 50.0 + 3.0 * math.sin(ang), 6.0), (math.cos(ang), math.sin(ang), 0.3), 2.2,
              18.0 - abs(i - 5) * 1.4, ICE, tip=0.9)
    ar, h = a["arm_right"]["bone"], a["arm_right"]["hand"]                                   # long ice lance
    rod(m, ar, (h[0], h[1] + 10.0, h[2] + 6.0), (h[0], h[1] - 6.0, h[2] - 24.0), 2, ICE, extend=0)
    spike(m, ar, (h[0], h[1] - 6.0, h[2] - 24.0), (0, -0.5, -1), 2.4, 6.0, ICE, tip=0.8)
    return m
