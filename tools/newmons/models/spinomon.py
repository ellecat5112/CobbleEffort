"""Spinomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the colossal spinosaur: a hulking orange-and-gold scaled dinosaur with a sail of huge serrated silver
blades rising from its back, a long crocodilian head of fangs, crimson-edged armour scales, curved white claws and
talons, and a heavy armoured tail. 35 blocks.

Front is -z, y is up. 60 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import theropod
from _digidetail import metal, scales, skin, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a hulking orange-and-gold spinosaur with a sail of huge serrated silver blades, a long fanged crocodilian head and white claws"
BASE = {"orange": (220, 120, 40), "orange_dark": (140, 60, 14), "gold": (230, 190, 90), "gold_dark": (160, 120, 40),
        "red": (180, 40, 30), "steel": (210, 214, 226), "steel_dark": (100, 104, 120), "claw": (246, 244, 236),
        "eye": (250, 220, 60), "mouth": (150, 30, 40), "tooth": (250, 250, 240)}
SHINY = {"orange": (70, 120, 170), "orange_dark": (24, 60, 100), "gold": (190, 200, 220)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "orange", "red", size=1.8)
BELLY = skin(P, "gold", dark="gold_dark")
STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("spinomon")
    mats = {"skin": HIDE, "belly": BELLY, "snout": HIDE, "jaw": BELLY, "claw": solid(P, "claw"), "talon": solid(P, "claw"),
            "tooth": solid(P, "tooth"), "mouth": solid(P, "mouth")}
    a = theropod(m, mats, "spinomon", chest=(0, 38.0, -4.0), body_r=8.0, chest_r=7.4, neck_top=(0, 48.0, -10.0),
                 head_len=16.0, head_w=4.0, head_h=4.6, mouth_open=16, teeth=8, arm_len=12.0, arm_bulk=1.5, leg_bulk=1.6,
                 tail=((0, 24, 10), (0, 18, 20), (0, 12, 30), (0, 8, 40)), tail_r=(6.0, 4.6, 3.0, 1.8))
    e = a["eye"]
    for sx in (-1, 1):
        m.box(a["head"], min(sx * e[0], sx * (e[0] + 0.2)), e[1] - 0.6, e[2] - 0.8, max(sx * e[0], sx * (e[0] + 0.2)),
              e[1] + 0.6, e[2] + 0.8, solid(P, "eye", glow=True))
    for j in range(7):                                                                   # sail of serrated blades
        z = -8.0 + j * 4.0
        h = 18.0 - abs(j - 3) * 3.0
        m.box(a["body"], -0.8, 40.0 - j * 1.4, z - 2.0, 0.8, 40.0 - j * 1.4 + h, z + 2.0, STEEL,
              rotation=(-15, 0, 0), pivot=(0, 40.0, z))
        for k in range(3):
            spike(m, a["body"], (0, 42.0 + k * 4.0 - j * 1.4, z + 2.0), (0, 0.3, 1), 0.8, 2.0, STEEL, tip=0.8)
    return m
