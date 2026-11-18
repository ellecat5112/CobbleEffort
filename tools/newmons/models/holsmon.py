"""Holsmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
Armor griffin of love: a crouching beast with a white eagle head in a blue-marked helmet-mask, swept white wing-blades
on its back, a red-brown feathered body and tail plume, black-feathered chest, orange clawed legs with white talons
and red claws on its hind feet. Adult stage, 15 blocks long.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, feathers, scales, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a crouching griffin with a white eagle head in a blue-marked helmet-mask, swept white wing-blades, a red-brown "
        "feathered body and orange clawed legs")
BASE = {"brown": (180, 60, 30), "brown_dark": (110, 30, 10), "white": (246, 246, 250), "white_dark": (190, 192, 206),
        "blue": (40, 80, 170), "black": (40, 36, 40), "orange": (240, 160, 40), "orange_dark": (180, 100, 10),
        "talon": (246, 246, 246), "red": (210, 40, 70), "beak": (240, 200, 70), "eye": (60, 120, 220)}
SHINY = {"brown": (60, 110, 180), "brown_dark": (20, 60, 120)}


def P(v):
    return pal(BASE, SHINY, v)


FEATH = feathers(P, "brown", "brown_dark", size=(1.2, 2.0))


def maskf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west") and abs(((x + z) * 0.6) % 3.0 - 1.5) < 0.25:
        return tone(p["blue"], face), None
    return armour(P, "white", "white_dark", trim="blue")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("holsmon")
    mats = {"skin": FEATH, "belly": feathers(P, "black", "black"), "neck": FEATH, "head": maskf, "snout": solid(P, "beak"),
            "jaw": solid(P, "beak"), "mouth": solid(P, "red"), "tooth": solid(P, "beak"),
            "leg_lower": scales(P, "orange", "orange_dark", size=0.8), "paw": scales(P, "orange", "orange_dark"),
            "claw": solid(P, "talon")}
    a = quadruped(m, mats, "holsmon", length=28.0, body_y=13.0, body_rx=5.0, body_ry=5.0, chest_bulk=1.2,
                  neck=((0, 17, -12), (0, 20, -16)), head_len=8.0, head_w=3.0, head_h=3.4, snout=0.5, mouth_open=6,
                  teeth=0, leg_bulk=1.3, toes=3, tail=((0, 16, 14), (0, 19, 20), (2, 22, 26)), tail_r=(2.0, 1.6, 1.2))
    bd = a["body"]
    for side in (1, -1):                                                               # swept white wing-blades
        for j in range(2):
            spike(m, bd, (side * 3.0, 19.0 - j * 2.0, -4.0 + j * 3.0), (side * 0.6, 0.3, 1), 2.0, 16.0 - j * 4.0,
                  armour(P, "white", "white_dark", trim="blue"), tip=0.9)
    e = a["tail_pts"][-1]
    for j in range(5):
        spike(m, a["tail"], e, (0.3 * (j - 2), 0.4, 1), 1.4, 6.0, FEATH, tip=0.8)
    return m
