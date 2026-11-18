"""Raptordramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a cyborg raptor-dragon: a lean grey steel frame with blue armour plates on its chest and
flanks, a long-jawed skull-like steel head with fangs, ribbed cables along its neck, swept black-and-grey blade-wings,
yellow clawed legs, and a long tail streaming into a plume of yellow fur. 15 blocks.

Front is -z, y is up. 36 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, fur, metal, solid
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a lean grey cyborg raptor-dragon with blue chest plates, a long fanged steel head, swept blade-wings and a yellow fur tail plume"
BASE = {"steel": (150, 154, 166), "steel_dark": (70, 74, 86), "blue": (50, 80, 170), "blue_dark": (20, 34, 100),
        "yellow": (250, 200, 50), "yellow_dark": (200, 140, 20), "black": (30, 30, 36), "tooth": (240, 240, 230),
        "eye": (240, 60, 40), "mouth": (150, 30, 40)}
SHINY = {"steel": (200, 170, 120), "steel_dark": (120, 90, 50), "blue": (170, 40, 50), "blue_dark": (100, 14, 20)}


def P(v):
    return pal(BASE, SHINY, v)


STEEL = metal(P, "steel", dark="steel_dark")
BLUE = armour(P, "blue", "blue_dark", trim="steel", trim_w=0.2)
YEL = fur(P, "yellow", "yellow_dark", length=1.4)


def build():
    m = Model("raptordramon")
    mats = {"skin": STEEL, "belly": BLUE, "head": STEEL, "neck": STEEL, "tooth": solid(P, "tooth"),
            "mouth": solid(P, "mouth"), "paw": solid(P, "yellow"), "leg_lower": solid(P, "yellow"), "claw": solid(P, "black"),
            "tail": STEEL}
    a = quadruped(m, mats, "raptordramon", length=24.0, body_y=16.0, body_rx=5.0, body_ry=5.0, neck=((0, 22, -14),
                  (0, 26, -19)), head_len=11.0, head_w=3.0, head_h=3.6, snout=0.7, teeth=6, tail=((0, 18, 12),
                  (0, 18, 20), (0, 16, 26)), tail_r=(2.2, 1.6, 1.0))
    bd = a["body"]
    m.round_box(bd, 0, -4.0, 4.6, 5.0, 12.0, 20.0, BLUE, cut=1)                             # blue chest plates
    hd = a["head"]
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 3.0, sx * 3.3))
        m.box(hd, x0, 27.0, -23.0, x1, 27.8, -21.6, solid(P, "eye", glow=True))
        for j in range(4):                                                               # swept blade-wings
            spike(m, bd, (sx * 4.0, 20.0, -6.0 + j * 1.6), (sx * (0.8 - j * 0.1), 0.6, 0.6 + j * 0.2), 1.4,
                  16.0 - j * 2.0, STEEL if j % 2 else solid(P, "black"), tip=0.8)
    for j in range(5):                                                                   # neck cables
        rod(m, a["neck"], (0, 21.0 + j * 1.0, -12.0 - j * 1.4), (0, 22.0 + j * 1.0, -12.0 - j * 1.4), 1, STEEL,
            extend=0.0, t2=1)
    tb = m.bone("tail_plume", "tail", (0, 16, 26))
    for j in range(6):                                                                   # yellow fur plume
        spike(m, tb, (0, 16.0, 26.0), ((j - 2.5) * 0.25, 0.1 * (j % 3), 1), 2.2, 10.0 - abs(j - 2.5), YEL, tip=0.8)
    return m
