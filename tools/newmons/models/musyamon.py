"""Musyamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a demon samurai: red lacquered armour laced with white cords over a green-skinned oni body, a wild
blond mane and beard with golden horns, glaring eyes, a blue tasseled cord at its throat, ragged violet cape-wings
streaming behind, a gold-trimmed sash, straw sandals with blue wraps, a prayer-bead string and a long katana raised
in its right hand. 15 blocks tall.

Front is -z, y is up. 66 units tall (the katana); Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import armour, fabric, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a demon samurai in red lacquered armour laced white over a green oni body, a wild blond mane and golden horns, "
        "ragged violet cape-wings, straw sandals and a long katana")
BASE = {"red": (210, 60, 40), "red_dark": (120, 24, 14), "white": (240, 240, 236), "green": (110, 150, 80),
        "green_dark": (60, 90, 40), "blond": (240, 210, 90), "blond_dark": (180, 140, 40), "gold": (230, 190, 70),
        "violet": (150, 140, 210), "violet_dark": (80, 70, 150), "blue": (60, 90, 190), "straw": (220, 190, 120),
        "steel": (220, 224, 236), "steel_dark": (110, 114, 126), "eye": (250, 230, 60), "bead": (130, 200, 180)}
SHINY = {"red": (40, 50, 70), "red_dark": (14, 18, 30), "violet": (220, 120, 120), "violet_dark": (140, 50, 50)}


def P(v):
    return pal(BASE, SHINY, v)


ARM0 = armour(P, "red", "red_dark", trim="gold", trim_w=0.25)
SKIN = skin(P, "green", dark="green_dark")


def armf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "south") and abs(((x + y) % 2.4) - 1.2) < 0.15 and abs(((x - y) % 2.4) - 1.2) < 0.6:
        return tone(p["white"], face), None                                              # white lacing cords
    return ARM0(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("musyamon")
    mats = {"skin": SKIN, "chest": armf, "abs": armf, "pelvis": armf, "neck": SKIN, "deltoid": armf,
            "upper_arm": SKIN, "forearm": armf, "hand": SKIN, "finger": SKIN, "thigh": armf, "knee": armf,
            "shin": fabric(P, "blue", "blue"), "calf": fabric(P, "blue", "blue"), "foot": solid(P, "straw"),
            "toe": solid(P, "straw")}
    a = humanoid(m, mats, bulk=1.05, arm_bulk=1.05, leg_bulk=1.0, hand_pose="fist", name="musyamon")
    bd = a["body"]
    for sx in (-1, 1):                                                                   # big shoulder guards
        m.round_box(bd, sx * 8.0, 0.0, 3.4, 3.8, 45.0, 52.0, armf, cut=1)
    for j in range(3):                                                                   # armour skirt tassets
        r = 5.4 + j * 0.6
        m.round_box(bd, 0, 0.4, r, r * 0.8, 30.0 - (j + 1) * 3.0, 30.4 - j * 3.0, armf, cut=1)
    m.round_box(bd, 0, 0.4, 5.4, 4.0, 30.0, 32.0, metal(P, "gold"), cut=1)               # gold sash
    cape(m, bd, 52.0, 18.0, 40.0, fabric(P, "violet", "violet_dark"), z=4.0, flare=1.4, panels=7, seed=9)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 2.8, 54.0, 59.6, SKIN, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 2.0), 57.0, -3.3, max(sx * 0.6, sx * 2.0), 57.8, -3.1, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 1.8, 59.6, -1.0), (sx * 0.5, 1, 0), 1.4, 4.0, solid(P, "gold"), tip=0.8)   # golden horns
    for i in range(10):                                                                  # wild blond mane + beard
        ang = math.radians(-90 + i * 20)
        spike(m, hd, (2.6 * math.sin(ang), 58.6, 2.0 * math.cos(ang) * 0.6 + 0.6), (math.sin(ang), 0.8, 0.5), 1.6,
              5.0, strands(P, "blond", "blond_dark"), tip=0.8)
    for j in range(4):
        spike(m, hd, ((j - 1.5) * 1.0, 54.4, -2.6), (0, -1, -0.4), 1.2, 4.0, strands(P, "blond", "blond_dark"), tip=0.8)
    for j in range(3):                                                                   # blue tasselled cord
        rod(m, bd, ((j - 1) * 1.6, 51.0, -4.2), ((j - 1) * 2.0, 46.0, -4.8), 1, solid(P, "blue"), extend=0.1)
    ar = a["arm_right"]                                                                  # long raised katana
    h = ar["hand"]
    rod(m, ar["bone"], (h[0], h[1] - 2.0, h[2]), (h[0], h[1] + 2.0, h[2]), 1, solid(P, "red_dark"), extend=0.2)
    m.box(ar["bone"], h[0] - 1.6, h[1] + 2.0, h[2] - 1.6, h[0] + 1.6, h[1] + 2.6, h[2] + 1.6, metal(P, "gold"))
    rod(m, ar["bone"], (h[0], h[1] + 2.6, h[2]), (h[0] + 2.0, h[1] + 30.0, h[2] - 4.0), 1,
        metal(P, "steel", dark="steel_dark"), extend=0.2, t2=2)
    al = a["arm_left"]                                                                   # prayer beads
    w = al["hand"]
    for i in range(8):
        ball(m, al["bone"], (w[0] + 0.4 * math.sin(i), w[1] - 1.0 - i * 1.1, w[2] - 1.0), 0.6, solid(P, "bead"),
             layers=1)
    return m
