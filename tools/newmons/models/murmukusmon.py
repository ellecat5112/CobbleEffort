"""Murmukusmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a demon lord of greed in green and silver: a horned helm over a wrapped green face, a long green
scarf, silver-and-green armour on its chest and shoulders, one enormous gleaming blue fist, legs striped violet and
white with gold knee bands and black claw feet, a ragged crimson bat wing and a red barbed tail. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage (Demon Lord size).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, bat_wing
from _digibody import humanoid
from _digidetail import armour, fabric, metal, skin, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a demon lord in green and silver armour with a horned helm, a long green scarf, one enormous blue fist, violet-"
        "and-white striped legs, a crimson bat wing and a barbed tail")
BASE = {"green": (90, 150, 70), "green_dark": (40, 80, 30), "silver": (210, 214, 226), "silver_dark": (110, 116, 130),
        "blue": (150, 170, 240), "blue_dark": (60, 80, 170), "violet": (110, 100, 170), "white": (236, 236, 244),
        "gold": (230, 190, 70), "black": (30, 28, 34), "red": (190, 30, 40), "red_dark": (100, 10, 16),
        "eye": (240, 220, 60)}
SHINY = {"green": (170, 60, 140), "green_dark": (100, 20, 80), "red": (60, 70, 170), "red_dark": (20, 26, 100)}


def P(v):
    return pal(BASE, SHINY, v)


GREEN = armour(P, "green", "green_dark", trim="silver", trim_w=0.25)
SILVER = armour(P, "silver", "silver_dark", trim="green", trim_w=0.25)


def legf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["violet"] if (y % 3.0) < 1.5 else p["white"], face), None


def build():
    m = Model("murmukusmon")
    mats = {"skin": GREEN, "chest": SILVER, "abs": GREEN, "pelvis": GREEN, "neck": fabric(P, "green", "green_dark"),
            "deltoid": SILVER, "upper_arm": GREEN, "forearm": SILVER, "hand": GREEN, "finger": GREEN,
            "claw": solid(P, "black"), "thigh": legf, "knee": metal(P, "gold"), "shin": legf, "calf": legf,
            "foot": solid(P, "black"), "talon": solid(P, "black")}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=0.95, leg_bulk=0.95, claws=True, talons=True, digitigrade=True,
                 name="murmukusmon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 2.8, 54.0, 60.0, fabric(P, "green", "green_dark"), cut=1)   # wrapped face
    m.box(hd, -1.8, 57.0, -3.3, 1.8, 57.8, -3.1, solid(P, "eye", glow=True))
    m.round_box(hd, 0, 0.0, 3.0, 3.2, 58.0, 61.4, SILVER, cut=1)                          # horned helm
    for sx in (-1, 1):
        pts = [(sx * 2.6, 60.0, 0), (sx * 5.0, 63.0, 0.6), (sx * 5.4, 67.0, 1.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 2 - j, solid(P, "red"), extend=0.3)
    m.box(bd, 1.0, 36.0, 3.2, 4.0, 53.0, 3.6, fabric(P, "green", "green_dark"))           # long scarf
    al = a["arm_left"]                                                                   # enormous blue fist
    w = al["wrist"]
    ball(m, al["bone"], (w[0] + 1.0, w[1] - 3.0, w[2] - 1.0), 5.6, metal(P, "blue", dark="blue_dark"), layers=5)
    for f in range(4):
        m.round_box(al["bone"], w[0] + 1.0 + (f - 1.5) * 2.4, w[2] - 6.4, 1.1, 1.2, w[1] - 4.0, w[1] + 0.6,
                    metal(P, "blue", dark="blue_dark"), cut=0)
    wb = m.bone("wing_right", bd, (-3.0, 48.0, 3.0))                                     # ragged crimson wing
    bat_wing(m, wb, (-3.0, 48.0, 3.0), 22.0, 20.0, 4, solid(P, "red_dark"), fabric(P, "red", "red_dark"), side=-1,
             sweep=18)
    tb = m.bone("tail", bd, (0, 31, 3))                                                  # barbed tail
    pts = [(0, 31.0, 3.0), (2.0, 22.0, 8.0), (5.0, 14.0, 10.0), (8.0, 8.0, 9.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 1, solid(P, "red"), extend=0.2, t2=1)
    spike(m, tb, pts[-1], (0.4, -0.6, -0.2), 1.6, 3.0, solid(P, "red"), tip=0.8)
    return m
