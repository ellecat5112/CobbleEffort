"""Cougarmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the mountain lion. A powerful tawny-grey cougar with a shaggy dark-streaked mane, blue swirl
markings round red eyes, small black-tipped ears, white paws and belly, a necklace of gold bells with a braided
cord, and a black-tipped tail. 15 blocks tall.

Front is -z, y is up. 32 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import fur, metal, solid, strands
from _route import pal, tone

HEIGHT = 32
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 14}
LOOK = ("a powerful tawny-grey cougar with a shaggy dark-streaked mane, blue swirl markings round red eyes, white paws "
        "and a necklace of gold bells")
BASE = {"tawny": (196, 180, 150), "tawny_dark": (130, 116, 90), "tawny_tip": (236, 226, 204), "white": (246, 244, 236),
        "white_dark": (200, 196, 186), "black": (34, 32, 34), "blue": (90, 150, 220), "eye": (220, 40, 40),
        "gold": (240, 200, 60), "gold_dark": (170, 130, 20), "cord": (110, 90, 70), "mouth": (130, 30, 40),
        "tooth": (250, 250, 246)}
SHINY = {"tawny": (150, 160, 200), "tawny_dark": (90, 100, 150), "tawny_tip": (210, 220, 245)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "tawny", "tawny_dark", tip="tawny_tip", length=1.2)
MANE = strands(P, "tawny_tip", "black")
WHITE = fur(P, "white", "white_dark", length=1.0)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 2.0) < 0.6 and abs(y - 22.2) < 0.4:
                return p["eye"], p["eye"]
            r = math.hypot(x - sx * 2.0, y - 22.2)
            if 0.9 < r < 1.5 and math.atan2(y - 22.2, (x - sx * 2.0) * sx) > -0.6:
                return tone(p["blue"], face), None                       # swirl markings
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("cougarmon")
    mats = {"skin": FUR, "belly": WHITE, "neck": FUR, "head": headf, "snout": WHITE, "jaw": WHITE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": FUR, "leg_lower": FUR,
            "paw": WHITE, "claw": solid(P, "white_dark"), "tail": FUR}
    a = quadruped(m, mats, "cougarmon", length=24.0, body_y=14.0, body_rx=5.6, body_ry=6.0, chest_bulk=1.3,
                  neck=((0, 18, -12), (0, 21, -15)), head_len=9.0, head_w=4.2, head_h=4.4, snout=0.35, mouth_open=8,
                  teeth=4, leg_bulk=1.6, toes=4, tail=((0, 18, 14), (2, 16, 20), (4, 18, 25)), tail_r=(1.6, 1.3, 1.0))
    hd, bd = a["head"], a["head"]
    for i in range(18):                                                    # shaggy streaked mane
        ang = math.radians(-100 + i * 11.8)
        base = (4.6 * math.sin(ang), 23.0 + 1.4 * math.cos(ang), -13.0 + 1.0 * abs(math.sin(ang)))
        rod(m, hd, base, (base[0] * 1.8, base[1] + 3.0 * math.cos(ang), -8.0), 2, MANE, extend=0.3, t2=2)
    for sx in (-1, 1):                                                     # black-tipped ears
        spike(m, hd, (sx * 3.0, 24.6, -14.0), (sx * 0.3, 1, 0.2), 1.6, 2.6, FUR, tip=0.6)
        spike(m, hd, (sx * 3.2, 26.6, -14.0), (sx * 0.3, 1, 0.2), 0.8, 1.2, solid(P, "black"))
    nk = a["neck"]                                                         # gold bell necklace
    for i in range(5):
        ang = math.radians(-60 + i * 30)
        c = (3.6 * math.sin(ang), 17.6 - 1.0 * math.cos(ang) ** 2, -12.0 - 2.6 * math.cos(ang))
        m.round_box(nk, c[0], c[2], 1.0, 1.0, c[1] - 1.2, c[1] + 0.8, metal(P, "gold", dark="gold_dark"), cut=1)
    rod(m, nk, (0, 16.0, -14.6), (0, 11.0, -15.0), 1, solid(P, "cord"), extend=0)
    e = a["tail_pts"][-1]
    spike(m, a["tail"], e, (0.4, 0.4, 1), 1.6, 2.6, solid(P, "black"), tip=0.6)
    return m
