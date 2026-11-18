"""Magna Garurumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the Hybrid of light united: a sleek ice-blue armoured wolf warrior with a wolf helm,
gold trim, slim armoured limbs with gold claws, a huge revolver cannon on one arm and a long rail cannon on the other,
and a crossed rack of swept blade-wings with red tips on its back. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage (Hybrid).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a sleek ice-blue armoured wolf warrior with gold trim, a revolver cannon, a rail cannon and swept blade-wings on its back"
BASE = {"blue": (140, 180, 240), "blue_dark": (50, 80, 160), "blue_light": (220, 236, 255), "gold": (240, 200, 70),
        "gold_dark": (160, 120, 20), "steel": (180, 190, 210), "steel_dark": (80, 90, 110), "red": (220, 50, 40),
        "eye": (250, 220, 60), "black": (30, 30, 40)}
SHINY = {"blue": (80, 80, 96), "blue_dark": (24, 24, 34), "blue_light": (160, 160, 180)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "blue", "blue_dark", light="blue_light", trim="gold", trim_w=0.25)
GUN = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("magnagarurumon")
    mats = {"skin": ARM, "chest": ARM, "abs": ARM, "pelvis": ARM, "neck": ARM, "deltoid": ARM, "upper_arm": ARM,
            "forearm": ARM, "hand": ARM, "finger": ARM, "claw": metal(P, "gold", dark="gold_dark"), "thigh": ARM,
            "knee": metal(P, "gold", dark="gold_dark"), "shin": ARM, "calf": ARM, "foot": ARM,
            "talon": metal(P, "gold", dark="gold_dark")}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.9, claws=True, talons=True, digitigrade=True,
                 name="magnagarurumon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, -1))
    m.round_box(hd, 0, -1.6, 2.6, 3.6, 53.6, 59.6, ARM, cut=1)
    m.round_box(hd, 0, -5.4, 1.6, 1.6, 53.8, 56.6, ARM, cut=1)
    m.box(hd, -1.6, 57.2, -5.1, 1.6, 57.8, -5.0, solid(P, "eye", glow=True))
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.8, 59.2, 0), (sx * 0.4, 1, 0.6), 1.4, 5.0, ARM, tip=0.8)
    hr = a["arm_right"]                                                              # revolver cannon
    hx, hy, hz = hr["hand"]
    m.round_box(hr["bone"], hx - 1.0, hz - 2.0, 3.0, 3.0, hy - 4.0, hy + 4.0, GUN, cut=1)
    rod(m, hr["bone"], (hx - 1.0, hy - 1.0, hz - 4.0), (hx - 1.0, hy - 1.0, hz - 16.0), 2, GUN, extend=0)
    m.round_box(hr["bone"], hx - 1.0, hz - 16.4, 1.6, 0.4, hy - 2.6, hy + 0.6, solid(P, "black"), cut=0)
    hl = a["arm_left"]                                                               # long rail cannon
    lx, ly, lz = hl["hand"]
    m.round_box(hl["bone"], lx + 1.0, lz - 4.0, 2.4, 10.0, ly - 2.0, ly + 2.4, GUN, cut=1)
    for side in (1, -1):                                                             # swept blade-wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 50.0, 4.0))
        for j, ang in enumerate((15, -10)):
            a_ = math.radians(ang)
            end = (side * 28.0 * math.cos(a_), 50.0 + 28.0 * math.sin(a_) + 6.0, 6.0)
            rod(m, wb, (side * 3.0, 50.0, 4.0), end, 1, ARM, extend=0.4, t2=3)
            spike(m, wb, end, (side * math.cos(a_), math.sin(a_), 0), 1.4, 4.0, solid(P, "red"), tip=0.8)
        rod(m, wb, (side * 4.0, 50.0, 4.0), (side * 10.0, 38.0, 8.0), 1, metal(P, "gold", dark="gold_dark"), extend=0.2, t2=2)
    return m
