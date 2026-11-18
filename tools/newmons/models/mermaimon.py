"""Mermaimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the pirate mermaid: a black pirate hat with a skull badge over long blonde hair in a braid, a
silver chain-mail top under a red-lined black pirate coat with a wide belt, black gloves, a long black fish tail with
a broad split fin, and a huge golden anchor held across her body. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage. Built covered: the chain-mail top is a full shirt.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, fabric, leather, metal, riveted, scales, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = ("a pirate mermaid in a black skull-badged hat, blonde braid, chain-mail shirt under a red-lined black coat, a "
        "long black fish tail and a huge golden anchor")
BASE = {"skin": (240, 210, 190), "skin_dark": (190, 150, 130), "black": (40, 38, 46), "black_dark": (14, 12, 18),
        "red": (190, 30, 40), "chain": (190, 196, 206), "chain_dark": (100, 106, 116), "gold": (240, 200, 70),
        "gold_dark": (160, 120, 20), "hair": (250, 230, 150), "hair_dark": (200, 170, 80), "eye": (60, 140, 200),
        "bone": (246, 244, 236)}
SHINY = {"black": (40, 70, 140), "black_dark": (14, 26, 70), "hair": (240, 160, 190), "hair_dark": (190, 90, 130)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "skin", dark="skin_dark")
CHAIN = riveted(P, "chain", "chain_dark", spacing=1.0)
COAT = fabric(P, "black", "black_dark", seam="red")
TAIL = scales(P, "black", "black_dark", size=1.4)
GOLD = metal(P, "gold", dark="gold_dark")
HAIR = strands(P, "hair", "hair_dark")


def build():
    m = Model("mermaimon")
    mats = {"skin": SKIN, "chest": CHAIN, "abs": CHAIN, "pelvis": leather(P, "black", "black_dark", stitch="gold"),
            "neck": SKIN, "deltoid": COAT, "upper_arm": COAT, "forearm": COAT, "hand": solid(P, "black"),
            "finger": solid(P, "black")}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.95, name="mermaimon")
    m.boxes[:] = [b for b in m.boxes if b.bone not in ("leg_left", "leg_right")]          # a fish tail instead of legs
    m.bones[:] = [b for b in m.bones if b["name"] not in ("leg_left", "leg_right")]
    bd = a["body"]
    m.round_box(bd, 0, 0.4, 4.4, 3.4, 33.0, 35.0, metal(P, "gold", dark="gold_dark"), cut=1)   # belt
    for sx in (-1, 1):                                                                   # open coat panels
        x0, x1 = sorted((sx * 2.8, sx * 5.8))
        m.box(bd, x0, 30.0, -3.8, x1, 51.0, -3.4, COAT)
        m.box(bd, -5.8, 30.0, 3.4, 5.8, 51.0, 3.8, COAT)
    tb = m.bone("tail", bd, (0, 30, 0))                                                  # long black fish tail
    pts = [(0, 31.0, 0.4), (0, 22.0, 1.0), (1.0, 14.0, 3.0), (3.0, 7.0, 7.0), (6.0, 3.0, 12.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tb, p0, p1, 8 - j * 2 if j < 3 else 2, TAIL, extend=1.0)
    e = pts[-1]
    for sy in (-1, 1):                                                                   # split tail fin
        m.box(tb, e[0], e[1] - 1.0, e[2], e[0] + 9.0, e[1] + 1.0, e[2] + 4.0, TAIL,
              rotation=(0, -20, sy * 35), pivot=e)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 60.0, SKIN, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.6), 57.4, -2.9, max(sx * 0.6, sx * 1.6), 58.2, -2.8, solid(P, "eye"))
        spike(m, hd, (sx * 2.4, 57.6, 0.0), (sx * 1, 0.2, 0.2), 1.0, 2.6, SKIN, tip=0.8)     # pointed ears
    m.round_box(hd, 0, 0.6, 2.6, 2.8, 58.0, 61.0, HAIR, cut=1)                           # hair under the hat
    m.round_box(hd, 0, 0.2, 5.0, 4.0, 60.4, 61.2, solid(P, "black"), cut=1)              # pirate hat brim
    m.round_box(hd, 0, 0.2, 3.0, 2.8, 61.2, 64.4, solid(P, "black"), cut=1)
    for sx in (-1, 1):
        spike(m, hd, (sx * 4.4, 61.0, 0.2), (sx * 0.5, 1, 0), 1.6, 3.0, solid(P, "black"), tip=0.8)
    m.box(hd, -0.9, 62.0, -2.75, 0.9, 63.6, -2.6, solid(P, "bone"))                      # skull badge
    pts = [(0, 58.0, 2.4), (0, 50.0, 4.0), (1.0, 42.0, 4.4), (1.4, 36.0, 4.4)]
    for p0, p1 in zip(pts, pts[1:]):                                                     # long braid
        rod(m, hd, p0, p1, 2, HAIR, extend=0.4)
    ar = a["arm_right"]                                                                  # huge golden anchor
    h = ar["hand"]
    top_ = (h[0] + 4.0, h[1] + 14.0, h[2] - 3.0)
    bot = (h[0] + 14.0, h[1] - 20.0, h[2] - 3.0)
    rod(m, ar["bone"], top_, bot, 2, GOLD, extend=0.4)
    for sx in (-1, 1):
        rod(m, ar["bone"], (top_[0] + 1.2, top_[1] - 4.0, top_[2]), (top_[0] + 1.2 + sx * 4.0, top_[1] - 4.6, top_[2]),
            1, GOLD, extend=0.4)
    for i in range(8):                                                                   # ring on top
        ang = 2 * math.pi * i / 8
        m.box(ar["bone"], top_[0] + 2.4 * math.cos(ang) - 0.6, top_[1] + 2.6 + 2.4 * math.sin(ang) - 0.6, top_[2] - 0.6,
              top_[0] + 2.4 * math.cos(ang) + 0.6, top_[1] + 2.6 + 2.4 * math.sin(ang) + 0.6, top_[2] + 0.6, GOLD)
    for sx in (-1, 1):                                                                   # anchor flukes
        p0 = bot
        p1 = (bot[0] + sx * 6.0 - 2.0, bot[1] + 4.0 + sx * 2.0, bot[2])
        rod(m, ar["bone"], p0, p1, 2, GOLD, extend=0.4)
        spike(m, ar["bone"], p1, (sx * 0.3, 1, 0), 1.6, 3.0, GOLD, tip=0.8)
    return m
