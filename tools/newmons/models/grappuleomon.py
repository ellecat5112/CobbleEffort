"""Grappu Leomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the grappling lion: a lion-man boxer with a wild golden mane, a white muzzle, black-and-
white armoured fighting gear, heavy grey gauntlets, armoured greaves with white claws and spinning vortex rings round
his fists and shins. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, fur, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 3.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a lion-man boxer with a wild golden mane, black-and-white armoured fighting gear, heavy grey gauntlets and "
        "spinning vortex rings round his fists and shins")
BASE = {"gold": (240, 170, 50), "gold_dark": (180, 100, 20), "white": (246, 246, 246), "white_dark": (180, 182, 196),
        "black": (40, 40, 46), "black_dark": (14, 14, 18), "grey": (150, 154, 166), "grey_dark": (80, 84, 96),
        "tan": (230, 190, 120), "tan_dark": (180, 130, 70), "eye": (60, 140, 220), "vortex": (200, 210, 230, 120),
        "red": (200, 40, 40)}
SHINY = {"gold": (200, 60, 50), "gold_dark": (130, 20, 14), "black": (230, 230, 236), "black_dark": (160, 160, 176)}


def P(v):
    return pal(BASE, SHINY, v)


BLACK = armour(P, "black", "black_dark", trim="white", trim_w=0.3)
WHITE = armour(P, "white", "white_dark", trim="black", trim_w=0.3)
GREY = metal(P, "grey", dark="grey_dark")


def vortexf(x, y, z, face, variant, box=None, **k):
    c = P(variant)["vortex"]
    return c, None


def build():
    m = Model("grappuleomon")
    mats = {"skin": skin(P, "tan", dark="tan_dark"), "chest": WHITE, "abs": BLACK, "pelvis": BLACK, "deltoid": BLACK,
            "upper_arm": BLACK, "forearm": GREY, "hand": GREY, "finger": GREY, "thigh": BLACK, "knee": WHITE,
            "shin": GREY, "calf": GREY, "foot": WHITE, "talon": solid(P, "white")}
    a = humanoid(m, mats, bulk=1.1, arm_bulk=1.15, leg_bulk=1.1, talons=True, digitigrade=True, name="grappuleomon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.8, 3.2, 53.4, 60.4, skin(P, "tan", dark="tan_dark"), cut=1)
    m.round_box(hd, 0, -3.8, 1.8, 1.2, 54.0, 57.0, skin(P, "white", dark="white_dark"), cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.2), 58.0, -3.9, max(sx * 0.8, sx * 2.2), 58.8, -3.7, solid(P, "eye"))
    for ring, (r, n, ln) in enumerate(((3.4, 14, 7.0), (4.8, 18, 9.0))):                     # wild golden mane
        for i in range(n):
            ang = 2 * math.pi * (i + ring * 0.5) / n
            spike(m, hd, (r * math.cos(ang) * 0.8, 57.0 + r * math.sin(ang), 1.0 + ring),
                  (math.cos(ang), math.sin(ang) + 0.3, 0.6), 2.0 - ring * 0.3, ln, strands(P, "gold", "gold_dark"), tip=0.8)
    for nm in ("arm_left", "arm_right", "leg_left", "leg_right"):                            # vortex rings
        jt = a[nm].get("wrist") or a[nm].get("ankle")
        bone = a[nm]["bone"]
        for j in range(8):
            a0, a1 = 2 * math.pi * j / 8, 2 * math.pi * (j + 1) / 8
            r = 4.0
            rod(m, bone, (jt[0] + r * math.cos(a0), jt[1] + 2.0 + j * 0.4, jt[2] + r * math.sin(a0)),
                (jt[0] + r * math.cos(a1), jt[1] + 2.4 + j * 0.4, jt[2] + r * math.sin(a1)), 1, vortexf, extend=0.3, t2=2)
    return m
