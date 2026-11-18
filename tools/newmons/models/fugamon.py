"""Fugamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the oni. A stooped, hulking rust-brown ogre with shaggy grey hair, a snarling fanged face with a
broad nose, a tiger-striped loincloth and sash, black spiked bracers, a great studded club of bone, and clawed feet.
15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fur, leather, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a stooped hulking rust-brown ogre with shaggy grey hair, a fanged snarling face, a tiger-striped loincloth, black "
        "spiked bracers and a great studded bone club")
BASE = {"rust": (180, 80, 40), "rust_dark": (110, 40, 16), "rust_light": (230, 140, 90), "grey": (210, 210, 214),
        "grey_dark": (130, 130, 140), "tiger": (250, 190, 40), "tiger_dark": (30, 26, 24), "black": (34, 32, 38),
        "black_dark": (14, 14, 18), "bone": (240, 232, 210), "bone_dark": (180, 170, 140), "mouth": (120, 20, 30),
        "tooth": (250, 250, 246), "eye": (250, 220, 60), "steel": (200, 204, 214)}
SHINY = {"rust": (80, 110, 170), "rust_dark": (30, 50, 100), "rust_light": (150, 180, 230)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "rust", dark="rust_dark", light="rust_light")


def tigerf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(((x + 0.5 * y) * 0.7) % 3.0 - 1.5) < 0.4:
        return tone(p["tiger_dark"], face), None
    return tone(p["tiger"], face), None


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if 47.0 < y < 49.4 and abs(x) < 2.8:
            if (y > 48.6 or y < 47.6) and ((x + 3.0) % 1.0) < 0.5:
                return tone(p["tooth"], face), None
            return tone(p["mouth"], face), None
        for sx in (-1, 1):
            if abs(x - sx * 1.6) < 0.6 and abs(y - 52.0) < 0.4:
                return p["eye"], p["eye"]
    return SKIN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("fugamon")
    mats = {"skin": SKIN, "pelvis": tigerf, "hand": SKIN, "finger": SKIN, "claw": solid(P, "black"),
            "forearm": leather(P, "black", "black_dark"), "foot": SKIN, "talon": solid(P, "black")}
    a = humanoid(m, mats, bulk=1.25, arm_bulk=1.3, leg_bulk=1.15, claws=True, talons=True, name="fugamon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 50, -3))                                               # head low on hunched shoulders
    m.round_box(hd, 0, -3.0, 3.6, 3.4, 45.6, 54.6, headf, cut=1)
    m.round_box(hd, 0, -6.8, 1.4, 0.8, 49.6, 51.6, SKIN, cut=0)                        # broad nose
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.8, 47.2, -6.2), (0, 1, -0.2), 0.8, 2.6, solid(P, "tooth"), tip=0.2)   # tusks
        spike(m, hd, (sx * 3.6, 53.0, -2.0), (sx, 0.3, 0), 1.0, 2.0, SKIN, tip=0.3)                 # ears
    for i in range(14):                                                                # shaggy grey hair
        ang = math.radians(-120 + i * 18)
        spike(m, hd, (3.0 * math.sin(ang), 54.0, -2.0 + 2.6 * math.cos(ang) + 1.0),
              (math.sin(ang) * 0.8, 0.5, 0.6 + 0.3 * math.cos(ang)), 1.8, 7.0 + (i % 3) * 1.5,
              strands(P, "grey", "grey_dark"), tip=0.4)
    m.round_box(bd, 0, -0.4, 5.6 * 1.25, 4.4, 36.6, 38.2, tigerf, cut=1)               # tiger sash
    for nm in ("arm_left", "arm_right"):                                               # bracer spikes
        w = a[nm]["wrist"]
        sx = 1 if w[0] > 0 else -1
        for j in range(3):
            spike(m, a[nm]["bone"], (w[0] + sx * 1.6, w[1] + 1.0 + j * 1.6, w[2]), (sx, 0, 0), 0.8, 1.8,
                  solid(P, "steel"), tip=0.2)
    ar, h = a["arm_right"]["bone"], a["arm_right"]["hand"]                             # studded bone club
    rod(m, ar, (h[0], h[1], h[2] - 1.0), (h[0] - 2.0, h[1] - 4.0, h[2] - 18.0), 2,
        leather(P, "bone", "bone_dark"), extend=0.3, t2=3)
    m.round_box(ar, h[0] - 2.0, h[2] - 19.0, 2.6, 3.0, h[1] - 6.6, h[1] - 1.4, solid(P, "bone"), cut=1)
    for j in range(5):
        ang = math.radians(j * 72)
        spike(m, ar, (h[0] - 2.0 + 2.6 * math.cos(ang), h[1] - 4.0 + 2.6 * math.sin(ang), h[2] - 19.0),
              (math.cos(ang), math.sin(ang), -0.3), 0.8, 2.0, solid(P, "steel"), tip=0.2)
    return m
