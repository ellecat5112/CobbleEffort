"""Tempomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a street-dancing penguin-bird man: a deep blue hoodie with a gold disc emblem, a yellow beak and
spiky yellow crest, green headphones, baggy white trousers, red-and-black sneakers, black taloned hands in gold-cuffed
gloves and a green-tipped tail. 25 blocks.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import fabric, feathers, leather, plane, skin, solid
from _route import pal, tone

HEIGHT = 67
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a street-dancing bird man in a blue hoodie with a gold disc, a yellow beak and crest, green headphones, white trousers and red sneakers"
BASE = {"blue": (50, 60, 160), "blue_dark": (24, 28, 90), "white": (244, 244, 248), "white_dark": (190, 190, 204),
        "yellow": (250, 210, 50), "yellow_dark": (200, 150, 20), "black": (36, 34, 40), "black_dark": (14, 14, 16),
        "green": (80, 230, 90), "red": (210, 40, 40), "red_dark": (130, 16, 16), "gold": (230, 186, 60),
        "eye": (255, 255, 255), "orange": (240, 140, 40)}
SHINY = {"blue": (160, 40, 60), "blue_dark": (90, 16, 30)}


def P(v):
    return pal(BASE, SHINY, v)


def hoodief(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        d = math.hypot(a, b - 44.0)
        if d < 3.6:
            return (p["gold"] if d > 2.4 or d < 1.0 else p["blue_dark"]), None
    return fabric(P, "blue", "blue_dark")(x, y, z, face, variant, box=box, **k)


def shoef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if y < 0.8:
        return tone(p["white"], face), None
    return tone(p["red"] if y < 2.2 else p["black"], face), None


def build():
    m = Model("tempomon")
    HOOD = fabric(P, "blue", "blue_dark")
    PANTS = fabric(P, "white", "white_dark")
    mats = {"skin": skin(P, "black", dark="black_dark"), "chest": hoodief, "abs": HOOD, "pelvis": PANTS,
            "deltoid": HOOD, "upper_arm": HOOD, "forearm": HOOD, "hand": leather(P, "black", "black_dark"),
            "thigh": PANTS, "knee": PANTS, "shin": PANTS, "calf": PANTS, "foot": shoef, "neck": HOOD}
    a = humanoid(m, mats, bulk=1.0, arm_bulk=0.95, leg_bulk=1.2, name="tempomon")
    bd = a["body"]
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                                # baggy trouser cuffs
        lg = a[nm]
        k = lg["knee"]
        m.round_box(lg["bone"], k[0], k[2], 3.2, 3.2, 6.0, 18.0, PANTS, cut=1)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        w = a[nm]["wrist"]
        m.round_box(a[nm]["bone"], w[0], w[2], 1.8, 1.8, w[1] - 0.6, w[1] + 1.0, solid(P, "gold"), cut=0)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0.4, 4.2, 4.4, 53.0, 62.0, HOOD, cut=2)                            # hood
    m.round_box(hd, 0, -1.4, 3.0, 3.0, 54.0, 60.0, skin(P, "black", dark="black_dark"), cut=1)
    spike(m, hd, (0, 57.0, -4.0), (0, -0.2, -1), 2.4, 5.0, solid(P, "yellow"), tip=0.8)       # beak
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.0), 58.2, -4.5, max(sx * 0.8, sx * 2.0), 59.0, -4.2, solid(P, "eye", glow=True))
        m.round_box(hd, sx * 4.4, 0, 1.0, 2.0, 56.0, 60.0, solid(P, "green", glow=True), cut=0)  # headphones
    for j in range(5):                                                                  # crest
        spike(m, hd, ((j - 2) * 0.8, 61.6, 0.6), ((j - 2) * 0.3, 1, 0.5), 1.0, 6.0 + (2 - abs(j - 2)) * 1.6,
              solid(P, "yellow"), tip=0.8)
    tl = m.bone("tail", bd, (0, 30, 4))
    for j in range(3):
        spike(m, tl, ((j - 1) * 1.4, 30.0, 4.0), ((j - 1) * 0.3, -0.6, 1), 1.4, 7.0, feathers(P, "black", "black_dark"),
              tip=0.8)
    spike(m, tl, (0, 26.0, 9.0), (0, -0.6, 1), 1.2, 3.0, solid(P, "green"), tip=0.8)
    return m
