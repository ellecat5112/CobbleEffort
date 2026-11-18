"""Kaus Gammamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Gammamon's wind-archer evolution: a lean blue dragon-man with white armour plates and a long
crested head, black claws, a short dark tail and a great orange-and-cream membrane stretched from its arms to its
legs like a flying squirrel's, with jet vents on its legs. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, cutout, local, scales, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a lean blue dragon-man with white armour plates, a crested head, black claws and a great orange membrane between arms and legs"
BASE = {"blue": (50, 100, 200), "blue_dark": (16, 40, 120), "blue_light": (130, 180, 250), "white": (240, 244, 250),
        "white_dark": (160, 170, 196), "orange": (240, 150, 50), "cream": (250, 230, 190), "black": (24, 24, 30),
        "eye": (240, 60, 40)}
SHINY = {"blue": (160, 60, 160), "blue_dark": (80, 20, 80), "blue_light": (230, 150, 230), "orange": (90, 200, 160)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "blue", "blue_dark", size=1.2, light="blue_light")
PLATE = armour(P, "white", "white_dark", trim="blue_dark", trim_w=0.2)


def memf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return tone(p["cream"] if u / max(W, 1e-6) < 0.35 else p["orange"], face), None


def mem_in(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    a, b = u / max(W, 1e-6), v / max(H, 1e-6)
    return b > 0.2 * a and b < 1.0 - 0.15 * a * a


def build():
    m = Model("kausgammamon")
    mats = {"skin": HIDE, "chest": PLATE, "abs": HIDE, "pelvis": PLATE, "neck": HIDE, "deltoid": PLATE,
            "upper_arm": HIDE, "forearm": PLATE, "hand": HIDE, "finger": HIDE, "claw": solid(P, "black"),
            "thigh": HIDE, "knee": PLATE, "shin": PLATE, "calf": HIDE, "foot": HIDE, "talon": solid(P, "black")}
    a = humanoid(m, mats, bulk=0.82, arm_bulk=0.85, leg_bulk=0.9, claws=True, talons=True, digitigrade=True,
                 name="kausgammamon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.6, 2.4, 4.2, 54.0, 59.0, HIDE, cut=1)
    m.round_box(hd, 0, -4.6, 1.8, 2.0, 54.4, 57.0, PLATE, cut=1)                      # white snout plate
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.6, sx * 2.5), 57.0, -4.0, max(sx * 1.6, sx * 2.5), 57.8, -3.0, solid(P, "eye", glow=True))
    for j in range(4):                                                               # long crest
        spike(m, hd, (0, 58.6, -2.0 + j * 1.6), (0, 0.6, 1), 1.4, 7.0 - j, HIDE, tip=0.8)
    for side in (1, -1):                                                              # orange membranes
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 5.0, 48.0, 1.0))
        x0, x1 = sorted((side * 5.0, side * 24.0))
        m.box(wb, x0, 18.0, 1.6, x1, 48.0, 1.6, cutout(mem_in, memf), rotation=(0, side * -10, 0),
              pivot=(side * 5.0, 48.0, 1.6))
    rod(m, bd, (0, 32.0, 3.0), (0, 24.0, 10.0), 2, HIDE, extend=0.4, t2=1)
    return m
