"""Paildramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the DNA Digivolution of Ex-Veemon and Stingmon: a powerful blue dragon-man hunched on clawed legs,
black insect armour plates with spikes over its chest, shoulders and arms, a red helm with a long black horn, white
bat-like wings, long red-banded steel claws on its hands, twin gun barrels at its hips and a blue tail. 25 blocks tall.

Front is -z, y is up. 60 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing
from _digibody import humanoid
from _digidetail import armour, metal, skin, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a powerful blue dragon-man in black spiked insect armour, a red horned helm, white bat-like wings, long steel "
        "claws, twin hip guns and a blue tail")
BASE = {"blue": (60, 110, 210), "blue_dark": (20, 50, 130), "white": (240, 240, 246), "black": (40, 40, 48),
        "black_dark": (12, 12, 16), "red": (200, 40, 40), "steel": (210, 214, 226), "steel_dark": (100, 104, 116),
        "green": (60, 120, 70), "eye": (250, 200, 40)}
SHINY = {"blue": (110, 170, 90), "blue_dark": (40, 100, 30), "black": (120, 40, 40), "black_dark": (60, 14, 14)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "blue", dark="blue_dark")
ARM = armour(P, "black", "black_dark", trim="green", trim_w=0.25)
STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("paildramon")
    mats = {"skin": SKIN, "chest": ARM, "deltoid": ARM, "forearm": ARM, "knee": ARM, "claw": STEEL, "talon": STEEL}
    a = humanoid(m, mats, bulk=1.15, arm_bulk=1.15, leg_bulk=1.15, claws=True, talons=True, digitigrade=True,
                 name="paildramon")
    bd = a["body"]
    for sx in (-1, 1):                                                                   # spiked plates
        for j in range(3):
            spike(m, bd, (sx * 7.6, 50.0 - j * 1.6, 0.6 * j), (sx * 0.8, 0.7, 0.3), 1.4, 4.0, ARM, tip=0.8)
        rod(m, bd, (sx * 5.0, 31.0, -1.0), (sx * 6.0, 28.0, -8.0), 2, STEEL, extend=0.3)   # twin hip guns
    hd = m.bone("head", bd, (0, 55, -1))
    m.round_box(hd, 0, -2.0, 2.6, 3.6, 53.6, 59.6, armour(P, "red", "black"), cut=1)       # red helm
    m.round_box(hd, 0, -5.6, 1.8, 2.0, 54.0, 56.6, SKIN, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.4), 57.4, -5.7, max(sx * 1.0, sx * 2.4), 58.2, -5.5, solid(P, "eye", glow=True))
    spike(m, hd, (0, 58.4, -5.0), (0, 0.3, -1), 1.4, 9.0, solid(P, "black"), tip=0.8)      # long black horn
    for nm in ("arm_left", "arm_right"):                                                 # long banded claws
        h = a[nm]["hand"]
        sx = 1 if h[0] > 0 else -1
        for f in range(3):
            spike(m, a[nm]["bone"], (h[0] + (f - 1) * 0.9, h[1] - 1.0, h[2] - 1.0), (sx * 0.2, -1, -0.4), 1.0, 8.0,
                  STEEL, tip=0.8)
    wb = m.bone("wings", bd, (0, 48, 3))
    for side in (1, -1):
        bat_wing(m, wb, (side * 3.0, 48.0, 3.0), 18.0, 14.0, 3, solid(P, "steel"), solid(P, "white"), side=side,
                 sweep=20)
    tb = m.bone("tail", bd, (0, 31, 3))
    rod(m, tb, (0, 31.0, 3.0), (0, 22.0, 12.0), 3, SKIN, extend=0.4)
    rod(m, tb, (0, 22.0, 12.0), (0, 18.0, 18.0), 2, SKIN, extend=0.3)
    return m
