"""Gyukimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the ox-demon: a hunched violet-furred demon with long curled horns and a white skull-mask, its arms
wrapped in bandages and talisman papers, huge red claws, a shaggy hide, and on its back a red armoured shell sprouting
two great cannons with glowing green barrels. 25 blocks tall.

Front is -z, y is up. 44 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, fabric, fur, gem, metal, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(25, HEIGHT, 4.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("a hunched violet-furred ox-demon with curled horns, a white skull-mask, bandaged arms with talismans, red claws "
        "and a red armoured shell with two green-barrelled cannons")
BASE = {"violet": (130, 90, 150), "violet_dark": (70, 40, 90), "violet_light": (190, 160, 210), "bone": (236, 232, 220),
        "bone_dark": (170, 166, 150), "bandage": (236, 230, 216), "bandage_dark": (180, 170, 150), "red": (190, 40, 40),
        "red_dark": (110, 14, 18), "talisman": (240, 220, 160), "green": (80, 230, 110), "green_light": (200, 255, 200),
        "steel": (170, 176, 190), "steel_dark": (80, 86, 100), "claw": (210, 40, 40), "eye": (250, 220, 60)}
SHINY = {"violet": (80, 120, 150), "violet_dark": (30, 60, 90), "red": (40, 60, 150), "red_dark": (14, 24, 80)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "violet", "violet_dark", tip="violet_light", length=1.6, density=2.0)
BAND = fabric(P, "bandage", "bandage_dark", axis="y", period=1.2)


def bandf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west") and (y % 6.0) < 1.6 and (x * 0.7 % 2.0) < 1.0:
        return tone(p["talisman"], face), None
    return BAND(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("gyukimon")
    top = m.bone("gyukimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    m.round_box(bd, 0, 1.0, 8.0, 7.0, 12.0, 28.0, FUR, cut=3)
    m.round_box(bd, 0, 9.0, 9.0, 5.0, 14.0, 30.0, armour(P, "red", "red_dark", trim="steel"), cut=3)   # red shell
    for sx in (-1, 1):                                                                     # green-barrelled cannons
        rod(m, bd, (sx * 4.0, 28.0, 10.0), (sx * 6.0, 42.0, 14.0), 4, metal(P, "steel", dark="steel_dark"), extend=0)
        m.round_box(bd, sx * 6.0, 14.0, 1.6, 1.6, 38.0, 44.0, gem(P, "green", "green_light"), cut=1)
    hd = m.bone("head", bd, (0, 28, -6))
    m.round_box(hd, 0, -7.0, 4.0, 3.4, 24.0, 32.0, FUR, cut=2)
    m.round_box(hd, 0, -10.0, 3.0, 0.8, 25.0, 31.0, metal(P, "bone", dark="bone_dark"), cut=0)          # skull-mask
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.0), 28.0, -11.0, max(sx * 0.8, sx * 2.0), 29.0, -10.8, solid(P, "eye", glow=True))
        pts = [(sx * 3.4, 31.0, -6.0), (sx * 8.0, 34.0, -4.0), (sx * 11.0, 32.0, -1.0), (sx * 10.0, 29.0, 1.0)]
        for p0, p1 in zip(pts, pts[1:]):                                                     # curled horns
            rod(m, hd, p0, p1, 1, metal(P, "bone", dark="bone_dark"), extend=0.3, t2=2)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 8.0, 26.0, -2.0))
        rod(m, ab, (sx * 8.0, 26.0, -2.0), (sx * 13.0, 16.0, -6.0), 4, bandf, extend=0.6)
        rod(m, ab, (sx * 13.0, 16.0, -6.0), (sx * 13.0, 6.0, -10.0), 4, bandf, extend=0.6)
        for j in range(4):
            spike(m, ab, (sx * 13.0 + (j - 1.5) * 1.4, 5.0, -10.0), (0, -0.8, -0.8), 1.2, 4.6, solid(P, "claw"), tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 5.0, 14.0, 0))
        rod(m, lg, (sx * 5.0, 14.0, 0), (sx * 6.0, 3.0, -1.0), 5, FUR, extend=0.6)
        for j in range(3):
            spike(m, lg, (sx * 6.0 + (j - 1) * 1.8, 1.0, -4.0), (0, -0.3, -1), 1.4, 4.0, solid(P, "claw"), tip=0.8)
    return m
