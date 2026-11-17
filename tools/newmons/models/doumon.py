"""Doumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): the onmyoji fox priest. A tall fox-faced figure in a long black robe trimmed with gold and a pale grey
over-robe with a jagged black-and-white hem, a tall black eboshi cap, a yin-yang medallion on its chest, a huge
white-and-black glove of a hand, a white fox tail, and a swirl of red paper talismans drifting round it. 25 blocks
tall.

Front is -z, y is up. 66 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import fabric, fur, local, skin, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(25, HEIGHT, 2.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a tall fox-faced priest in a long gold-trimmed black robe and a grey over-robe, a tall black cap, a yin-yang "
        "medallion, a huge glove of a hand, a white fox tail and drifting red paper talismans")
BASE = {"black": (34, 32, 40), "black_dark": (10, 10, 14), "grey": (190, 190, 200), "grey_dark": (120, 120, 134),
        "white": (246, 246, 250), "white_dark": (190, 190, 204), "gold": (230, 190, 70), "red": (210, 40, 40),
        "red_dark": (130, 14, 18), "fox": (230, 226, 236), "fox_dark": (170, 166, 186), "eye": (200, 40, 60)}
SHINY = {"black": (60, 40, 110), "black_dark": (24, 14, 50), "red": (60, 110, 220), "red_dark": (20, 50, 140)}


def P(v):
    return pal(BASE, SHINY, v)


ROBE = fabric(P, "black", "black_dark", axis="y")
OVER = fabric(P, "grey", "grey_dark", axis="y")
FOX = fur(P, "fox", "fox_dark", length=1.0)


def robef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(abs(x) - 2.0) < 0.3:
        return tone(p["gold"], face), None
    if face == "north" and math.hypot(x, y - 46.0) < 2.2:                    # yin-yang medallion
        r = math.hypot(x, y - 46.0)
        top = math.hypot(x, y - 47.1) < 1.1
        bot = math.hypot(x, y - 44.9) < 1.1
        light = (x > 0 or top) and not bot
        return tone(p["white"] if light else p["black"], face), None
    return ROBE(x, y, z, face, variant, box=box, **k)


def faced(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(y - (57.6 + (abs(x) - 1.0) * 0.4)) < 0.3 and 0.4 < abs(x) < 1.8 and x * sx > 0:
                return p["eye"], p["eye"]
    return FOX(x, y, z, face, variant, box=box, **k)


def talismanf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if abs(u - W / 2) < 0.3 and 0.6 < v < H - 0.6:
        return tone(p["black"], face), None
    return tone(p["red"], face), None


def build():
    m = Model("doumon")
    mats = {"skin": ROBE, "chest": robef, "abs": robef, "pelvis": ROBE, "neck": FOX, "deltoid": OVER,
            "upper_arm": OVER, "forearm": OVER, "hand": FOX, "finger": FOX, "thigh": ROBE, "knee": ROBE, "shin": ROBE,
            "calf": ROBE, "foot": FOX, "toe": FOX}
    a = humanoid(m, mats, bulk=1.0, arm_bulk=1.0, leg_bulk=1.0, name="doumon")
    bd = a["body"]
    m.round_box(bd, 0, 0.6, 6.0, 4.6, 6.0, 30.0, ROBE, cut=2)                          # long robe skirt
    cape(m, bd, 52.0, 14.0, 44.0, OVER, z=4.2, flare=1.0)                               # grey over-robe
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 2.6, 3.4, 54.0, 60.0, faced, cut=1)                        # fox face
    m.box(hd, -1.4, 54.4, -6.6, 1.4, 56.4, -4.0, FOX)                                   # muzzle
    m.round_box(hd, 0, 0.4, 2.2, 2.6, 60.0, 68.0, ROBE, cut=1)                          # tall eboshi cap
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.2, 59.6, 0.4), (sx * 0.3, 1, 0.1), 1.4, 3.0, FOX, tip=0.5)
    ar = a["arm_right"]                                                                 # huge glove of a hand
    hx, hy, hz = ar["hand"]
    m.round_box(ar["bone"], hx, hz, 4.4, 4.0, hy - 4.0, hy + 3.0, skin(P, "white", dark="white_dark"), cut=2)
    for j in range(4):
        m.round_box(ar["bone"], hx + (j - 1.5) * 2.0, hz - 3.6, 0.9, 1.0, hy - 6.6, hy - 4.0, solid(P, "black"), cut=0)
    tl = m.bone("tail", bd, (0, 30, 4))                                                 # white fox tail
    pts = [(0, 30.0, 4.0), (4.0, 26.0, 10.0), (10.0, 26.0, 14.0), (14.0, 30.0, 14.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 3 + j, FOX, extend=0.8)
    rb = m.bone("ring_talismans", bd, (0, 40, 0))                                       # drifting paper talismans
    for i in range(8):
        ang = 2 * math.pi * i / 8
        cx, cz = 14.0 * math.cos(ang), 14.0 * math.sin(ang)
        cy = 26.0 + 10.0 * math.sin(ang * 2)
        m.box(rb, cx - 1.4, cy, cz, cx + 1.4, cy + 6.0, cz, talismanf, rotation=(0, -math.degrees(ang) + 90, 10),
              pivot=(cx, cy, cz))
    return m
