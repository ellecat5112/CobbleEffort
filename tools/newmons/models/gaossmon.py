"""Gaossmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
little blue shark-headed dinosaur bursting out of the ground: a big toothy jaw with a pale throat, red eyes, a tall
swept dorsal fin, a thick blue hide etched with fine lines and red-tipped claws. Child stage, 1 block tall.

Front is -z, y is up. 28 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import theropod
from _digidetail import scales, skin, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1.0, HEIGHT, 1.6)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 12}
LOOK = "a little blue shark-headed dinosaur with a big toothy jaw, red eyes, a tall swept dorsal fin and red claws"
BASE = {"blue": (50, 70, 170), "blue_dark": (20, 30, 90), "blue_light": (120, 140, 230), "belly": (220, 226, 240),
        "belly_dark": (170, 176, 200), "eye": (210, 30, 40), "mouth": (200, 60, 80), "tooth": (250, 250, 246),
        "claw": (210, 30, 40)}
SHINY = {"blue": (90, 90, 100), "blue_dark": (40, 40, 50), "blue_light": (170, 170, 180)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "blue", "blue_dark", size=1.0, light="blue_light")


def build():
    m = Model("gaossmon")
    mats = {"skin": HIDE, "belly": skin(P, "belly", dark="belly_dark"), "neck": HIDE, "head": HIDE, "jaw": HIDE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "arm": HIDE, "hand": HIDE, "claw": solid(P, "claw"),
            "thigh": HIDE, "shin": HIDE, "foot": HIDE, "talon": solid(P, "claw"), "tail": HIDE}
    a = theropod(m, mats, "gaossmon", hip_y=8.0, chest=(0, 14.0, -1.0), body_r=4.4, chest_r=4.6,
                 neck_top=(0, 18.0, -3.0), head_len=9.0, head_w=4.0, head_h=4.0, mouth_open=26, teeth=6,
                 arm_len=4.0, leg_bulk=0.8, tail=((0, 8, 5), (0, 6, 10), (0, 4, 14)), tail_r=(3.0, 2.0, 1.2))
    hd, bd = a["head"], a["body"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.6,
              solid(P, "eye"))
    for j in range(3):                                                           # tall swept dorsal fin
        spike(m, bd, (0, 18.0 - j * 2.0, 1.0 + j * 2.4), (0, 1, 0.9), 2.4 - j * 0.4, 9.0 - j * 2.0, HIDE, tip=0.8)
    return m
