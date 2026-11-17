"""Bakumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a holy tapir that eats nightmares. A brown furred body with a blue belly and legs, a long silver
armoured mask over its snout with gold scroll engraving and a big blue eye, two ivory tusks, gold bands on its legs,
pointed ears and a trailing wisp of dream-smoke for a tail. 1 block tall.

Front is -z, y is up. 30 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digidetail import armour, eye, fur, metal, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.0)
KIND = "quadruped"
K = 4
ANIM = {"leg_amp": 16}
LOOK = ("a holy tapir: brown fur, blue belly and legs, a long silver armoured mask with gold engraving and a big blue "
        "eye, ivory tusks, gold leg bands and a wisp of dream-smoke for a tail")
BASE = {"brown": (140, 80, 40), "brown_dark": (80, 44, 20), "brown_light": (200, 140, 90), "blue": (110, 140, 220),
        "blue_dark": (60, 80, 160), "silver": (210, 214, 226), "silver_dark": (110, 114, 128), "gold": (236, 196, 60),
        "gold_dark": (160, 120, 30), "ivory": (246, 236, 210), "smoke": (230, 230, 236, 200), "eye": (80, 170, 240),
        "pupil": (16, 20, 30), "white": (250, 250, 250), "mouth": (110, 40, 40), "tooth": (250, 250, 246)}
SHINY = {"brown": (60, 60, 80), "brown_dark": (30, 30, 40), "brown_light": (120, 120, 150), "blue": (220, 140, 190),
         "blue_dark": (160, 80, 130)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "brown", "brown_dark", tip="brown_light", length=1.4)
BLUE = fur(P, "blue", "blue_dark", length=1.0)
MASK = armour(P, "silver", "silver_dark", trim="gold", trim_w=0.4)


def maskf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 13.0, y - 16.0, 1.4, "eye")
        if c is not None:
            return c, None
    return MASK(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("bakumon")
    mats = {"skin": FUR, "belly": BLUE, "neck": FUR, "head": maskf, "snout": MASK, "jaw": BLUE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": FUR, "leg_lower": BLUE, "paw": BLUE,
            "claw": solid(P, "ivory"), "tail": FUR}
    a = quadruped(m, mats, "bakumon", length=18.0, body_y=10.0, body_rx=5.6, body_ry=5.4,
                  chest_bulk=1.1, neck=((0, 13, -9), (0, 15, -11)), head_len=9.0, head_w=3.6, head_h=4.0,
                  snout=0.8, mouth_open=4, teeth=0, leg_bulk=1.2, toes=2, tail=((0, 12, 10), (0, 12, 12)),
                  tail_r=(1.0, 0.8))
    hd = a["head"]
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.4, 13.0, -16.0), (sx * 0.3, -0.6, -1), 1.2, 3.0, solid(P, "ivory"))       # tusks
        spike(m, hd, (sx * 2.6, 18.0, -10.0), (sx * 0.5, 1, 0.4), 1.6, 3.6, FUR)                       # ears
    for nm in ("leg_front_left", "leg_front_right"):
        w = a[nm]["wrist"]
        m.round_box(a[nm]["bone"], w[0], w[2], 2.4, 2.4, 3.6, 4.8, metal(P, "gold", dark="gold_dark"), cut=1)
    tl = a["tail"]
    for j in range(5):                                           # trailing dream-smoke
        ball(m, tl, (j * 0.6 - 1.0, 12.0 + j * 0.5, 11.0 + j * 2.4), 1.0 + j * 0.3, solid(P, "smoke"), layers=2)
    return m
