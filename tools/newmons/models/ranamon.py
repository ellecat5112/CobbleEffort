"""Ranamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the warrior of the water spirit: a slender pale-green frog-girl in a blue-and-white water bodysuit
with leggings and a short skirt, a frog-hood helmet set with big red jewel eyes and a curling tail-fin, blue fin
cuffs, a jewelled water sash at her hip, and webbed feet. 15 blocks.

Front is -z, y is up. 60 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, fabric, gem, skin, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a slender pale-green frog-girl in a blue-and-white water bodysuit with a frog-hood helmet set with big red jewel eyes"
BASE = {"green": (170, 220, 180), "green_dark": (110, 170, 130), "blue": (60, 120, 210), "blue_dark": (24, 60, 140),
        "white": (240, 246, 252), "white_dark": (190, 200, 220), "red": (220, 60, 40), "eye": (230, 80, 40),
        "black": (24, 24, 30)}
SHINY = {"green": (230, 200, 230), "green_dark": (180, 140, 180), "blue": (200, 60, 120), "blue_dark": (130, 20, 70)}


def P(v):
    return pal(BASE, SHINY, v)


def suitf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(math.sin(y * 0.5 + x * 0.3)) > 0.82:
        return tone(p["white"], face), None
    return fabric(P, "blue", "blue_dark", axis="y", period=2.6)(x, y, z, face, variant, box=box, **k)


SKIN = skin(P, "green", dark="green_dark", var=0.03)


def build():
    m = Model("ranamon")
    mats = {"skin": suitf, "neck": SKIN, "hand": SKIN, "finger": SKIN, "foot": SKIN, "forearm": SKIN}
    a = humanoid(m, mats, bulk=0.7, arm_bulk=0.7, leg_bulk=0.75, name="ranamon")
    bd = a["body"]
    m.round_box(bd, 0, 0.4, 5.0, 3.8, 27.0, 32.0, suitf, cut=1)                             # short skirt
    m.round_box(bd, 0, 0, 4.6, 3.6, 31.0, 33.0, solid(P, "white"), cut=1)                  # water sash
    m.box(bd, 2.0, 30.6, -3.9, 4.0, 32.6, -3.6, gem(P, "red", "white"))
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.2, 2.4, 54.0, 59.0, SKIN, cut=1)
    m.box(hd, -1.4, 56.4, -2.9, -0.6, 57.2, -2.7, solid(P, "black"))
    m.box(hd, 0.6, 56.4, -2.9, 1.4, 57.2, -2.7, solid(P, "black"))
    m.round_box(hd, 0, 0, 3.0, 3.2, 57.6, 61.0, armour(P, "blue", "blue_dark", trim="white", trim_w=0.3), cut=1)
    for sx in (-1, 1):                                                                   # jewel eyes on the hood
        m.round_box(hd, sx * 1.6, -2.6, 1.2, 0.8, 59.0, 61.6, gem(P, "eye", "white"), cut=0)
        spike(m, hd, (sx * 3.0, 59.0, 0), (sx * 1, 0.2, 0.2), 1.0, 2.6, solid(P, "blue"), tip=0.8)
    pts = [(0, 61.0, 2.6), (2.0, 64.0, 5.0), (6.0, 63.0, 6.0), (7.0, 60.0, 5.0)]             # curling hood fin
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, hd, p0, p1, 1, armour(P, "blue", "blue_dark"), extend=0.2, t2=2)
    for side in ("arm_left", "arm_right"):                                               # fin cuffs
        w = a[side]["wrist"]
        m.round_box(a[side]["bone"], w[0], w[2], 1.6, 1.6, w[1] + 1.0, w[1] + 3.0, solid(P, "blue"), cut=0)
    for side in ("leg_left", "leg_right"):
        k_ = a[side]["knee"]
        m.round_box(a[side]["bone"], k_[0], k_[2], 2.2, 2.2, k_[1] - 6.0, k_[1] - 3.0, solid(P, "blue"), cut=1)
    return m
