"""Pharaohmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the god-king of the desert: a towering figure in banded golden armour and a white royal cloak, a
golden pharaoh's headdress and mask with an ankh-topped crown, jewelled collar, golden clawed feet, and a great golden
sarcophagus standing at its side like a shield, set with red gems. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import armour, fabric, gem, metal, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("a towering god-king in banded golden armour and a white cloak, a golden pharaoh headdress and mask with an ankh "
        "crown, a jewelled collar and a great golden sarcophagus shield")
BASE = {"gold": (236, 196, 70), "gold_dark": (150, 110, 24), "white": (244, 242, 236), "white_dark": (190, 186, 176),
        "blue": (40, 80, 180), "red": (200, 30, 40), "red_light": (255, 150, 150), "black": (30, 28, 30),
        "eye": (230, 40, 40)}
SHINY = {"gold": (200, 210, 230), "gold_dark": (110, 120, 140)}


def P(v):
    return pal(BASE, SHINY, v)


def bandf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face != "up" and (y % 2.4) < 0.5:
        return tone(p["gold_dark"], face), None
    return metal(P, "gold", dark="gold_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("pharaohmon")
    mats = {"skin": bandf, "chest": bandf, "abs": bandf, "talon": metal(P, "gold")}
    a = humanoid(m, mats, bulk=1.05, arm_bulk=1.0, leg_bulk=1.05, talons=True, name="pharaohmon")
    bd = a["body"]
    cape(m, bd, 52.0, 18.0, 48.0, fabric(P, "white", "white_dark", seam="gold"), z=4.0, flare=0.8, panels=6, seed=10)
    for i in range(7):                                                                   # jewelled collar
        ang = math.radians(-60 + i * 20)
        ball(m, bd, (4.4 * math.sin(ang), 51.0 - abs(i - 3) * 0.4, -3.6 * math.cos(ang)), 0.8,
             gem(P, "blue" if i % 2 else "red", "red_light"), layers=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 2.8, 54.0, 60.0, armour(P, "gold", "gold_dark", trim="blue", trim_w=0.3), cut=1)
    m.box(hd, -1.8, 57.4, -3.3, 1.8, 58.2, -3.1, solid(P, "eye", glow=True))
    for sx in (-1, 1):                                                                   # headdress lappets
        x0, x1 = sorted((sx * 2.4, sx * 4.0))
        m.box(hd, x0, 50.0, -1.0, x1, 59.0, 2.0, armour(P, "gold", "gold_dark", trim="blue", trim_w=0.4))
    m.round_box(hd, 0, 0, 2.0, 2.0, 60.0, 64.0, metal(P, "gold"), cut=1)                   # crown
    for i in range(8):                                                                   # ankh loop
        ang = 2 * math.pi * i / 8
        m.box(hd, 1.4 * math.cos(ang) - 0.4, 66.4 + 1.6 * math.sin(ang) - 0.4, -0.4, 1.4 * math.cos(ang) + 0.4,
              66.4 + 1.6 * math.sin(ang) + 0.4, 0.4, metal(P, "gold"))
    al = a["arm_left"]                                                                   # golden sarcophagus shield
    w = al["wrist"]
    m.round_box(al["bone"], w[0] + 4.0, w[2] - 3.0, 4.0, 2.4, 2.0, 50.0, bandf, cut=1)
    m.round_box(al["bone"], w[0] + 4.0, w[2] - 5.2, 2.6, 0.6, 38.0, 46.0, armour(P, "gold", "gold_dark", trim="blue"), cut=0)
    for j in range(4):
        ball(m, al["bone"], (w[0] + 4.0, 30.0 - j * 6.0, w[2] - 5.6), 1.0, gem(P, "red", "red_light"), layers=1)
    return m
