"""Hanumon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
monkey brawler: a crouching beast-man with a shaggy golden-yellow mane and fur streaked red, a blue-grey ape face, a
green beaded collar, blue-grey hands and feet with claws, and a big bone club. Adult stage, 15 blocks tall.

Front is -z, y is up. 48 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fur, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a crouching beast-man with a shaggy golden mane and red-streaked fur, a blue-grey ape face and a big bone club"
BASE = {"gold": (250, 220, 70), "gold_dark": (200, 160, 30), "red": (210, 50, 40), "grey": (120, 130, 170),
        "grey_dark": (70, 80, 120), "green": (60, 160, 90), "bone": (240, 232, 210), "bone_dark": (180, 170, 150),
        "eye": (250, 220, 60), "claw": (240, 236, 220)}
SHINY = {"gold": (240, 240, 246), "gold_dark": (180, 180, 196)}


def P(v):
    return pal(BASE, SHINY, v)


FUR0 = fur(P, "gold", "gold_dark", length=1.6, density=2.0)
GREY = skin(P, "grey", dark="grey_dark")


def furf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(((y * 0.5 + x * 0.3) % 4.0) - 2.0) < 0.25:
        return tone(p["red"], face), None
    return FUR0(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("hanumon")
    top = m.bone("hanumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    m.round_box(bd, 0, 0, 7.0, 6.0, 16.0, 32.0, furf, cut=3)
    m.round_box(bd, 0, -0.4, 7.4, 6.4, 30.0, 32.0, metal(P, "green", dark="grey_dark"), cut=2)   # beaded collar
    hd = m.bone("head", bd, (0, 32, -4))
    m.round_box(hd, 0, -4.0, 4.4, 4.0, 30.0, 40.0, furf, cut=2)
    m.round_box(hd, 0, -7.4, 3.0, 1.4, 31.0, 37.0, GREY, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 2.0), 35.0, -8.9, max(sx * 0.6, sx * 2.0), 35.8, -8.7, solid(P, "eye"))
    for i in range(14):                                                                 # shaggy mane
        ang = math.radians(-160 + i * 24)
        spike(m, hd, (4.0 * math.cos(ang), 37.0 + 3.0 * math.sin(ang), -2.0), (math.cos(ang), 0.6 + 0.4 * math.sin(ang), 0.6),
              2.0, 7.0, strands(P, "gold", "gold_dark"), tip=0.9)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 7.0, 28.0, 0))
        rod(m, ab, (sx * 7.0, 28.0, 0), (sx * 11.0, 18.0, -3.0), 4, furf, extend=0.6)
        m.round_box(ab, sx * 11.0, -4.0, 2.6, 2.6, 12.0, 18.0, GREY, cut=1)
        for j in range(3):
            spike(m, ab, (sx * 11.0 + (j - 1) * 1.2, 12.0, -5.0), (0, -1, -0.4), 0.9, 2.6, solid(P, "claw"), tip=0.8)
    ar = "arm_left"                                                                      # bone club
    rod(m, ar, (11.0, 14.0, -5.0), (13.0, 36.0, -8.0), 2, metal(P, "bone", dark="bone_dark"), extend=0)
    m.round_box(ar, 13.0, -8.0, 2.4, 2.4, 34.0, 39.0, metal(P, "bone", dark="bone_dark"), cut=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 16.0, 0))
        rod(m, lg, (sx * 4.0, 17.0, 0), (sx * 6.0, 4.0, -2.0), 4, furf, extend=0.6)
        m.round_box(lg, sx * 6.0, -3.0, 3.0, 3.6, 0.0, 3.4, GREY, cut=1)
    return m
