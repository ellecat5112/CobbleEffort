"""Troopmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a bulky undead foot soldier in a black rubber suit: a gas-mask head with round glass eyepieces, twin
filter canisters and a breathing hose, a spike on its crown, chrome tubes and fittings on its shoulders, spiked
gauntlets and boots, a round heavy belly, and a short whip tail. 15 blocks.

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import leather, metal, solid
from _route import pal, tone

HEIGHT = 65
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a bulky undead soldier in a black rubber suit with a gas-mask head, twin filter canisters, chrome fittings and spiked gauntlets"
BASE = {"black": (44, 42, 48), "black_dark": (16, 14, 18), "chrome": (210, 214, 224), "chrome_dark": (100, 104, 116),
        "glass": (230, 236, 246), "eye": (30, 30, 40), "violet": (140, 90, 190)}
SHINY = {"black": (60, 70, 50), "black_dark": (24, 30, 20)}


def P(v):
    return pal(BASE, SHINY, v)


RUBBER = leather(P, "black", "black_dark")
CHROME = metal(P, "chrome", dark="chrome_dark")


def build():
    m = Model("troopmon")
    mats = {"skin": RUBBER, "chest": RUBBER, "abs": RUBBER, "pelvis": RUBBER, "deltoid": RUBBER, "upper_arm": RUBBER,
            "forearm": RUBBER, "hand": RUBBER, "thigh": RUBBER, "knee": RUBBER, "shin": RUBBER, "calf": RUBBER,
            "foot": RUBBER, "talon": CHROME, "neck": RUBBER}
    a = humanoid(m, mats, bulk=1.45, arm_bulk=1.2, leg_bulk=1.3, talons=True, name="troopmon")
    bd = a["body"]
    ball(m, bd, (0, 37.0, -2.0), 8.0, RUBBER, layers=4)                                 # heavy belly
    for sx in (-1, 1):
        m.round_box(bd, sx * 7.4, 0, 2.0, 2.0, 49.0, 53.0, CHROME, cut=1)
        rod(m, bd, (sx * 7.4, 52.0, 2.0), (sx * 3.0, 56.0, 4.0), 1, CHROME, extend=0.3)
        for nm in ("arm_left", "arm_right"):
            pass
    for nm in ("arm_left", "arm_right"):                                               # spiked gauntlets
        w = a[nm]["wrist"]
        for j in range(3):
            spike(m, a[nm]["bone"], (w[0], w[1] + 2.0 + j * 1.6, w[2] + 1.0), (0, 0.2, 1), 0.9, 2.4, CHROME, tip=0.8)
    for nm in ("leg_left", "leg_right"):
        k = a[nm]["knee"]
        spike(m, a[nm]["bone"], (k[0], k[1], k[2] - 2.0), (0, 0.3, -1), 1.0, 2.6, CHROME, tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 3.4, 3.6, 54.0, 62.0, RUBBER, cut=2)
    for sx in (-1, 1):                                                                  # glass eyepieces
        m.round_box(hd, sx * 1.6, -3.4, 1.4, 0.6, 58.0, 60.6, metal(P, "glass"), cut=0)
        m.round_box(hd, sx * 1.6, -3.6, 0.6, 0.4, 58.8, 59.8, solid(P, "eye"), cut=0)
        m.round_box(hd, sx * 2.6, -4.4, 1.4, 1.4, 54.4, 56.8, CHROME, cut=1)              # filter canisters
    spike(m, hd, (0, 61.6, 0), (0, 1, 0.2), 1.6, 5.0, CHROME, tip=0.8)
    tl = m.bone("tail", bd, (0, 30, 4))
    pts = [(0, 30.0, 4.0), (3.0, 22.0, 10.0), (7.0, 18.0, 13.0), (10.0, 20.0, 15.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, RUBBER, extend=0.3)
    return m
