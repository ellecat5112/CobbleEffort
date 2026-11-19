"""Suannishou (a Digimon of the CobbleEffort: Digital crossover; built after the manga sketch on wikimon.net, its only
picture): a lion-headed warrior of the Shou: a tall armoured beast-man with a great maned lion's head under a crested
helm, layered plate armour over a long tasselled tabard, broad pauldrons, a cloak swept back, and flames of spirit
rising behind it. 25 blocks. Perfect stage (no facts on wikimon; by analogy with PalaPandashou).

Front is -z, y is up. 66 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import armour, fabric, fur, metal, solid, strands
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a tall lion-headed warrior of the Shou in layered plate armour over a long tabard, a crested helm and a swept cloak"
BASE = {"gold": (220, 180, 80), "gold_dark": (140, 100, 30), "red": (170, 40, 40), "red_dark": (90, 14, 14),
        "mane": (210, 130, 50), "mane_dark": (130, 70, 20), "fur": (220, 170, 100), "steel": (190, 194, 206),
        "eye": (250, 220, 60), "flame": (250, 160, 60, 180)}
SHINY = {"gold": (200, 204, 216), "gold_dark": (110, 114, 130), "mane": (240, 240, 246), "mane_dark": (170, 170, 186)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "gold", "gold_dark", trim="red", trim_w=0.2)


def capef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["red_dark"] if face == "north" else p["red"], face), None


def build():
    m = Model("suannishou")
    mats = {"skin": PLATE, "neck": fur(P, "fur", "mane_dark"), "hand": fur(P, "fur", "mane_dark"),
            "finger": fur(P, "fur", "mane_dark")}
    a = humanoid(m, mats, bulk=1.05, arm_bulk=1.0, leg_bulk=1.0, name="suannishou")
    bd = a["body"]
    m.box(bd, -3.0, 8.0, -4.8, 3.0, 32.0, -4.2, fabric(P, "red", "red_dark", axis="y"))      # tabard
    cape(m, bd, 52.0, 16.0, 44.0, capef, z=4.0, flare=2.0, panels=6, seed=2, sweep=(10.0, 15.0))
    for sx in (-1, 1):
        m.round_box(bd, sx * 8.4, 0, 3.6, 3.8, 45.0, 52.0, PLATE, cut=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 2.8, 3.2, 53.6, 60.0, fur(P, "fur", "mane_dark"), cut=1)       # lion head
    m.round_box(hd, 0, -4.0, 1.8, 1.4, 53.6, 56.6, fur(P, "fur", "mane_dark"), cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.2), 57.6, -4.3, max(sx * 0.8, sx * 2.2), 58.4, -4.1, solid(P, "eye", glow=True))
    for j in range(14):                                                                  # great mane
        ang = 2 * math.pi * j / 14
        spike(m, hd, (3.0 * math.cos(ang), 57.0 + 3.0 * math.sin(ang), 1.0), (math.cos(ang), math.sin(ang), 0.5), 2.0,
              5.0, strands(P, "mane", "mane_dark"), tip=0.8)
    m.round_box(hd, 0, 0, 3.0, 3.2, 59.6, 61.0, PLATE, cut=1)                                # crested helm
    spike(m, hd, (0, 61.0, -1.0), (0, 1, 0.4), 1.4, 6.0, PLATE, tip=0.8)
    fb = m.bone("flames", bd, (0, 50, 6))
    for j in range(5):
        spike(m, fb, ((j - 2) * 3.0, 50.0, 7.0), ((j - 2) * 0.2, 1, 0.3), 2.6, 14.0, solid(P, "flame", glow=True), tip=0.8)
    return m
