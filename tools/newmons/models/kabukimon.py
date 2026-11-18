"""Kabukimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the kabuki dancer: a figure in a white kabuki mask painted with red and green lines, a long mane
of flowing orange hair, a red-and-yellow kimono jacket with a white rope belt, huge red hakama trousers, big white
paw-feet, and two great pink lotus flowers held up in its hands, each with a kabuki face in its heart. 15 blocks.

Front is -z, y is up. 64 units tall; Adult stage (Armor).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import cutout, fabric, local, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a kabuki dancer with a painted white mask, a flowing orange mane, a red-and-yellow kimono, huge red hakama, "
        "white paw-feet and two great pink lotus flowers in its hands")
BASE = {"white": (246, 246, 250), "white_dark": (180, 182, 196), "red": (210, 30, 40), "red_dark": (120, 10, 18),
        "yellow": (240, 200, 60), "yellow_dark": (170, 130, 20), "orange": (230, 110, 40), "orange_dark": (160, 60, 14),
        "pink": (250, 180, 210), "pink_dark": (220, 110, 160), "green": (60, 150, 70), "eye": (40, 30, 30)}
SHINY = {"red": (40, 70, 200), "red_dark": (14, 24, 110), "orange": (240, 240, 250), "orange_dark": (170, 172, 190)}


def P(v):
    return pal(BASE, SHINY, v)


def maskf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.1) < 0.5 and abs(y - 57.8) < 0.3:
                return tone(p["eye"], face), None
            if abs(y - 58.6 - (sx * x) * 0.3) < 0.2 and 0.6 < sx * x < 2.2:
                return tone(p["red"], face), None
            if abs(x - sx * 1.6) < 0.2 and 55.0 < y < 57.0:
                return tone(p["green"], face), None
        if abs(y - 55.4) < 0.25 and abs(x) < 0.8:
            return tone(p["red"], face), None
    return skin(P, "white", dark="white_dark")(x, y, z, face, variant, box=box, **k)


def petal_in(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    a, b = u / max(W, 1e-6) - 0.5, v / max(H, 1e-6)
    return abs(a) < 0.5 * math.sin(math.pi * min(1.0, b * 0.95)) + 0.02


def petalf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return tone(p["pink_dark"] if v / max(H, 1e-6) < 0.3 else p["pink"], face), None


def lotus(m, bone, c, r):
    x, y, z = c
    m.round_box(bone, x, z, r * 0.3, r * 0.3, y - r * 0.3, y + r * 0.3, maskf, cut=0)
    for i in range(8):
        ang = 360.0 * i / 8
        m.box(bone, x - r * 0.35, y, z + 0.4, x + r * 0.35, y + r, z + 0.4, cutout(petal_in, petalf),
              rotation=(0, 0, ang), pivot=(x, y, z + 0.4))


def build():
    m = Model("kabukimon")
    JACK = fabric(P, "red", "red_dark")
    SLEEVE = fabric(P, "yellow", "yellow_dark")
    HAKAMA = fabric(P, "red", "red_dark", period=1.6)
    mats = {"skin": skin(P, "white", dark="white_dark"), "chest": JACK, "abs": JACK, "pelvis": HAKAMA,
            "neck": skin(P, "white", dark="white_dark"), "deltoid": SLEEVE, "upper_arm": SLEEVE, "forearm": SLEEVE,
            "hand": skin(P, "white", dark="white_dark"), "finger": skin(P, "white", dark="white_dark"),
            "thigh": HAKAMA, "knee": HAKAMA, "shin": HAKAMA, "calf": HAKAMA, "foot": solid(P, "white"),
            "toe": solid(P, "white")}
    a = humanoid(m, mats, bulk=1.0, arm_bulk=1.1, leg_bulk=1.0, name="kabukimon")
    bd = a["body"]
    m.round_box(bd, 0, 0.2, 4.8, 3.6, 34.6, 36.4, solid(P, "white"), cut=1)                     # rope belt
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                              # huge flared hakama
        lg = a[nm]["bone"]
        for j in range(4):
            r = 3.6 + j * 1.2
            m.round_box(lg, sx * (3.2 + j * 0.6), 0.0, r, r, 30.0 - (j + 1) * 6.0, 30.0 - j * 6.0 + 0.4, HAKAMA,
                        cut=max(1, int(r * 0.3)))
        m.round_box(lg, sx * 5.4, -2.0, 3.0, 4.6, 0.0, 3.6, solid(P, "white"), cut=1)
    for sx in (-1, 1):                                                               # wide kimono sleeves
        m.round_box(a["arm_left" if sx > 0 else "arm_right"]["bone"], sx * 8.0, 0.0, 2.8, 3.6, 38.0, 46.0, SLEEVE, cut=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 3.0, 54.0, 60.4, maskf, cut=1)
    for i in range(13):                                                              # flowing orange mane
        ang = math.radians(-120 + i * 20)
        rod(m, hd, (2.4 * math.sin(ang), 60.4, 0.6 + 1.6 * math.cos(ang)), (5.0 * math.sin(ang), 36.0, 4.0 + 1.6 * math.cos(ang)),
            2, strands(P, "orange", "orange_dark"), extend=0.3, t2=1)
    for nm in ("arm_left", "arm_right"):                                             # lotus flowers held up
        hx, hy, hz = a[nm]["hand"]
        sx = 1 if hx > 0 else -1
        rod(m, a[nm]["bone"], (hx, hy, hz), (hx + sx * 2.0, hy + 12.0, hz - 2.0), 1, solid(P, "green"), extend=0, t2=1)
        lotus(m, a[nm]["bone"], (hx + sx * 2.0, hy + 16.0, hz - 3.0), 7.0)
    return m
