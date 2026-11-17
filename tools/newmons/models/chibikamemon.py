"""Chibi Kamemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net, where it is listed under its Japanese name and shares Kamemon's page): the little turtle soldier.
A green turtle standing upright in a blue camouflage helmet, a red shell-vest with a gold button, white claws on its
hands and feet, and a short tail. Child stage.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, fbm, metal, mix, scales, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.0)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 14}
LOOK = "a little green turtle soldier in a blue camouflage helmet and a red shell-vest with a gold button"
BASE = {"green": (90, 170, 70), "green_dark": (40, 100, 30), "green_light": (160, 220, 130), "camo": (70, 110, 180),
        "camo_dark": (30, 50, 100), "camo_light": (140, 180, 230), "red": (220, 90, 60), "red_dark": (150, 40, 20),
        "gold": (240, 200, 60), "gold_dark": (170, 120, 20), "claw": (246, 246, 246), "eye": (30, 30, 30),
        "black": (30, 30, 36)}
SHINY = {"green": (220, 180, 80), "green_dark": (150, 110, 30), "green_light": (250, 220, 150), "camo": (90, 140, 70),
         "camo_dark": (40, 80, 30), "camo_light": (160, 200, 120)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = scales(P, "green", "green_dark", size=1.2, light="green_light", rim_mix=0.3)


def camof(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    n = fbm(x * 0.5, y * 0.5, z * 0.5, 4)
    return tone(p["camo_dark"] if n < 0.4 else p["camo_light"] if n > 0.62 else p["camo"], face), None


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.6) < 0.7 and abs(y - 22.2) < 0.3:
                return tone(p["eye"], face), None
        if abs(y - 20.4) < 0.15 and abs(x) < 1.8:
            return tone(p["eye"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("chibikamemon")
    top = m.bone("chibikamemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 0.4, 4.6, 4.0, 7.0, 17.4, armour(P, "red", "red_dark", trim="red_dark"), cut=2)   # shell-vest
    m.round_box(bd, 0, 1.6, 4.4, 3.4, 8.0, 17.0, SKIN, cut=2)
    m.box(bd, -1.0, 12.0, -4.6, 1.0, 14.0, -4.0, metal(P, "gold", dark="gold_dark"))            # gold button
    hd = m.bone("head", bd, (0, 17, 0))
    m.round_box(hd, 0, -0.8, 3.2, 3.4, 17.0, 23.6, headf, cut=1)
    m.box(hd, -2.2, 18.6, -5.6, 2.2, 21.4, -3.6, SKIN)                                   # snout
    m.round_box(hd, 0, -0.6, 3.8, 3.8, 22.4, 26.6, camof, cut=1)                          # camo helmet
    m.box(hd, -4.0, 22.2, -4.6, 4.0, 23.0, 3.4, solid(P, "black"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.6, 15.0, 0))
        rod(m, ab, (sx * 4.6, 15.0, 0), (sx * 6.0, 10.0, -1.0), 2, SKIN, extend=0.4)
        for j in range(3):
            spike(m, ab, (sx * 6.0 + (j - 1) * 0.7, 9.6, -1.4), (0, -1, -0.4), 0.7, 1.4, solid(P, "claw"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.4, 8.0, 0))
        m.round_box(lg, sx * 2.6, 0, 2.0, 2.2, 0.0, 8.0, SKIN, cut=1)
        for j in range(3):
            spike(m, lg, (sx * 2.6 + (j - 1) * 1.0, 0.6, -2.2), (0, -0.2, -1), 0.8, 1.6, solid(P, "claw"))
    tl = m.bone("tail", bd, (0, 8, 4))
    spike(m, tl, (0, 8.0, 4.0), (0.3, -0.3, 1), 1.6, 3.0, SKIN, tip=0.4)
    return m
