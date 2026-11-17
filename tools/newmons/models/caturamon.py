"""Caturamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): one of the Twelve Devas, a guardian lion-dog (komainu). A stocky four-legged beast in rounded
silver-blue armour with gold-rimmed drum plates on its flanks, a violet cloak over its back, a lion-dog head with a
curly silver mane, gold fangs and a wide red mouth, black-clawed paws and a curling teal-tipped tail. 25 blocks tall.

Front is -z, y is up. 34 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, fabric, metal, solid, strands
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(25, HEIGHT, 3.2)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a stocky guardian lion-dog in silver-blue armour with gold-rimmed drum plates, a violet cloak, a curly mane, "
        "gold fangs and a curling teal-tipped tail")
BASE = {"silver": (180, 194, 230), "silver_dark": (100, 110, 160), "silver_light": (236, 240, 255),
        "gold": (236, 196, 60), "gold_dark": (160, 120, 20), "violet": (130, 90, 170), "violet_dark": (70, 40, 110),
        "red": (220, 50, 50), "mouth": (160, 20, 30), "teal": (70, 200, 180), "black": (30, 30, 36),
        "tooth": (250, 230, 120), "eye": (250, 210, 50)}
SHINY = {"silver": (240, 200, 120), "silver_dark": (170, 120, 50), "silver_light": (255, 240, 200),
         "violet": (60, 120, 200), "violet_dark": (20, 60, 130)}


def P(v):
    return pal(BASE, SHINY, v)


SILVER = armour(P, "silver", "silver_dark", light="silver_light", trim="gold", trim_w=0.3)
GOLD = metal(P, "gold", dark="gold_dark")
CLOAK = fabric(P, "violet", "violet_dark", axis="z", period=2.6)
MANE = strands(P, "silver_light", "silver")


def build():
    m = Model("caturamon")
    mats = {"skin": SILVER, "belly": SILVER, "neck": SILVER, "head": SILVER, "snout": SILVER, "jaw": solid(P, "red"),
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": SILVER, "leg_lower": SILVER,
            "paw": SILVER, "claw": solid(P, "black"), "tail": SILVER}
    a = quadruped(m, mats, "caturamon", length=24.0, body_y=14.0, body_rx=7.0, body_ry=6.4, chest_bulk=1.3,
                  neck=((0, 17, -12), (0, 18, -15)), head_len=10.0, head_w=5.0, head_h=5.0, snout=0.3, mouth_open=16,
                  teeth=4, leg_bulk=1.7, toes=3, tail=((0, 22, 14), (0, 28, 16), (0, 31, 12)),
                  tail_r=(1.6, 1.4, 1.2))
    bd, hd = a["body"], a["head"]
    for sx in (-1, 1):                                                       # gold-rimmed drum plates
        for zz in (-6.0, 6.0):
            m.box(bd, sx * 7.4 - 0.6, 10.0, zz - 4.0, sx * 7.4 + 0.6, 18.0, zz + 4.0, GOLD)
            m.box(bd, sx * 7.6 - 0.6, 11.4, zz - 2.6, sx * 7.6 + 0.6, 16.6, zz + 2.6, SILVER)
        m.box(hd, sx * 2.6 - 0.6, 19.6, -20.1, sx * 2.6 + 0.6, 20.6, -19.9, solid(P, "eye", glow=True))
    for i in range(16):                                                      # the curly mane
        ang = math.radians(i * 22.5)
        base = (5.4 * math.cos(ang), 18.0 + 5.0 * math.sin(ang), -14.0)
        rod(m, hd, base, (base[0] * 1.4, base[1] + 1.4 * math.sin(ang), -11.0), 3, MANE, extend=0.4)
    cl = m.bone("cap", bd, (0, 20, -4))                                      # the violet cloak
    m.box(cl, -8.0, 20.4, -8.0, 8.0, 21.4, 8.0, CLOAK)
    for sx in (-1, 1):
        m.box(cl, min(sx * 7.6, sx * 8.4), 10.0, -8.0, max(sx * 7.6, sx * 8.4), 21.0, 8.0, CLOAK,
              rotation=(0, 0, -sx * 10), pivot=(sx * 8.0, 21.0, 0))
    tl = a["tail"]                                                           # teal spiral tail tip
    e = a["tail_pts"][-1]
    for j in range(5):
        ang = j * 1.2
        rod(m, tl, (e[0], e[1] + 1.4 * math.sin(ang), e[2] - 1.4 * math.cos(ang)),
            (e[0], e[1] + 1.4 * math.sin(ang + 1.2), e[2] - 1.4 * math.cos(ang + 1.2)), 2, solid(P, "teal"), extend=0.3)
    return m
