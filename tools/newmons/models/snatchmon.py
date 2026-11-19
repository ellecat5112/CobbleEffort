"""Snatchmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a sly purple thief: a lean violet body strapped with black harness belts, a crescent-moon hood
sweeping up and back over a dark face with one white eye, a long whip tail, and big pale-blue crystal claws that
snatch at anything that glitters. 15 blocks.

Front is -z, y is up. 66 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, gem, leather, metal, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a sly lean violet thief strapped with black belts, a crescent-moon hood, a long whip tail and big pale-blue crystal claws"
BASE = {"violet": (100, 60, 170), "violet_dark": (40, 20, 90), "black": (24, 22, 28), "white": (250, 250, 250),
        "crystal": (130, 220, 250), "steel": (200, 204, 216)}
SHINY = {"violet": (40, 130, 120), "violet_dark": (14, 70, 60)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "violet", "violet_dark")


def build():
    m = Model("snatchmon")
    mats = {"skin": ARM, "hand": ARM, "finger": gem(P, "crystal", "white"), "claw": gem(P, "crystal", "white"),
            "talon": solid(P, "black")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.85, leg_bulk=0.85, claws=True, talons=True, digitigrade=True,
                 name="snatchmon")
    bd = a["body"]
    for sx in (-1, 1):                                                                   # harness belts
        m.box(bd, sx * 2.0 - 0.6, 32.0, -4.4, sx * 2.0 + 0.6, 51.0, -3.8, leather(P, "black", "black"),
              rotation=(0, 0, sx * 20), pivot=(sx * 2.0, 42.0, -4.1))
    m.round_box(bd, 0, 0, 4.6, 3.6, 34.0, 35.6, leather(P, "black", "black"), cut=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.6, 54.0, 60.0, solid(P, "black"), cut=1)
    m.box(hd, 0.6, 57.0, -3.1, 1.8, 58.4, -2.9, solid(P, "white", glow=True))
    pts = [(0, 60.0, -2.0), (0, 66.0, -1.0), (0, 70.0, 4.0), (0, 68.0, 12.0), (0, 62.0, 16.0)]   # crescent hood
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, hd, p0, p1, 4 - i // 2, ARM, extend=0.6)
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.4, 58.0, 0), (sx * 0.8, 0.4, 0.4), 1.2, 6.0, ARM, tip=0.8)
    for side in ("arm_left", "arm_right"):                                               # big crystal claws
        h = a[side]["hand"]
        sx = 1 if side == "arm_left" else -1
        for f in range(4):
            spike(m, a[side]["bone"], (h[0] + (f - 1.5) * 0.8, h[1], h[2]), ((f - 1.5) * 0.3 + sx * 0.3, -1, -0.6), 1.2,
                  6.0, gem(P, "crystal", "white"), tip=0.8)
    tl = m.bone("tail", bd, (0, 32, 3))
    pts = [(0, 32.0, 3.0), (4.0, 20.0, 12.0), (2.0, 8.0, 18.0), (-4.0, 4.0, 22.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, ARM, extend=0.2, t2=2)
    spike(m, tl, pts[-1], (-1, 0, 0.4), 1.0, 3.0, ARM, tip=0.8)
    return m
