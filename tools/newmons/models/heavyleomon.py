"""Heavy Leomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the heavy lion: a squat lion-man in yellow-and-black heavy machinery armour with a flaming mane, a
huge yellow tower-shield arm tipped with a drill spike, a red armoured fist with a twin-barrel cannon, steel pistons
at its shoulders and a wheeled, red-footed base. 35 blocks tall.

Front is -z, y is up. 60 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, cutout, flame_inside, local, metal, riveted, skin, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(35, HEIGHT, 4.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("a squat lion-man in yellow-and-black heavy machinery armour with a flaming mane, a huge yellow tower-shield arm "
        "with a drill spike, a red cannon fist and a wheeled base")
BASE = {"yellow": (240, 200, 40), "yellow_dark": (170, 130, 10), "black": (40, 38, 44), "black_dark": (14, 14, 18),
        "red": (200, 40, 40), "red_dark": (120, 14, 18), "steel": (190, 196, 210), "steel_dark": (90, 96, 110),
        "face": (230, 180, 90), "fire": (255, 150, 40, 215), "fire_core": (255, 240, 170, 240), "eye": (60, 140, 220)}
SHINY = {"yellow": (70, 160, 220), "yellow_dark": (20, 90, 160)}


def P(v):
    return pal(BASE, SHINY, v)


YEL = armour(P, "yellow", "yellow_dark", trim="black", trim_w=0.4, rivets=True)
BLACK = riveted(P, "black", "black_dark")
STEEL = metal(P, "steel", dark="steel_dark")


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
    return c, c[:3]


def build():
    m = Model("heavyleomon")
    mats = {"skin": BLACK, "chest": YEL, "deltoid": YEL, "forearm": YEL, "thigh": BLACK, "knee": YEL, "shin": YEL,
            "foot": armour(P, "red", "red_dark")}
    a = humanoid(m, mats, bulk=1.3, arm_bulk=1.3, leg_bulk=1.3, name="heavyleomon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, -1))
    m.round_box(hd, 0, -1.4, 3.0, 3.4, 53.0, 60.0, skin(P, "face", dark="yellow_dark"), cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.2), 57.0, -4.9, max(sx * 0.8, sx * 2.2), 57.8, -4.7, solid(P, "eye"))
        rod(m, bd, (sx * 8.0, 52.0, 2.0), (sx * 10.0, 46.0, 4.0), 2, STEEL, extend=0)          # shoulder pistons
    for j in range(5):                                                                        # flaming mane
        for ang in (0, 90):
            at = ((j - 2) * 1.8, 59.0, 1.0 + abs(j - 2) * 0.6)
            m.box(hd, at[0] - 1.6, at[1], at[2], at[0] + 1.6, at[1] + 6.0 - abs(j - 2), at[2],
                  cutout(flame_inside(3, 0.2, j + 1), firef), rotation=(0, ang, 0), pivot=at)
    al, hl = a["arm_left"]["bone"], a["arm_left"]["hand"]                                      # tower-shield arm
    m.round_box(al, hl[0] + 3.0, hl[2] - 2.0, 4.0, 3.0, hl[1] - 6.0, hl[1] + 22.0, YEL, cut=1)
    spike(m, al, (hl[0] + 3.0, hl[1] + 22.0, hl[2] - 2.0), (0, 1, 0), 3.0, 8.0, STEEL, tip=1.0)
    ar, hr = a["arm_right"]["bone"], a["arm_right"]["hand"]                                     # red cannon fist
    m.round_box(ar, hr[0], hr[2] - 1.0, 3.0, 3.0, hr[1] - 2.0, hr[1] + 3.0, armour(P, "red", "red_dark"), cut=1)
    for sy in (-1, 1):
        rod(m, ar, (hr[0], hr[1] + 5.0 + sy * 1.4, hr[2]), (hr[0], hr[1] + 5.0 + sy * 1.4, hr[2] - 10.0), 2, STEEL, extend=0)
    for sx in (-1, 1):                                                                           # wheels
        m.round_box(a["leg_left" if sx > 0 else "leg_right"]["bone"], sx * 7.0, 4.0, 1.0, 3.0, 0.0, 6.0,
                    BLACK, cut=1)
    return m
