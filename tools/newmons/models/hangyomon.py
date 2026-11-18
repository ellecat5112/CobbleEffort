"""Hangyomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the fish-man warrior: a hunched blue fish-man with a big white-and-red fishy head, a toothy grin
and green eyes, huge clawed blue hands, white fin-wings at its wrists and hips, a breathing tube on its back, a red
pack, a short harpoon spear and finned feet. 25 blocks tall.

Front is -z, y is up. 56 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, metal, scales, skin, solid
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(25, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a hunched blue fish-man with a big white-and-red fishy head, a toothy grin, huge clawed hands, white fins, a "
        "breathing tube and a harpoon")
BASE = {"blue": (50, 80, 180), "blue_dark": (20, 40, 110), "blue_light": (120, 150, 230), "white": (246, 246, 250),
        "white_dark": (190, 192, 206), "red": (210, 40, 50), "eye": (60, 190, 110), "mouth": (110, 20, 30),
        "tooth": (250, 250, 240), "steel": (190, 196, 210), "steel_dark": (90, 96, 110), "claw": (30, 30, 60),
        "rope": (220, 190, 130)}
SHINY = {"blue": (60, 140, 90), "blue_dark": (20, 80, 40), "blue_light": (140, 210, 160)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "blue", "blue_dark", size=1.4, light="blue_light")
WHITE = skin(P, "white", dark="white_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if 48.0 < y < 50.4 and abs(x) < 3.6:
            if y > 49.6 and (x * 1.2) % 1.2 < 0.7:
                return tone(p["tooth"], face), None
            return tone(p["mouth"], face), None
        if y < 48.0:
            return tone(p["red"], face), None
    return WHITE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("hangyomon")
    mats = {"skin": HIDE, "hand": HIDE, "finger": HIDE, "claw": solid(P, "claw"), "talon": solid(P, "claw")}
    a = humanoid(m, mats, bulk=1.05, arm_bulk=1.2, leg_bulk=1.0, claws=True, talons=True, name="hangyomon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 50, -3))
    m.round_box(hd, 0, -3.0, 4.4, 4.6, 46.0, 56.0, headf, cut=2)                        # big fishy head
    for sx in (-1, 1):
        m.round_box(hd, sx * 3.0, -7.4, 1.0, 0.3, 52.0, 54.0, solid(P, "eye"), cut=0)
        spike(m, hd, (sx * 4.2, 52.0, -1.0), (sx, 0.3, 0.4), 1.4, 4.0, WHITE, tip=0.8)      # fin ears
    for nm in ("arm_left", "arm_right", "leg_left", "leg_right"):                          # white fin-wings
        jt = a[nm].get("wrist") or a[nm].get("knee")
        sx = 1 if jt[0] > 0 else -1
        spike(m, a[nm]["bone"], jt, (sx, 0.3, 0.4), 1.6, 6.0, WHITE, tip=0.9)
    m.round_box(bd, 0, 5.0, 4.0, 2.4, 38.0, 48.0, armour(P, "red", "red", trim="steel"), cut=1)   # red pack
    rod(m, bd, (2.0, 48.0, 6.0), (0, 54.0, 2.0), 1, metal(P, "steel", dark="steel_dark"), extend=0.2, t2=1)  # tube
    ar, h = a["arm_right"]["bone"], a["arm_right"]["hand"]                                  # harpoon
    rod(m, ar, (h[0] + 4.0, h[1] + 6.0, h[2] + 6.0), (h[0] - 4.0, h[1] - 4.0, h[2] - 18.0), 1,
        metal(P, "steel", dark="steel_dark"), extend=0, t2=1)
    spike(m, ar, (h[0] - 4.0, h[1] - 4.0, h[2] - 18.0), (-0.3, -0.4, -1), 1.6, 3.0, solid(P, "steel_dark"), tip=0.8)
    return m
