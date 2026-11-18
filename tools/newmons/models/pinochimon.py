"""Pinochimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the wooden puppet of the Dark Masters: a jointed wooden puppet in blue overalls with brass
fittings, a red helmet-cap with a radiation emblem and a yellow bobble, white gloves, a long pointed wooden nose, a
great wooden cross strapped to its back with red puppet strings, and a hammer whose head is a revolver cylinder. 35
blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import fabric, metal, skin, solid, twisted
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a jointed wooden puppet in blue overalls, a red cap with a yellow bobble, a long pointed nose, a great wooden "
        "cross on its back with red strings and a revolver-cylinder hammer")
BASE = {"wood": (200, 160, 110), "wood_dark": (140, 100, 60), "blue": (60, 90, 170), "blue_dark": (24, 40, 100),
        "red": (210, 40, 40), "red_dark": (130, 14, 14), "yellow": (250, 210, 50), "white": (246, 246, 246),
        "brass": (210, 170, 70), "steel": (200, 204, 214), "steel_dark": (100, 104, 116), "black": (30, 28, 30)}
SHINY = {"wood": (120, 90, 70), "wood_dark": (70, 50, 34), "blue": (150, 60, 60), "blue_dark": (90, 24, 24)}


def P(v):
    return pal(BASE, SHINY, v)


WOOD = twisted(P, "wood", "wood_dark", period=3.0, angle=0.1)


def build():
    m = Model("pinochimon")
    mats = {"skin": WOOD, "chest": fabric(P, "blue", "blue_dark", seam="brass"), "abs": fabric(P, "blue", "blue_dark"),
            "pelvis": fabric(P, "blue", "blue_dark"), "thigh": fabric(P, "blue", "blue_dark"),
            "hand": skin(P, "white", dark="steel_dark"), "finger": skin(P, "white", dark="steel_dark")}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.9, hand_pose="fist", name="pinochimon")
    bd = a["body"]
    for nm in ("arm_left", "arm_right", "leg_left", "leg_right"):                        # brass joints
        anc = a[nm]
        j = anc.get("elbow") or anc.get("knee")
        ball(m, anc["bone"], j, 1.4, metal(P, "brass"), layers=2)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 2.8, 54.0, 59.6, WOOD, cut=1)
    spike(m, hd, (0, 56.6, -3.0), (0, 0, -1), 1.2, 7.0, WOOD, tip=0.8)                      # long pointed nose
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 1.8), 57.6, -3.3, max(sx * 0.8, sx * 1.8), 58.4, -3.1, solid(P, "black"))
    m.round_box(hd, 0, 0, 3.2, 3.2, 59.0, 62.0, fabric(P, "red", "red_dark"), cut=1)        # red cap
    m.box(hd, -1.0, 60.0, -3.3, 1.0, 61.6, -3.1, solid(P, "yellow"))
    ball(m, hd, (0, 63.4, 0), 1.0, solid(P, "yellow"), layers=1)
    rod(m, bd, (0, 22.0, 5.0), (0, 62.0, 5.0), 2, WOOD, extend=0.4, t2=3)                    # wooden cross
    rod(m, bd, (-12.0, 52.0, 5.0), (12.0, 52.0, 5.0), 2, WOOD, extend=0.4, t2=3)
    for sx in (-1, 1):                                                                   # red puppet strings
        rod(m, bd, (sx * 12.0, 52.0, 5.0), (sx * 9.0, 30.0, 0.0), 1, solid(P, "red"), extend=0.0)
    ar = a["arm_right"]                                                                  # revolver-cylinder hammer
    h = ar["hand"]
    rod(m, ar["bone"], (h[0], h[1] + 2.0, h[2]), (h[0], h[1] - 16.0, h[2] - 2.0), 1, metal(P, "steel"), extend=0.2,
        t2=2)
    m.round_box(ar["bone"], h[0], h[2] - 2.0, 3.0, 3.0, h[1] - 20.0, h[1] - 15.0, metal(P, "steel", dark="steel_dark"),
                cut=1)
    for i in range(6):
        ang = 2 * math.pi * i / 6
        m.box(ar["bone"], h[0] + 1.8 * math.cos(ang) - 0.5, h[1] - 20.1, h[2] - 2.0 + 1.8 * math.sin(ang) - 0.5,
              h[0] + 1.8 * math.cos(ang) + 0.5, h[1] - 19.9, h[2] - 2.0 + 1.8 * math.sin(ang) + 0.5, metal(P, "brass"))
    return m
