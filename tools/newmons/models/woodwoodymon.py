"""Woodwoodymon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net): a wooden cowboy puppet: a jointed figure of varnished wood under a battered brown cowboy hat, a red
neckerchief, a tan vest with a gold star badge over a yellow shirt, blue jeans, brown boots, white gloves, and a long
red lasso whirling round it. 15 blocks.

Front is -z, y is up. 64 units tall; Adult stage (by analogy: wikimon gives no level).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fabric, leather, metal, skin, solid
from _route import pal, tone

HEIGHT = 65
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a wooden cowboy puppet in a battered brown hat, a red neckerchief, a tan vest with a star badge, blue jeans and a red lasso"
BASE = {"wood": (210, 160, 100), "wood_dark": (150, 100, 50), "hat": (150, 90, 50), "hat_dark": (90, 50, 20),
        "red": (210, 40, 40), "vest": (200, 170, 110), "vest_dark": (150, 120, 60), "shirt": (240, 210, 80),
        "jeans": (60, 80, 170), "jeans_dark": (24, 34, 100), "boot": (130, 80, 40), "white": (248, 248, 248),
        "gold": (240, 200, 60), "eye": (40, 30, 20)}
SHINY = {"vest": (110, 150, 200), "vest_dark": (60, 90, 140), "jeans": (90, 60, 40), "jeans_dark": (50, 30, 16)}


def P(v):
    return pal(BASE, SHINY, v)


WOOD = skin(P, "wood", dark="wood_dark")


def vestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if math.hypot(x + 2.4, y - 46.0) < 1.0:
            return tone(p["gold"], face), None
        if abs(x) < 1.4:
            return fabric(P, "shirt", "vest_dark")(x, y, z, face, variant, box=box, **k)
    return fabric(P, "vest", "vest_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("woodwoodymon")
    JEANS = fabric(P, "jeans", "jeans_dark")
    mats = {"skin": WOOD, "chest": vestf, "abs": fabric(P, "shirt", "vest_dark"), "pelvis": JEANS,
            "deltoid": fabric(P, "shirt", "vest_dark"), "upper_arm": fabric(P, "shirt", "vest_dark"),
            "forearm": fabric(P, "shirt", "vest_dark"), "hand": skin(P, "white", dark="vest_dark"), "thigh": JEANS,
            "knee": JEANS, "shin": leather(P, "boot", "hat_dark"), "calf": leather(P, "boot", "hat_dark"),
            "foot": leather(P, "boot", "hat_dark"), "neck": WOOD}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.8, leg_bulk=0.85, name="woodwoodymon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.8, 3.0, 54.0, 61.0, WOOD, cut=1)
    for sx in (-1, 1):
        m.box(hd, sx * 1.2 - 0.5, 58.0, -3.2, sx * 1.2 + 0.5, 59.0, -3.0, solid(P, "eye"))
    m.round_box(hd, 0, 0, 3.2, 3.2, 52.6, 54.4, solid(P, "red"), cut=1)                     # neckerchief
    m.round_box(hd, 0, 0, 6.4, 6.4, 60.6, 61.6, leather(P, "hat", "hat_dark"), cut=3)      # cowboy hat
    m.round_box(hd, 0, 0, 3.4, 3.4, 61.6, 65.0, leather(P, "hat", "hat_dark"), cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 4.0, sx * 6.4), 61.4, -2.0, max(sx * 4.0, sx * 6.4), 62.4, 2.0, leather(P, "hat", "hat_dark"),
              rotation=(0, 0, sx * 20), pivot=(sx * 4.0, 61.6, 0))
    lb = m.bone("lasso", bd, (0, 40, 0))                                                 # whirling red lasso
    for i in range(16):
        ang = i * 2 * math.pi / 16
        cx, cz = 12.0 * math.cos(ang), 12.0 * math.sin(ang)
        m.box(lb, cx - 1.0, 20.0, cz - 1.0, cx + 1.0, 21.0, cz + 1.0, solid(P, "red"))
    return m
