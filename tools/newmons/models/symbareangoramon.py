"""Symbare Angoramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the angora rabbit brawler: a stocky beast-man with a huge white-and-cream angora fur ruff
and face, long rabbit ears that sweep out like twin green-patterned blades, a brown leather jacket, big orange boxing
gloves, baggy black trousers, and black boots. 15 blocks.

Front is -z, y is up. 72 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import fabric, fur, leather, solid
from _route import pal, tone

HEIGHT = 72
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a stocky angora rabbit brawler with a huge cream fur ruff, long blade-like green-patterned ears, a leather jacket and orange boxing gloves"
BASE = {"cream": (250, 240, 210), "cream_dark": (200, 186, 150), "white": (250, 250, 250), "ear": (230, 230, 190),
        "ear_mark": (110, 160, 80), "brown": (130, 90, 60), "brown_dark": (80, 50, 30), "orange": (240, 140, 50),
        "orange_dark": (170, 80, 20), "black": (36, 34, 38), "black_dark": (12, 12, 14), "eye": (60, 50, 40)}
SHINY = {"cream": (200, 200, 220), "cream_dark": (140, 140, 170), "orange": (90, 150, 230), "orange_dark": (30, 80, 170)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "cream", "cream_dark", length=1.8)


def earf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(((y + abs(x) * 0.6) % 4.0) - 2.0) < 0.3:
        return tone(p["ear_mark"], face), None
    return tone(p["ear"], face), None


def build():
    m = Model("symbareangoramon")
    mats = {"skin": leather(P, "brown", "brown_dark"), "neck": FUR, "pelvis": fabric(P, "black", "black_dark", axis="y"),
            "thigh": fabric(P, "black", "black_dark", axis="y"), "knee": fabric(P, "black", "black_dark"),
            "shin": fabric(P, "black", "black_dark"), "foot": leather(P, "black", "black_dark"),
            "hand": leather(P, "orange", "orange_dark"), "finger": leather(P, "orange", "orange_dark")}
    a = humanoid(m, mats, bulk=1.1, arm_bulk=1.2, leg_bulk=1.15, name="symbareangoramon")
    bd = a["body"]
    m.round_box(bd, 0, 0, 7.6, 6.0, 44.0, 54.0, FUR, cut=3)                                  # huge fur ruff
    hd = m.bone("head", bd, (0, 55, 0))
    ball(m, hd, (0, 57.0, -0.6), 4.0, FUR, layers=3)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.0), 57.4, -4.5, max(sx * 0.8, sx * 2.0), 58.0, -4.3, solid(P, "eye"))
        pts = [(sx * 1.6, 60.0, 0), (sx * 7.0, 66.0, 2.0), (sx * 14.0, 70.0, 4.0)]          # blade ears
        for p0, p1 in zip(pts, pts[1:]):
            m.box(hd, min(p0[0], p1[0]) - 1.0, min(p0[1], p1[1]), p0[2] - 0.6, max(p0[0], p1[0]) + 1.0,
                  max(p0[1], p1[1]) + 2.0, p0[2] + 0.6, earf)
    for side in ("arm_left", "arm_right"):                                               # big boxing gloves
        ball(m, a[side]["bone"], a[side]["hand"], 3.4, leather(P, "orange", "orange_dark"), layers=3)
    return m
