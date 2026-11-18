"""Parallelmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a mutant from a parallel world, built as two mirrored halves: a pale lavender-and-white armoured
body of curved shell plates marked with violet hexagon sigils, a pointed visored mask with a violet gem, great curved
shoulder carapaces, arms ending in dark blue blade-claws and legs tipped with long black talons, joined by twisted
brown cords. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, gem, local, metal, solid, twisted
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("a pale lavender-and-white armoured mutant of curved shell plates with violet hexagon sigils, a pointed visored "
        "mask, great shoulder carapaces, dark blue blade-claws and twisted cords")
BASE = {"shell": (220, 210, 236), "shell_dark": (150, 140, 180), "violet": (130, 70, 200), "violet_light": (220, 180, 255),
        "navy": (40, 40, 110), "navy_dark": (14, 14, 50), "cord": (110, 70, 50), "cord_dark": (60, 34, 20),
        "black": (24, 22, 30)}
SHINY = {"shell": (210, 236, 220), "shell_dark": (140, 180, 150), "violet": (200, 90, 60)}


def P(v):
    return pal(BASE, SHINY, v)


SHELL0 = armour(P, "shell", "shell_dark", trim="violet", trim_w=0.2)


def shellf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west") and box is not None:
        u, v, W, H = local(x, y, z, face, box)
        d = max(abs(u - W / 2), abs(v - H / 2) * 1.15)
        if W > 4 and H > 4 and abs(d - min(W, H) * 0.3) < 0.3:
            return tone(p["violet"], face), None
    return SHELL0(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("parallelmon")
    CORD = twisted(P, "cord", "cord_dark")
    mats = {"skin": shellf, "neck": CORD, "upper_arm": CORD, "thigh": CORD, "claw": metal(P, "navy", dark="navy_dark"),
            "talon": solid(P, "black")}
    a = humanoid(m, mats, bulk=1.0, arm_bulk=1.0, leg_bulk=1.1, claws=True, talons=True, digitigrade=True,
                 name="parallelmon")
    bd = a["body"]
    for sx in (-1, 1):                                                                   # great shoulder carapaces
        m.round_box(bd, sx * 11.0, 0, 5.0, 5.0, 40.0, 54.0, shellf, cut=2)
        for j in range(3):
            spike(m, bd, (sx * 12.0 + (j - 1) * 2.0, 40.0, -3.0), (0, -1, -0.4), 1.4, 7.0,
                  metal(P, "navy", dark="navy_dark"), tip=0.8)
    for nm in ("arm_left", "arm_right"):                                                 # blade-claws
        h = a[nm]["hand"]
        sx = 1 if h[0] > 0 else -1
        spike(m, a[nm]["bone"], (h[0], h[1], h[2]), (sx * 0.4, -1, -0.6), 2.4, 12.0, metal(P, "navy", dark="navy_dark"),
              tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 2.8, 54.0, 59.0, shellf, cut=1)
    spike(m, hd, (0, 58.0, -1.0), (0, 1, -0.3), 2.4, 8.0, shellf, tip=0.8)                 # pointed visored mask
    ball(m, hd, (0, 55.6, -3.0), 1.2, gem(P, "violet", "violet_light"), layers=2)
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.4, 57.0, 0), (sx * 1, 0.4, 0.2), 1.2, 5.0, shellf, tip=0.8)
    return m
