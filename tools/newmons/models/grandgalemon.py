"""Grand Galemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Galemon grown into an armoured storm-dragon knight: a green dragon in teal plate scrolled
with gold, a beaked helm under a red crest, white fur at its neck, great teal wings edged black, red claws, a long
green tail, and a heavy golden war-hammer with red flanges. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digibody import humanoid
from _digidetail import armour, feathers, fur, metal, scales, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a green dragon knight in gold-scrolled teal plate, a beaked helm with a red crest, great teal wings, red claws "
        "and a heavy golden war-hammer")
BASE = {"teal": (30, 130, 110), "teal_dark": (10, 70, 60), "teal_light": (90, 200, 180), "gold": (240, 200, 70),
        "gold_dark": (160, 120, 20), "green": (60, 150, 80), "green_dark": (24, 90, 40), "red": (210, 30, 40),
        "black": (30, 28, 32), "white": (246, 246, 246), "white_dark": (190, 190, 200), "beak": (230, 220, 200),
        "eye": (250, 220, 60)}
SHINY = {"teal": (60, 60, 140), "teal_dark": (24, 24, 80), "teal_light": (120, 120, 210), "green": (90, 90, 170)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "teal", "teal_dark", light="teal_light", trim="gold", trim_w=0.3)
HIDE = scales(P, "green", "green_dark", size=1.4)
GOLD = metal(P, "gold", dark="gold_dark")


def build():
    m = Model("grandgalemon")
    mats = {"skin": HIDE, "chest": ARM, "deltoid": ARM, "forearm": ARM, "hand": HIDE, "finger": HIDE,
            "claw": solid(P, "red"), "thigh": ARM, "knee": ARM, "shin": ARM, "calf": ARM, "foot": HIDE,
            "talon": solid(P, "red")}
    a = humanoid(m, mats, bulk=1.05, arm_bulk=1.05, leg_bulk=1.05, claws=True, talons=True, digitigrade=True,
                 name="grandgalemon")
    bd = a["body"]
    m.round_box(bd, 0, 0, 6.6, 5.0, 50.0, 53.6, fur(P, "white", "white_dark", length=1.2), cut=2)
    hd = m.bone("head", bd, (0, 55, -1))
    m.round_box(hd, 0, -1.0, 2.8, 3.4, 53.0, 60.0, ARM, cut=1)
    spike(m, hd, (0, 56.0, -4.4), (0, -0.5, -1), 2.2, 5.0, solid(P, "beak"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.4, sx * 2.9), 57.6, -3.4, max(sx * 1.4, sx * 2.9), 58.4, -2.6, solid(P, "eye", glow=True))
    for j in range(5):
        spike(m, hd, (0, 59.6 - j * 0.4, -2.0 + j * 1.4), (0, 1, 0.6), 1.2, 6.0 - j, solid(P, "red"), tip=0.8)
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 4.0, 49.0, 4.0))
        feather_wing(m, wb, (side * 4.0, 49.0, 4.0), 28.0, 12.0, 3, feathers(P, "teal", "teal_dark", tip="black"),
                     side=side, sweep=15, droop=-10.0)
    tb = m.bone("tail", bd, (0, 32, 3))
    pts = [(0, 32.0, 3.0), (4.0, 24.0, 10.0), (10.0, 18.0, 15.0), (16.0, 16.0, 18.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tb, p0, p1, 3 - j, HIDE, extend=0.4)
    ar, h = a["arm_right"]["bone"], a["arm_right"]["hand"]                                   # golden war-hammer
    rod(m, ar, (h[0], h[1] + 2.0, h[2] - 1.0), (h[0], h[1] - 24.0, h[2] - 1.0), 1, GOLD, extend=0)
    m.round_box(ar, h[0], h[2] - 1.0, 3.6, 2.4, h[1] - 32.0, h[1] - 24.0, armour(P, "black", "black", trim="gold"), cut=1)
    for sy in (-1, 1):
        m.round_box(ar, h[0] + sy * 4.0, h[2] - 1.0, 0.8, 2.6, h[1] - 31.0, h[1] - 25.0, solid(P, "red"), cut=0)
    return m
