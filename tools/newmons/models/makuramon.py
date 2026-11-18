"""Makuramon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
monkey of the Twelve Devas: a lanky brown monkey with a pale face, big round eyes and a wide grin, a violet cap marked
with a kanji, a red neckerchief, a white tunic with gold buttons, puffy white trousers, silver bracers, big grey
gloves and brown shoes, and a long curling tail. 25 blocks tall.

Front is -z, y is up. 56 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fabric, fur, leather, metal, skin, solid
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(25, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a lanky brown monkey with a pale grinning face, a violet kanji cap, a red neckerchief, a white tunic and puffy trousers and big grey gloves"
BASE = {"brown": (130, 90, 60), "brown_dark": (70, 44, 24), "face": (240, 220, 190), "face_dark": (200, 170, 140),
        "violet": (110, 70, 160), "violet_dark": (60, 30, 100), "red": (200, 40, 40), "white": (246, 244, 236),
        "white_dark": (190, 186, 170), "gold": (230, 190, 60), "silver": (200, 204, 216), "silver_dark": (100, 104, 116),
        "grey": (80, 80, 90), "grey_dark": (40, 40, 46), "eye": (24, 20, 20)}
SHINY = {"brown": (200, 200, 210), "brown_dark": (130, 130, 146)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "brown", "brown_dark", length=0.8)
TUNIC = fabric(P, "white", "white_dark")


def tunicf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 0.4 and (y % 3.0) < 1.0:
        return tone(p["gold"], face), None
    return TUNIC(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("makuramon")
    mats = {"skin": FUR, "chest": tunicf, "abs": tunicf, "pelvis": TUNIC, "neck": FUR, "deltoid": TUNIC,
            "upper_arm": FUR, "forearm": metal(P, "silver", dark="silver_dark"), "hand": leather(P, "grey", "grey_dark"),
            "finger": leather(P, "grey", "grey_dark"), "thigh": TUNIC, "knee": TUNIC, "shin": TUNIC, "calf": TUNIC,
            "foot": leather(P, "brown", "brown_dark"), "toe": leather(P, "brown", "brown_dark")}
    a = humanoid(m, mats, bulk=0.82, arm_bulk=0.85, leg_bulk=1.0, name="makuramon")
    bd = a["body"]
    m.round_box(bd, 0, -0.4, 2.6, 2.6, 50.0, 52.0, solid(P, "red"), cut=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 3.0, 3.0, 53.4, 60.4, FUR, cut=1)
    m.round_box(hd, 0, -2.6, 2.4, 0.8, 54.0, 59.6, skin(P, "face", dark="face_dark"), cut=0)
    for sx in (-1, 1):
        m.round_box(hd, sx * 1.2, -3.3, 0.8, 0.2, 57.2, 58.8, solid(P, "eye"), cut=0)
        m.round_box(hd, sx * 3.6, 0, 1.0, 1.0, 56.0, 58.4, skin(P, "face", dark="face_dark"), cut=0)
    m.box(hd, -1.6, 55.0, -3.3, 1.6, 55.4, -3.2, solid(P, "eye"))
    m.round_box(hd, 0, 0.2, 3.2, 3.2, 59.4, 63.0, fabric(P, "violet", "violet_dark"), cut=2)      # violet cap
    m.round_box(hd, 0, -3.3, 1.0, 0.2, 60.4, 62.0, solid(P, "white"), cut=0)
    for nm in ("arm_left", "arm_right"):                                              # big gloves
        hx, hy, hz = a[nm]["hand"]
        m.round_box(a[nm]["bone"], hx, hz, 2.6, 2.6, hy - 3.0, hy + 1.0, leather(P, "grey", "grey_dark"), cut=1)
    tb = m.bone("tail", bd, (0, 32, 3))
    pts = [(0, 32.0, 3.4), (3.0, 26.0, 9.0), (6.0, 32.0, 13.0), (5.0, 38.0, 11.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 1, FUR, extend=0.3, t2=1)
    return m
