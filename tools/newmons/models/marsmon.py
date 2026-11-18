"""Marsmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): the war god of the Olympos Twelve: a towering crimson-skinned brawler with a white beast-head helm and
horn, flames blazing off his shoulders, huge steel-and-red cannon gauntlets, a gold belt, violet patterned trousers,
red-and-white boots, and a long violet-lined cape. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import armour, cutout, fabric, flame_inside, fur, local, metal, skin, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a towering crimson war god with a white beast-head helm, flaming shoulders, huge cannon gauntlets, violet trousers and a long cape"
BASE = {"red": (210, 50, 40), "red_dark": (130, 20, 14), "red_light": (250, 140, 110), "white": (240, 240, 246),
        "white_dark": (180, 180, 196), "steel": (180, 184, 196), "steel_dark": (80, 84, 96), "violet": (130, 110, 180),
        "violet_dark": (60, 46, 110), "gold": (240, 200, 70), "gold_dark": (160, 120, 20), "eye": (60, 140, 230),
        "fire": (255, 160, 40, 210), "fire_core": (255, 240, 170, 240), "black": (34, 32, 36)}
SHINY = {"red": (60, 100, 200), "red_dark": (20, 40, 120), "red_light": (150, 180, 250), "fire": (120, 200, 255, 210)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "red", dark="red_dark", light="red_light")
PANTS = fabric(P, "violet", "violet_dark", period=1.6)
GAUNT = armour(P, "steel", "steel_dark", trim="red", trim_w=0.3, rivets=True)


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
    return c, c[:3]


def build():
    m = Model("marsmon")
    mats = {"skin": SKIN, "chest": SKIN, "abs": SKIN, "pelvis": PANTS, "neck": SKIN, "deltoid": SKIN, "upper_arm": SKIN,
            "forearm": GAUNT, "hand": GAUNT, "finger": GAUNT, "thigh": PANTS, "knee": PANTS, "shin": armour(P, "red", "red_dark"),
            "calf": armour(P, "red", "red_dark"), "foot": armour(P, "white", "white_dark"), "toe": solid(P, "red")}
    a = humanoid(m, mats, bulk=1.3, arm_bulk=1.3, leg_bulk=1.15, name="marsmon")
    bd = a["body"]
    m.round_box(bd, 0, -0.2, 5.6, 4.0, 33.0, 35.6, metal(P, "gold", dark="gold_dark"), cut=1)          # gold belt
    cape(m, bd, 53.0, 16.0, 46.0, fabric(P, "violet", "black"), z=4.4, flare=0.9, panels=8)
    hd = m.bone("head", bd, (0, 55, -1))
    m.round_box(hd, 0, -1.0, 3.2, 3.6, 53.6, 61.0, fur(P, "white", "white_dark"), cut=1)               # beast-head helm
    m.round_box(hd, 0, -4.6, 2.2, 1.6, 54.0, 57.0, fur(P, "white", "white_dark"), cut=1)
    m.box(hd, -1.6, 58.0, -4.7, 1.6, 58.8, -4.6, solid(P, "eye", glow=True))
    spike(m, hd, (0, 60.6, -3.0), (0, 1, -0.2), 1.6, 5.0, fur(P, "white", "white_dark"), tip=0.8)          # horn
    for sx in (-1, 1):                                                               # flaming shoulders
        for rot in (0, 90):
            m.box(bd, sx * 8.0 - 3.0, 50.0, 0.0, sx * 8.0 + 3.0, 60.0, 0.0, cutout(flame_inside(4, 0.1, 2), firef),
                  rotation=(0, rot, 0), pivot=(sx * 8.0, 50.0, 0.0))
    for nm in ("arm_left", "arm_right"):                                              # huge cannon gauntlets
        w = a[nm]["wrist"]
        m.round_box(a[nm]["bone"], w[0], w[2], 4.0, 4.0, w[1] - 6.0, w[1] + 6.0, GAUNT, cut=2)
        m.round_box(a[nm]["bone"], w[0], w[2] - 4.4, 2.0, 0.6, w[1] - 2.0, w[1] + 2.0, solid(P, "black"), cut=0)
    return m
