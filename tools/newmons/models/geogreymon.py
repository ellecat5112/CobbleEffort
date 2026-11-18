"""Geo Greymon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Savers Greymon: a lean, muscular orange tyrannosaur striped with blue, a black horned helmet
banded red over its head, a jaw full of teeth, white claws and a long striped tail. Adult stage, 15 blocks tall.

Front is -z, y is up. 48 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import theropod
from _digidetail import armour, plane, scales, skin, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(15, HEIGHT, 3.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a lean muscular orange tyrannosaur striped blue with a black horned helmet banded red and white claws"
BASE = {"orange": (240, 120, 40), "orange_dark": (160, 60, 14), "orange_light": (255, 180, 110), "blue": (50, 150, 220),
        "black": (40, 38, 44), "black_dark": (14, 14, 18), "red": (200, 30, 40), "claw": (246, 246, 246),
        "mouth": (130, 20, 30), "tooth": (250, 250, 246), "eye": (250, 220, 60), "belly": (250, 200, 140),
        "belly_dark": (200, 140, 80)}
SHINY = {"orange": (60, 60, 70), "orange_dark": (24, 24, 30), "orange_light": (130, 130, 150), "blue": (250, 120, 40)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE0 = scales(P, "orange", "orange_dark", size=1.6, light="orange_light", rim_mix=0.3)


def hidef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    a, b = plane(x, y, z, face)
    if face in ("east", "west", "up", "south") and abs(((b * 0.35 + a * 0.3) % 4.0) - 2.0) < 0.4:
        return tone(p["blue"], face), None
    return HIDE0(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("geogreymon")
    mats = {"skin": hidef, "belly": skin(P, "belly", dark="belly_dark"), "neck": hidef, "head": hidef, "jaw": hidef,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "arm": hidef, "hand": hidef,
            "claw": solid(P, "claw"), "thigh": hidef, "shin": hidef, "foot": hidef, "talon": solid(P, "claw"),
            "tail": hidef}
    a = theropod(m, mats, "geogreymon", hip_y=18.0, chest=(0, 30.0, -2.0), body_r=5.4, chest_r=5.2,
                 neck_top=(0, 38.0, -5.0), head_len=11.0, head_w=3.6, head_h=4.0, mouth_open=22, teeth=8,
                 arm_len=9.0, leg_bulk=1.0, tail=((0, 17, 8), (0, 13, 16), (0, 9, 24), (2, 6, 31)),
                 tail_r=(4.0, 3.0, 2.0, 1.2))
    hd = a["head"]
    hc = a["head_c"]
    ex, ey, ez = a["eye"]
    m.round_box(hd, hc[0], hc[2] - 1.0, 4.0, 5.4, hc[1] - 0.4, hc[1] + 4.6,
                armour(P, "black", "black_dark", trim="red", trim_w=0.4), cut=1)                 # black helmet
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.5)), ey - 0.4, ez - 0.7, max(sx * ex, sx * (ex + 0.5)), ey + 0.4, ez + 0.7,
              solid(P, "eye"))
        spike(m, hd, (sx * 3.4, hc[1] + 3.6, hc[2] + 2.0), (sx * 0.8, 1, 0.4), 1.8, 8.0, solid(P, "black"), tip=0.9)
    spike(m, hd, (0, hc[1] + 4.0, hc[2] - 4.0), (0, 1, -0.6), 1.6, 4.0, solid(P, "black"), tip=0.8)
    bd = a["body"]
    for j in range(4):                                                                 # blue back spikes
        spike(m, bd, (0, 34.0 - j * 4.0, 2.0 + j * 2.0), (0, 0.6, 1), 1.4, 3.0, solid(P, "blue"), tip=0.8)
    return m
