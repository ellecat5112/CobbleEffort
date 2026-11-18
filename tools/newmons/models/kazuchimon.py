"""Kazuchimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the thunder god warrior: a towering samurai in black-and-green lacquered armour with gold trim, a
gold crescent crest on its kabuto, two thick rope-bound topknots rising like horns, a pale robe and white hakama, a
great dark scabbard and a sword crackling with green lightning, and green thunderbolts flashing round it. 35 blocks.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, fabric, metal, solid, twisted
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a towering samurai in black-and-green armour with a gold crescent crest, rope-bound topknots, a white hakama "
        "and a sword crackling with green lightning")
BASE = {"black": (40, 44, 40), "black_dark": (12, 14, 12), "black_light": (100, 110, 100), "green": (90, 220, 90),
        "green_dark": (30, 120, 30), "gold": (240, 200, 70), "gold_dark": (160, 120, 20), "white": (240, 236, 224),
        "white_dark": (180, 172, 156), "rope": (200, 190, 160), "rope_dark": (130, 120, 96), "eye": (250, 60, 40),
        "bolt": (150, 255, 120), "blade": (220, 255, 210)}
SHINY = {"green": (120, 180, 255), "green_dark": (40, 90, 200), "bolt": (140, 200, 255), "blade": (210, 230, 255)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "black", "black_dark", light="black_light", trim="gold", trim_w=0.3, glow_key="green")
HAK = fabric(P, "white", "white_dark", period=1.6)
BOLT = solid(P, "bolt", glow=True)


def build():
    m = Model("kazuchimon")
    mats = {"skin": ARM, "chest": ARM, "abs": HAK, "pelvis": HAK, "neck": ARM, "deltoid": ARM, "upper_arm": HAK,
            "forearm": ARM, "hand": ARM, "finger": ARM, "thigh": HAK, "knee": ARM, "shin": ARM, "calf": ARM,
            "foot": ARM, "toe": metal(P, "gold", dark="gold_dark")}
    a = humanoid(m, mats, bulk=1.2, arm_bulk=1.15, leg_bulk=1.15, name="kazuchimon")
    bd = a["body"]
    for j in range(6):                                                               # hakama skirt
        ang = math.radians(-75 + j * 30)
        spike(m, bd, (4.4 * math.sin(ang), 34.0, -3.4 * math.cos(ang)), (math.sin(ang) * 0.3, -1, -math.cos(ang) * 0.3),
              3.6, 14.0, HAK, tip=0.8)
    for sx in (-1, 1):                                                               # great sode pauldrons
        m.round_box(bd, sx * 9.0, 0.0, 3.0, 4.0, 42.0, 53.0, ARM, cut=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.8, 3.2, 54.0, 60.6, ARM, cut=1)
    m.round_box(hd, 0, -3.4, 2.0, 0.3, 56.6, 57.8, solid(P, "black_dark"), cut=0)
    m.box(hd, -1.4, 57.0, -3.8, 1.4, 57.6, -3.7, solid(P, "eye", glow=True))
    for sx in (-1, 1):                                                               # gold crescent crest
        rod(m, hd, (0, 60.4, -3.0), (sx * 4.0, 64.0, -3.4), 1, metal(P, "gold", dark="gold_dark"), extend=0, t2=1)
        rod(m, hd, (sx * 4.0, 64.0, -3.4), (sx * 5.0, 67.0, -3.0), 1, metal(P, "gold", dark="gold_dark"), extend=0, t2=1)
        pts = [(sx * 2.0, 60.0, 1.0), (sx * 4.0, 66.0, 2.0), (sx * 4.6, 72.0, 2.0)]    # rope topknots
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 2, twisted(P, "rope", "rope_dark"), extend=0.4)
        m.round_box(hd, sx * 4.6, 2.0, 1.4, 1.4, 70.0, 72.0, metal(P, "gold", dark="gold_dark"), cut=0)
    hr = a["arm_right"]                                                              # lightning sword
    hx, hy, hz = hr["hand"]
    m.round_box(hr["bone"], hx, hz, 1.0, 1.0, hy - 2.0, hy + 3.0, ARM, cut=0)
    m.round_box(hr["bone"], hx, hz, 2.6, 2.6, hy + 2.6, hy + 3.4, metal(P, "gold", dark="gold_dark"), cut=0)
    m.round_box(hr["bone"], hx, hz, 1.4, 0.5, hy + 3.4, hy + 36.0, solid(P, "blade", glow=True), cut=0)
    for j in range(4):                                                               # crackling bolts
        y0 = hy + 6.0 + j * 7.0
        rod(m, hr["bone"], (hx - 2.0, y0, hz), (hx + 3.0, y0 + 3.0, hz), 1, BOLT, extend=0, t2=1)
        rod(m, hr["bone"], (hx + 3.0, y0 + 3.0, hz), (hx - 2.6, y0 + 6.0, hz), 1, BOLT, extend=0, t2=1)
    hl = a["arm_left"]                                                               # dark scabbard
    lx, ly, lz = hl["hand"]
    rod(m, hl["bone"], (lx, ly - 22.0, lz + 2.0), (lx, ly + 6.0, lz + 1.0), 2, ARM, extend=0)
    return m
