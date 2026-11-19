"""Seraphimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): one of the Three Great Angels: a knight in silver-and-blue holy armour trimmed gold, a crested
helm with a dark visor, gold star emblems, a long tabard of red seals, and ten great golden feathered wings fanned
behind it. 35 blocks.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digibody import humanoid
from _digidetail import armour, feathers, metal, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a holy knight in silver-and-blue armour trimmed gold, a crested helm, gold star emblems, a seal tabard and ten golden feathered wings"
BASE = {"silver": (220, 224, 236), "silver_dark": (130, 136, 160), "blue": (50, 80, 170), "blue_dark": (20, 34, 100),
        "gold": (240, 200, 80), "gold_dark": (170, 120, 30), "visor": (30, 30, 50), "red": (200, 40, 40),
        "paper": (246, 236, 200)}
SHINY = {"silver": (60, 60, 74), "silver_dark": (24, 24, 30), "gold": (200, 200, 220), "gold_dark": (120, 120, 140)}


def P(v):
    return pal(BASE, SHINY, v)


def platef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and 44.0 < y < 50.0 and abs(x) < 3.0:
        a = math.atan2(y - 47.0, x)
        r = math.hypot(x, y - 47.0)
        if r < 1.0 + 1.2 * abs(math.cos(a * 2.5)):
            return tone(p["gold"], face), None
    if (y % 8.0) < 1.4:
        return armour(P, "blue", "blue_dark")(x, y, z, face, variant, box=box, **k)
    return armour(P, "silver", "silver_dark", trim="gold", trim_w=0.25)(x, y, z, face, variant, box=box, **k)


def tabardf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs((y % 3.0) - 1.5) < 0.6 and abs(x) < 1.0:
        return tone(p["red"], face), None
    return tone(p["paper"], face), None


def build():
    m = Model("seraphimon")
    mats = {"skin": platef, "knee": metal(P, "gold", dark="gold_dark"), "foot": armour(P, "blue", "blue_dark")}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=0.95, leg_bulk=0.95, name="seraphimon")
    bd = a["body"]
    m.box(bd, -2.0, 8.0, -4.6, 2.0, 32.0, -4.2, tabardf)                                  # seal tabard
    for sx in (-1, 1):
        m.round_box(bd, sx * 8.0, 0, 3.4, 3.6, 46.0, 52.0, platef, cut=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 2.8, 54.0, 60.0, platef, cut=1)
    m.box(hd, -1.8, 56.6, -3.3, 1.8, 58.0, -3.1, solid(P, "visor"))
    for j in range(5):                                                                   # crest
        spike(m, hd, (0, 60.0, -1.0 + j * 0.8), (0, 1, 0.4 + j * 0.2), 1.0, 4.0 + (2 - abs(j - 2)), metal(P, "gold"),
              tip=0.8)
    wb = m.bone("wings", bd, (0, 50, 4))                                                 # ten golden wings
    for sx in (-1, 1):
        for j, (droop, span) in enumerate(((-20.0, 30.0), (-8.0, 28.0), (4.0, 24.0), (14.0, 20.0), (24.0, 16.0))):
            feather_wing(m, wb, (sx * 3.0, 52.0 - j * 3.0, 4.0 + j * 0.6), span, 10.0, 4,
                         feathers(P, "gold", "gold_dark"), side=sx, sweep=20, droop=droop, layers=1)
    return m
