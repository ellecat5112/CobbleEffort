"""Togemogumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Armor Digimon of sincerity: a mole with a great mantle of glassy crystal quills, a navy
armoured snout-helm with a pink nose and a yellow face, a sincerity crest on its shoulder plates, and huge navy
digging claws tipped with ivory talons. 15 blocks.

Front is -z, y is up. Adult stage (Armor).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digidetail import armour, eye, gem, skin, solid
from _route import pal, tone

HEIGHT = 23
SCALE, HITBOX = sized(15, HEIGHT, 3.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a mole with a great mantle of glassy crystal quills, a navy armoured snout-helm, a yellow face and huge ivory-tipped claws"
BASE = {"navy": (40, 60, 110), "navy_dark": (16, 24, 50), "yellow": (240, 220, 120), "yellow_dark": (190, 160, 60),
        "crystal": (210, 236, 250), "crystal_light": (255, 255, 255), "ivory": (250, 240, 210), "pink": (230, 100, 140),
        "eye": (60, 60, 90), "pupil": (10, 10, 20), "white": (255, 255, 255), "crest": (240, 240, 250)}
SHINY = {"navy": (110, 40, 60), "navy_dark": (60, 14, 24)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "navy", "navy_dark", panel=(3.0, 3.0))


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 17.4, y - 21.4, 0.9, "eye")
        if c is not None:
            return c, None
    if y < 19.6:
        return skin(P, "yellow", dark="yellow_dark")(x, y, z, face, variant, box=box, **k)
    return ARM(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("togemogumon")
    mats = {"skin": skin(P, "yellow", dark="yellow_dark"), "belly": skin(P, "yellow", dark="yellow_dark"),
            "neck": ARM, "head": headf, "leg": ARM, "paw": ARM, "claw": solid(P, "ivory"), "tail": ARM}
    a = quadruped(m, mats, "togemogumon", length=20.0, body_y=12.0, body_rx=6.0, body_ry=6.0, chest_bulk=1.2,
                  neck=((0, 16, -10), (0, 19, -13)), head_len=10.0, head_w=4.0, head_h=5.0, snout=0.6, mouth_open=0,
                  tail=((0, 12, 10), (0, 10, 14)), tail_r=(1.6, 1.0), toes=3, claws=True)
    bd, hd = a["body"], a["head"]
    spike(m, hd, (0, 18.6, a["snout_front"]), (0, 0, -1), 1.6, 1.2, solid(P, "pink"), tip=0.8)
    for i in range(7):                                                                 # crystal quill mantle
        for j in range(5):
            ang = (j - 2) * 0.5
            z = -6.0 + i * 3.0
            spike(m, bd, (math.sin(ang) * 5.0, 15.0 + math.cos(ang) * 2.0, z), (math.sin(ang) * 0.8, 1, 0.9), 2.2,
                  7.0 + (3 - abs(i - 3)) * 1.2, gem(P, "crystal", "crystal_light", glow=False), tip=0.8)
    for nm in ("leg_front_left", "leg_front_right"):                                   # big digging claws
        sx = 1 if "left" in nm else -1
        m.round_box(bd, sx * 6.0, -7.0, 2.8, 3.0, 4.0, 10.0, ARM, cut=1)
        for j in range(3):
            spike(m, bd, (sx * 6.0 + (j - 1) * 1.4, 4.0, -9.6), (0, -0.4, -1), 1.2, 4.0, solid(P, "ivory"), tip=0.8)
    return m
