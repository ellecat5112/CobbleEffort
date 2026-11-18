"""Garummon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Legendary Warrior of light's beast spirit: a sleek mechanical wolf in white plating trimmed with
gold and violet lines, a sharp-eared wolf helm with a golden blade crest, golden blade-wings swept back from its
shoulders, wheeled armoured legs with golden claws and a long blade on its back. 25 blocks tall.

Front is -z, y is up. 34 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a sleek mechanical white wolf trimmed in gold and violet, a wolf helm with a golden blade crest, golden "
        "blade-wings, armoured legs with golden claws and a blade on its back")
BASE = {"white": (240, 242, 250), "white_dark": (170, 176, 196), "white_light": (255, 255, 255), "gold": (240, 200, 70),
        "gold_dark": (160, 120, 20), "violet": (120, 90, 200), "eye": (60, 200, 250), "mouth": (60, 50, 70),
        "tooth": (250, 250, 246), "steel": (190, 196, 210), "steel_dark": (90, 96, 110)}
SHINY = {"white": (50, 50, 60), "white_dark": (20, 20, 26), "white_light": (120, 120, 140)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE0 = armour(P, "white", "white_dark", light="white_light", trim="gold", trim_w=0.25)
GOLD = metal(P, "gold", dark="gold_dark")


def platef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and abs((z * 0.5) % 4.0 - 2.0) < 0.12:
        return p["violet"], p["violet"]
    return PLATE0(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("garummon")
    mats = {"skin": platef, "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "claw": GOLD,
            "paw": metal(P, "steel", dark="steel_dark")}
    a = quadruped(m, mats, "garummon", length=30.0, body_y=17.0, body_rx=5.0, body_ry=5.0, chest_bulk=1.3,
                  neck=((0, 21, -13), (0, 24, -17)), head_len=11.0, head_w=3.2, head_h=3.6, snout=0.9,
                  mouth_open=10, teeth=4, leg_bulk=1.4, toes=3, tail=((0, 19, 15), (0, 21, 21), (0, 22, 27)),
                  tail_r=(1.6, 1.2, 0.8))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.8, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.8,
              solid(P, "eye", glow=True))
        spike(m, hd, (sx * 1.8, ey + 3.0, ez + 2.0), (sx * 0.3, 1, 0.6), 1.6, 5.0, platef, tip=0.9)   # wolf ears
        for j in range(3):                                                              # golden blade-wings
            spike(m, bd, (sx * 4.6, 22.0, -6.0 + j * 2.0), (sx * 0.8, 0.5 + j * 0.15, 1.0), 1.6, 14.0 - j * 3.0,
                  GOLD, tip=0.9)
    spike(m, hd, (0, ey + 3.4, ez - 1.0), (0, 0.6, 1), 1.4, 6.0, GOLD, tip=0.9)               # blade crest
    m.box(bd, -0.6, 22.0, -6.0, 0.6, 24.0, 12.0, metal(P, "steel", dark="steel_dark"))      # back blade
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):
        w = a[nm]["wrist"]
        m.round_box(a[nm]["bone"], w[0], w[2], 2.6, 2.6, w[1] - 1.0, w[1] + 2.0, GOLD, cut=1)
    return m
