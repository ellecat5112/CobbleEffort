"""Raiji Ludomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the thunder beetle knight: a lean insectoid warrior in navy-and-gold armour with a
horned visored helm, curved navy blade-wings sweeping down like a cloak, segmented gold limbs with hooked claws,
yellow lightning crackling over a field of glowing hexagons, and a ball of lightning held low in one claw. 25 blocks.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a lean thunder-beetle knight in navy-and-gold armour with a horned helm, curved blade-wings and a ball of lightning"
BASE = {"navy": (40, 60, 140), "navy_dark": (14, 20, 60), "gold": (240, 200, 60), "gold_dark": (160, 110, 20),
        "steel": (200, 204, 216), "steel_dark": (100, 104, 120), "bolt": (250, 240, 120), "hex": (250, 240, 150, 120),
        "visor": (90, 220, 250)}
SHINY = {"navy": (140, 30, 40), "navy_dark": (60, 10, 14)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "navy", "navy_dark", trim="gold", trim_w=0.25)
GOLD = metal(P, "gold", dark="gold_dark")


def build():
    m = Model("raijiludomon")
    mats = {"skin": PLATE, "forearm": GOLD, "shin": GOLD, "hand": GOLD, "finger": GOLD, "claw": GOLD, "talon": GOLD}
    a = humanoid(m, mats, bulk=0.9, arm_bulk=0.85, leg_bulk=0.85, claws=True, talons=True, digitigrade=True,
                 name="raijiludomon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.4, 3.0, 54.0, 60.0, PLATE, cut=1)
    m.box(hd, -1.8, 57.0, -3.7, 1.8, 57.8, -3.5, solid(P, "visor", glow=True))
    spike(m, hd, (0, 60.0, -2.0), (0, 1, -0.4), 1.6, 8.0, GOLD, tip=0.8)                    # horn
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 59.0, -1.0), (sx * 0.8, 0.8, -0.2), 1.0, 4.0, PLATE, tip=0.8)
        m.round_box(bd, sx * 7.6, 0, 3.0, 3.4, 46.0, 51.0, PLATE, cut=1)
        for j in range(3):                                                               # curved blade-wings
            pts = [(sx * 6.0, 52.0, 3.0), (sx * (14.0 + j * 3.0), 48.0 - j * 4.0, 5.0),
                   (sx * (12.0 + j * 3.0), 20.0 - j * 4.0, 4.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, bd, p0, p1, 2, PLATE, extend=0.4)
    h = a["arm_right"]["hand"]                                                           # lightning ball
    ball(m, a["arm_right"]["bone"], (h[0], h[1] - 4.0, h[2] - 1.0), 3.4, solid(P, "bolt", glow=True), layers=3)
    for j in range(6):                                                                   # crackling bolts
        ang = 2 * math.pi * j / 6
        c = (h[0] + 6.0 * math.cos(ang), h[1] - 4.0 + 6.0 * math.sin(ang), h[2] - 1.0)
        rod(m, a["arm_right"]["bone"], (h[0], h[1] - 4.0, h[2] - 1.0), c, 1, solid(P, "bolt", glow=True), extend=0.0)
    hb = m.bone("ring_hex", bd, (0, 40, 8))                                              # field of hexagons
    for i in range(6):
        ang = 2 * math.pi * i / 6
        cx, cy = 14.0 * math.cos(ang), 40.0 + 14.0 * math.sin(ang)
        m.box(hb, cx - 3.0, cy - 2.6, 9.0, cx + 3.0, cy + 2.6, 9.0, solid(P, "hex", glow=True))
    return m
