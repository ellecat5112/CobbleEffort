"""Mistymon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the magic knight of the mist: a tall armoured figure in red-and-gold plate under a long violet
cape lined white, a pale masked face behind a horned gold crown-helm, a jewelled gorget, white gauntlets and boots,
and a blazing sword of yellow flame held aloft. 25 blocks tall.

Front is -z, y is up. 70 units tall (the sword); Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import armour, cutout, fabric, flame_inside, gem, local, metal, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(25, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a tall knight in red-and-gold plate under a long violet cape, a pale masked face behind a horned gold crown-helm "
        "and a blazing sword of yellow flame")
BASE = {"red": (170, 30, 40), "red_dark": (90, 10, 16), "gold": (230, 190, 80), "gold_dark": (150, 110, 30),
        "violet": (110, 70, 160), "violet_dark": (54, 30, 90), "white": (240, 240, 246), "white_dark": (180, 180, 196),
        "mask": (230, 226, 220), "eye": (60, 40, 60), "gem": (60, 180, 120), "fire": (255, 200, 60, 215),
        "fire_core": (255, 250, 200, 235)}
SHINY = {"red": (40, 60, 150), "red_dark": (14, 24, 80), "violet": (60, 60, 70), "violet_dark": (24, 24, 30)}


def P(v):
    return pal(BASE, SHINY, v)


RED = armour(P, "red", "red_dark", trim="gold", trim_w=0.3)
GOLD = metal(P, "gold", dark="gold_dark")
WHITE = armour(P, "white", "white_dark", trim="gold", trim_w=0.2)


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if 0.3 < u / max(W, 1e-6) < 0.7 else p["fire"]
    return c, c[:3]


def build():
    m = Model("mistymon")
    mats = {"skin": RED, "neck": GOLD, "upper_arm": RED, "forearm": WHITE, "hand": WHITE, "finger": WHITE,
            "thigh": RED, "knee": GOLD, "shin": WHITE, "calf": WHITE, "foot": WHITE, "toe": WHITE,
            "pelvis": fabric(P, "violet", "violet_dark")}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=0.9, leg_bulk=0.95, name="mistymon")
    bd = a["body"]
    for j in range(4):                                                                   # long robe skirt
        r = 4.8 + j * 0.8
        m.round_box(bd, 0, 0.6, r, r * 0.8, 31.0 - (j + 1) * 6.0, 31.4 - j * 6.0, fabric(P, "violet", "violet_dark",
                                                                                            seam="gold"), cut=1)
    ball(m, bd, (0, 49.0, -3.8), 1.0, gem(P, "gem", "white"), layers=2)                   # jewelled gorget
    cape(m, bd, 52.0, 16.0, 50.0, fabric(P, "violet", "violet_dark"), z=4.0, flare=0.7, panels=6, seed=3)
    for sx in (-1, 1):
        m.round_box(bd, sx * 7.4, 0.0, 2.6, 3.0, 49.0, 53.0, GOLD, cut=1)                 # shoulder plates
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 59.6, solid(P, "mask"), cut=1)               # pale mask
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.6), 57.0, -2.9, max(sx * 0.6, sx * 1.6), 57.6, -2.8, solid(P, "eye"))
    m.round_box(hd, 0, 0.0, 2.8, 3.0, 58.6, 61.6, GOLD, cut=1)                            # crown-helm
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.4, 60.6, 0.0), (sx * 0.5, 1, 0.3), 1.4, 6.0, GOLD, tip=0.8)
    spike(m, hd, (0, 61.4, -1.0), (0, 1, 0.2), 1.2, 3.6, GOLD, tip=0.8)
    ar = a["arm_right"]                                                                  # blazing flame sword
    h = ar["hand"]
    m.box(ar["bone"], h[0] - 2.4, h[1] + 0.4, h[2] - 1.0, h[0] + 2.4, h[1] + 1.4, h[2] + 1.0, GOLD)
    for ang in (0, 90):
        m.box(ar["bone"], h[0] - 2.0, h[1] + 1.4, h[2], h[0] + 2.0, h[1] + 26.0, h[2],
              cutout(flame_inside(6, 0.05, 4, base=0.8), firef), rotation=(0, ang, 0), pivot=(h[0], h[1], h[2]))
    return m
