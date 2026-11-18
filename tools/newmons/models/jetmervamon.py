"""Jet Mervamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Mervamon boosted with jet power: a warrior goddess in a red top and short red skirt over black
leggings and armoured yellow greaves, a red crested headpiece with swept black jet fins and red ribbon streamers, a
great golden shield-arm on her left, and on her right the giant cream serpent Olympos coiling from her arm with a gaping
jaw and a pink tongue. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage. Built as officially drawn (clothed).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, fabric, leather, metal, scales, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a warrior goddess in a red top and skirt with black leggings, a red crested headpiece with black jet fins, a "
        "golden shield-arm and the giant cream serpent Olympos coiling from her right arm")
BASE = {"skin": (240, 210, 190), "skin_dark": (190, 150, 130), "red": (210, 30, 40), "red_dark": (120, 10, 20),
        "black": (40, 40, 46), "black_dark": (12, 12, 16), "gold": (240, 200, 70), "gold_dark": (160, 120, 20),
        "cream": (240, 226, 190), "cream_dark": (190, 170, 130), "tongue": (220, 90, 140), "mouth": (180, 60, 90),
        "tooth": (250, 250, 246), "hair": (60, 60, 70), "hair_dark": (24, 24, 30), "eye": (200, 40, 60),
        "snake_eye": (220, 40, 80)}
SHINY = {"red": (40, 70, 200), "red_dark": (14, 24, 110), "cream": (180, 230, 190), "cream_dark": (110, 170, 120)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "skin", dark="skin_dark")
RED = fabric(P, "red", "red_dark")
BLACK = fabric(P, "black", "black_dark")
GOLD = armour(P, "gold", "gold_dark", trim="red", trim_w=0.25)
SNAKE = scales(P, "cream", "cream_dark", size=1.6)


def build():
    m = Model("jetmervamon")
    mats = {"skin": SKIN, "chest": RED, "abs": RED, "pelvis": RED, "neck": SKIN, "deltoid": GOLD,
            "upper_arm": BLACK, "forearm": GOLD, "hand": BLACK, "finger": BLACK, "thigh": BLACK, "knee": GOLD,
            "shin": GOLD, "calf": GOLD, "foot": GOLD, "toe": GOLD}
    a = humanoid(m, mats, bulk=0.82, arm_bulk=0.85, leg_bulk=0.88, name="jetmervamon")
    bd = a["body"]
    for i in range(8):                                                               # short red skirt
        ang = 2 * math.pi * i / 8
        spike(m, bd, (4.0 * math.cos(ang), 33.0, 3.4 * math.sin(ang)), (math.cos(ang) * 0.4, -1, math.sin(ang) * 0.4),
              2.6, 6.0, RED, tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 60.0, SKIN, cut=1)
    m.round_box(hd, 0, 0.4, 2.8, 2.8, 58.0, 61.6, armour(P, "red", "red_dark", trim="gold", trim_w=0.2), cut=1)
    m.round_box(hd, 0, -2.8, 2.2, 0.4, 56.6, 57.6, solid(P, "black"), cut=0)                    # visor band
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.6), 56.8, -3.3, max(sx * 0.6, sx * 1.6), 57.4, -3.2, solid(P, "eye", glow=True))
        for j in range(2):                                                          # black jet fins
            spike(m, hd, (sx * 2.6, 60.0 - j * 1.6, 0.6 + j), (sx, 0.4, 0.6), 1.6, 8.0 - j * 2.0, armour(P, "black", "black_dark"),
                  tip=0.8)
        rod(m, hd, (sx * 2.0, 58.0, 2.4), (sx * 6.0, 48.0, 8.0), 1, RED, extend=0.2, t2=2)         # ribbons
    spike(m, hd, (0, 61.4, -0.6), (0, 1, 0.6), 1.6, 5.0, armour(P, "red", "red_dark"), tip=0.8)
    for i in range(5):                                                              # dark hair
        rod(m, hd, ((i - 2) * 0.9, 59.6, 2.0), ((i - 2) * 1.4, 49.0, 4.0), 1, strands(P, "hair", "hair_dark"), extend=0.3, t2=2)
    hl = a["arm_left"]                                                              # golden shield-arm
    lx, ly, lz = hl["hand"]
    m.round_box(hl["bone"], lx + 1.0, lz - 1.0, 1.0, 5.0, ly - 4.0, ly + 10.0, GOLD, cut=0)
    hr = a["arm_right"]                                                             # the serpent Olympos
    hx, hy, hz = hr["hand"]
    pts = [(hx, hy, hz)]
    for i in range(1, 9):
        t = i / 8
        pts.append((hx - 4.0 - 10.0 * t + 5.0 * math.sin(t * 6.0), hy - 6.0 * math.sin(t * 3.0) + 2.0, hz - 2.0 - 12.0 * t))
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, hr["bone"], p0, p1, 3, SNAKE, extend=0.8)
    sx_, sy_, sz_ = pts[-1]
    m.round_box(hr["bone"], sx_, sz_ - 3.0, 3.0, 4.0, sy_ - 0.4, sy_ + 3.0, SNAKE, cut=1)
    m.round_box(hr["bone"], sx_, sz_ - 3.0, 2.6, 3.6, sy_ - 3.0, sy_ - 1.4, SNAKE, cut=1)
    m.round_box(hr["bone"], sx_, sz_ - 3.4, 2.2, 3.2, sy_ - 1.4, sy_ - 0.4, solid(P, "mouth"), cut=0)
    rod(m, hr["bone"], (sx_, sy_ - 1.0, sz_ - 4.0), (sx_, sy_ - 3.0, sz_ - 10.0), 1, solid(P, "tongue"), extend=0, t2=1)
    for sx in (-1, 1):
        m.box(hr["bone"], min(sx_ + sx * 2.9, sx_ + sx * 3.2), sy_ + 1.4, sz_ - 4.0, max(sx_ + sx * 2.9, sx_ + sx * 3.2),
              sy_ + 2.4, sz_ - 2.6, solid(P, "snake_eye", glow=True))
        spike(m, hr["bone"], (sx_ + sx * 1.6, sy_ - 0.6, sz_ - 6.0), (0, -1, 0), 0.8, 1.6, solid(P, "tooth"), tip=0.8)
    return m
