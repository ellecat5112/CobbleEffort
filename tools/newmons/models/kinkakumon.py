"""Kinkakumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the gold horn oni of the Saiyu Warriors, Ginkakumon's partner: a powerful oni warrior in golden
armour with a golden horned helm over spiky green hair, golden clawed gauntlets, a long red cape with gold edges, a
giant spiked iron mace slung over its shoulder and a crackling blue lightning orb in its other claw. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage. Built fully armoured.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import armour, fabric, gem, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a powerful oni warrior in golden armour with a horned helm, spiky green hair, a red cape, a giant spiked mace and a lightning orb"
BASE = {"gold": (240, 200, 70), "gold_dark": (160, 120, 20), "gold_light": (255, 240, 170), "green": (80, 190, 110),
        "green_dark": (30, 110, 50), "red": (200, 40, 40), "red_dark": (120, 14, 20), "steel": (200, 204, 216),
        "steel_dark": (90, 94, 106), "black": (30, 30, 36), "eye": (240, 60, 40), "orb": (120, 200, 255),
        "orb_light": (230, 250, 255)}
SHINY = {"gold": (220, 224, 236), "gold_dark": (130, 136, 156), "gold_light": (255, 255, 255), "green": (220, 90, 160),
         "green_dark": (140, 30, 90)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark", light="gold_light", trim="black", trim_w=0.2)
METAL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("kinkakumon")
    mats = {"skin": GOLD, "chest": GOLD, "abs": GOLD, "pelvis": GOLD, "neck": GOLD, "deltoid": GOLD, "upper_arm": GOLD,
            "forearm": GOLD, "hand": GOLD, "finger": GOLD, "claw": metal(P, "gold", dark="gold_dark"), "thigh": GOLD,
            "knee": GOLD, "shin": GOLD, "calf": GOLD, "foot": GOLD, "talon": metal(P, "gold", dark="gold_dark")}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=1.0, leg_bulk=1.0, claws=True, talons=True, digitigrade=True,
                 name="kinkakumon")
    bd = a["body"]
    cape(m, bd, 53.0, 14.0, 44.0, fabric(P, "red", "red_dark", seam="gold"), z=4.0, flare=0.8, panels=8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 3.0, 54.0, 60.4, GOLD, cut=1)
    m.round_box(hd, 0, -3.2, 2.0, 0.3, 56.6, 57.6, solid(P, "black"), cut=0)
    m.box(hd, -1.6, 56.8, -3.6, 1.6, 57.4, -3.5, solid(P, "eye", glow=True))
    for sx in (-1, 1):                                                               # golden horns
        pts = [(sx * 2.0, 60.0, -1.0), (sx * 3.6, 64.0, -1.0), (sx * 4.0, 68.0, 0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 2 - j, metal(P, "gold", dark="gold_dark"), extend=0.4)
    for i in range(10):                                                              # spiky green hair
        ang = math.radians(-100 + i * 22)
        spike(m, hd, (2.4 * math.sin(ang), 60.0, 1.0 + 1.6 * math.cos(ang)), (math.sin(ang) * 0.7, 0.6, 0.7), 1.6, 6.0,
              strands(P, "green", "green_dark"), tip=0.8)
    hr = a["arm_right"]                                                              # giant spiked mace
    hx, hy, hz = hr["hand"]
    rod(m, hr["bone"], (hx, hy - 2.0, hz), (hx - 4.0, hy + 26.0, hz + 6.0), 1, METAL, extend=0, t2=1)
    head_ = (hx - 4.0, hy + 26.0, hz + 6.0)
    m.round_box(hr["bone"], head_[0], head_[2], 3.0, 3.0, head_[1] - 6.0, head_[1] + 2.0, METAL, cut=1)
    for j in range(8):
        ang = 2 * math.pi * j / 8
        spike(m, hr["bone"], (head_[0] + 3.0 * math.cos(ang), head_[1] - 2.0, head_[2] + 3.0 * math.sin(ang)),
              (math.cos(ang), 0, math.sin(ang)), 1.2, 3.0, solid(P, "black"), tip=0.8)
    hl = a["arm_left"]                                                               # lightning orb
    lx, ly, lz = hl["hand"]
    ball(m, hl["bone"], (lx + 1.0, ly - 2.0, lz - 3.0), 3.0, gem(P, "orb", "orb_light"), layers=3)
    return m
