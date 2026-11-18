"""Lilamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
lilac flower fairy: a slender pale-pink figure whose head is a closed pink flower bud with a green face, long thin arms
ending in white petal hands, a green-and-pink leaf bodice, a white lily blossom floating beside her and long legs
ending in white feather-petal feet. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import cutout, local, skin, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a slender pale-pink flower fairy with a closed pink bud head, a green face, white petal hands and feather-petal feet"
BASE = {"pink": (246, 200, 210), "pink_dark": (210, 140, 160), "bud": (240, 140, 180), "bud_dark": (190, 80, 130),
        "green": (130, 200, 90), "green_dark": (60, 130, 40), "white": (250, 250, 250), "white_dark": (200, 200, 210),
        "yellow": (240, 220, 80), "eye": (40, 40, 40)}
SHINY = {"pink": (210, 220, 250), "pink_dark": (150, 160, 210), "bud": (150, 140, 240), "bud_dark": (90, 80, 190)}


def P(v):
    return pal(BASE, SHINY, v)


SK = skin(P, "pink", dark="pink_dark")


def petal_in(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    a, b = u / max(W, 1e-6) - 0.5, v / max(H, 1e-6)
    return abs(a) < 0.5 * math.sin(math.pi * min(1.0, b)) + 0.02


def build():
    m = Model("lilamon")
    mats = {"skin": SK, "chest": skin(P, "green", dark="green_dark"), "abs": SK, "pelvis": skin(P, "green", dark="green_dark"),
            "neck": SK, "deltoid": skin(P, "bud", dark="bud_dark"), "upper_arm": SK, "forearm": SK,
            "hand": solid(P, "white"), "finger": solid(P, "white"), "thigh": SK, "knee": SK, "shin": SK, "calf": SK,
            "foot": solid(P, "white"), "toe": solid(P, "white")}
    a = humanoid(m, mats, bulk=0.72, arm_bulk=0.7, leg_bulk=0.78, name="lilamon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.2, 2.4, 53.6, 58.6, skin(P, "green", dark="green_dark"), cut=1)       # green face
    m.box(hd, -1.2, 56.0, -3.1, -0.4, 56.6, -3.0, solid(P, "eye"))
    m.box(hd, 0.4, 56.0, -3.1, 1.2, 56.6, -3.0, solid(P, "eye"))
    for i in range(5):                                                                 # closed bud petals
        ang = math.radians(-90 + i * 45)
        m.box(hd, -2.2, 56.0, 0.0, 2.2, 66.0, 0.0, cutout(petal_in, skin(P, "bud", dark="bud_dark")),
              rotation=(-12, math.degrees(ang), 0), pivot=(0, 56.0, 0.6))
    for nm in ("arm_left", "arm_right", "leg_left", "leg_right"):                    # petal hands and feet
        anc = a[nm]
        p = anc.get("hand") or (anc["ankle"][0], 1.0, anc["ankle"][2])
        sx = 1 if p[0] > 0 else -1
        for j in range(4):
            spike(m, anc["bone"], p, (sx * 0.3 + (j - 1.5) * 0.3, -1, -0.3), 1.0, 5.0, solid(P, "white"), tip=0.8)
    lb = m.bone("lily", bd, (12, 46, -2))                                              # floating white lily
    for i in range(6):
        m.box(lb, 10.4, 46.0, -2.0, 13.6, 52.0, -2.0, cutout(petal_in, solid(P, "white")), rotation=(0, 0, i * 60),
              pivot=(12.0, 46.0, -2.0))
    m.round_box(lb, 12.0, -2.4, 0.8, 0.4, 45.2, 46.8, solid(P, "yellow"), cut=0)
    return m
