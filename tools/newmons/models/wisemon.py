"""Wisemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the sage of the forbidden library: a faceless figure in a long crimson robe with wide sleeves and a
belt, a golden cowl over a black void where its face should be with two glowing eyes, gold stole streamers, gloved
hands raised holding two glowing orbs (the Space-Time Stones), standing on a huge open golden book written in red
runes. 25 blocks.

Front is -z, y is up. 66 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import fabric, gem, leather, plane, solid
from _route import pal, tone

HEIGHT = 63
SCALE, HITBOX = sized(25, HEIGHT, 8.0)
KIND = "floater"
K = 3
LOOK = "a faceless sage in a crimson robe and golden cowl with glowing eyes, holding two glowing orbs, standing on a huge open golden book"
BASE = {"robe": (140, 30, 40), "robe_dark": (80, 10, 16), "gold": (240, 210, 110), "gold_dark": (180, 140, 50),
        "black": (14, 12, 16), "eye": (255, 220, 80), "page": (250, 220, 120), "page_dark": (200, 160, 60),
        "rune": (210, 40, 30), "cover": (120, 60, 30), "red": (230, 60, 50), "red_light": (255, 190, 170),
        "orb": (250, 200, 60), "orb_light": (255, 250, 200)}
SHINY = {"robe": (40, 60, 140), "robe_dark": (14, 24, 80)}


def P(v):
    return pal(BASE, SHINY, v)


ROBE = fabric(P, "robe", "robe_dark")


def pagef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "up" and abs(x) > 1.0 and (int(z * 1.4) % 2 == 0) and int(x * 2.3) % 3:
        return tone(p["rune"], face), None
    return tone(p["page"], face), None


def build():
    m = Model("wisemon")
    top = m.bone("wisemon", None, (0, 0, 0))
    bk = m.bone("book", top, (0, 2, 0))                                                 # the open book
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 0.4, sx * 15.0))
        m.box(bk, x0, 0.0, -10.0, x1, 1.0, 10.0, solid(P, "cover"), rotation=(0, 0, sx * 6), pivot=(0, 0.5, 0))
        m.box(bk, x0, 1.0, -9.4, x1 - sx * 0.6 if sx < 0 else x1 - 0.6, 3.6, 9.4, pagef,
              rotation=(0, 0, sx * 6), pivot=(0, 1.0, 0))
    mats = {"skin": ROBE, "chest": ROBE, "abs": ROBE, "pelvis": ROBE, "deltoid": ROBE, "upper_arm": ROBE,
            "forearm": ROBE, "hand": leather(P, "black", "black"), "thigh": ROBE, "knee": ROBE, "shin": ROBE,
            "calf": ROBE, "foot": leather(P, "black", "black"), "neck": ROBE}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=0.9, leg_bulk=0.95, name="wisemon")
    bd = a["body"]
    m.round_box(bd, 0, 0, 6.0, 4.6, 4.0, 32.0, ROBE, cut=2)                                  # long robe skirt
    m.round_box(bd, 0, 0, 5.4, 4.0, 30.0, 31.6, leather(P, "black", "black"), cut=1)
    for sx in (-1, 1):                                                                   # gold stole streamers
        m.box(bd, sx * 3.0 - 1.0, 14.0, -5.0, sx * 3.0 + 1.0, 50.0, -4.4, fabric(P, "gold", "gold_dark"))
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 3.4, 3.6, 53.0, 62.0, fabric(P, "gold", "gold_dark"), cut=2)       # golden cowl
    m.box(hd, -2.4, 54.0, -3.8, 2.4, 59.4, -3.4, solid(P, "black"))
    for sx in (-1, 1):
        m.box(hd, sx * 1.2 - 0.5, 57.0, -3.9, sx * 1.2 + 0.5, 58.0, -3.7, solid(P, "eye", glow=True))
    spike(m, hd, (0, 62.0, 1.0), (0, 0.4, 1), 2.0, 4.0, fabric(P, "gold", "gold_dark"), tip=0.8)
    for nm, key in (("arm_left", "orb"), ("arm_right", "red")):                         # Space-Time Stones
        h = a[nm]["hand"]
        ball(m, a[nm]["bone"], (h[0], h[1] + 3.0, h[2] - 1.0), 1.6,
             gem(P, key, "orb_light" if key == "orb" else "red_light"), layers=2)
    return m
