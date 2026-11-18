"""Panoptemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the hundred-eyed bird: a white peacock-man with gold armour on its breast set with blue eye-gems,
a crested head, a long golden spear with blue ribbons, and a great fan of blue tail plumes each marked with an eye.
25 blocks tall.

Front is -z, y is up. 60 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, feathers, gem, local, metal, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a white peacock-man in gold armour set with blue eye-gems, a crested head, a golden spear and a great fan of eyed blue plumes"
BASE = {"white": (240, 242, 250), "white_dark": (170, 176, 200), "gold": (236, 196, 80), "gold_dark": (160, 120, 30),
        "blue": (60, 120, 220), "blue_dark": (20, 50, 140), "cyan": (110, 220, 250), "beak": (240, 200, 70),
        "eye": (30, 30, 40), "talon": (90, 90, 110)}
SHINY = {"blue": (60, 180, 100), "blue_dark": (20, 110, 50), "cyan": (190, 250, 160)}


def P(v):
    return pal(BASE, SHINY, v)


FEATH = feathers(P, "white", "white_dark")
GOLD = armour(P, "gold", "gold_dark", trim="blue", trim_w=0.25)


def plumef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if math.hypot(u - W / 2, v - H * 0.85) < min(W, H) * 0.25:
        return tone(p["cyan"], face), p["cyan"]
    return tone(p["blue"] if u % 1.6 > 0.3 else p["blue_dark"], face), None


def build():
    m = Model("panoptemon")
    mats = {"skin": FEATH, "chest": GOLD, "deltoid": GOLD, "forearm": GOLD, "hand": FEATH, "finger": FEATH,
            "talon": solid(P, "talon"), "foot": solid(P, "talon"), "shin": solid(P, "talon")}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.8, leg_bulk=0.85, talons=True, digitigrade=True, name="panoptemon")
    bd = a["body"]
    for j in range(3):
        ball(m, bd, (-2.0 + j * 2.0, 46.0, -4.4), 0.8, gem(P, "blue", "cyan"), layers=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.2, 2.6, 54.0, 59.4, FEATH, cut=1)
    spike(m, hd, (0, 56.6, -3.0), (0, -0.2, -1), 1.4, 3.6, solid(P, "beak"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.2), 57.4, -2.7, max(sx * 1.0, sx * 2.2), 58.2, -2.5, solid(P, "eye"))
    for i in range(5):                                                                   # crest
        spike(m, hd, ((i - 2) * 0.6, 59.0, 0.4), ((i - 2) * 0.2, 1, 0.5), 0.8, 4.0, solid(P, "blue"), tip=0.8)
    for i in range(9):                                                                   # great fan of eyed plumes
        ang = math.radians(-80 + i * 20)
        m.box(bd, -1.6, 36.0, 4.6, 1.6, 64.0, 4.8, plumef, rotation=(0, 0, math.degrees(ang) * 0.9),
              pivot=(0, 36.0, 4.7))
    ar = a["arm_right"]                                                                  # golden spear
    h = ar["hand"]
    rod(m, ar["bone"], (h[0], h[1] - 22.0, h[2]), (h[0], h[1] + 24.0, h[2]), 1, metal(P, "gold"), extend=0.2)
    spike(m, ar["bone"], (h[0], h[1] + 24.0, h[2]), (0, 1, 0), 1.8, 5.0, metal(P, "gold"), tip=0.8)
    m.box(ar["bone"], h[0] - 0.2, h[1] + 14.0, h[2] - 0.8, h[0] + 0.2, h[1] + 20.0, h[2] + 0.8, solid(P, "blue"))
    return m
