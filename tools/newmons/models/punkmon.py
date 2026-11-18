"""Punkmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a punk-rock demon dragon: a lean violet reptile in a black studded leather harness and straps, a
green mohawk, a snarling dark snout, a torn red bandana, silver claws on its hands and feet, a black-banded tail
ending in a violet arrowhead, and a golden studded knuckle bracelet glowing with fire runes. 15 blocks tall.

Front is -z, y is up. 60 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import leather, metal, scales, solid, strands
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(15, HEIGHT, 3.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a lean violet punk dragon in a black studded harness with a green mohawk, a torn red bandana, silver claws and an arrow tail"
BASE = {"violet": (120, 70, 190), "violet_dark": (60, 30, 110), "black": (30, 28, 34), "black_dark": (10, 10, 12),
        "green": (60, 200, 90), "green_dark": (20, 120, 40), "red": (200, 30, 40), "steel": (210, 214, 226),
        "steel_dark": (110, 114, 126), "gold": (236, 190, 60), "gold_dark": (150, 100, 20), "eye": (250, 200, 40),
        "mouth": (150, 20, 40), "tooth": (250, 250, 240), "fire": (250, 140, 40)}
SHINY = {"violet": (60, 140, 200), "violet_dark": (20, 80, 140), "green": (240, 80, 160), "green_dark": (150, 30, 90)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "violet", "violet_dark", size=1.2)
LEATHER = leather(P, "black", "black_dark", stitch="steel")
STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("punkmon")
    mats = {"skin": HIDE, "pelvis": LEATHER, "hand": HIDE, "finger": HIDE, "claw": STEEL, "talon": STEEL}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.9, claws=True, talons=True, digitigrade=True,
                 name="punkmon")
    bd = a["body"]
    for sx in (-1, 1):                                                                   # harness straps
        m.box(bd, sx * 2.0 - 0.8, 34.0, -4.6, sx * 2.0 + 0.8, 51.0, -3.8, LEATHER,
              rotation=(0, 0, sx * 18), pivot=(sx * 2.0, 42.0, -4.2))
        for j in range(4):
            m.box(bd, sx * 2.6 - 0.4, 37.0 + j * 3.6, -4.9, sx * 2.6 + 0.4, 37.8 + j * 3.6, -4.5, STEEL)
    m.round_box(bd, 0, 0, 4.8, 3.6, 32.0, 34.0, LEATHER, cut=1)                             # belt
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 2.6, 3.4, 53.6, 59.4, HIDE, cut=1)
    m.round_box(hd, 0, -5.4, 1.8, 2.2, 53.4, 56.4, solid(P, "black"), cut=1)                # dark snout
    m.box(hd, -1.4, 53.6, -7.8, 1.4, 54.4, -4.0, solid(P, "mouth"))
    for j in range(3):
        for sx in (-1, 1):
            spike(m, hd, (sx * 1.2, 54.4, -7.2 + j * 1.2), (0, -1, 0), 0.8, 1.0, solid(P, "tooth"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.5, sx * 2.7), 57.0, -3.4, max(sx * 2.5, sx * 2.7), 57.8, -2.0, solid(P, "eye", glow=True))
    for j in range(7):                                                                   # green mohawk
        spike(m, hd, (0, 59.0 - abs(j - 3) * 0.4, -3.0 + j * 1.2), (0, 1, 0.2 + j * 0.08), 1.4, 5.0 + (3 - abs(j - 3)),
              strands(P, "green", "green_dark"), tip=0.8)
    m.round_box(hd, 0, -0.6, 2.9, 3.6, 52.6, 53.8, solid(P, "red"), cut=1)                  # torn bandana
    rod(m, hd, (2.4, 53.0, 3.0), (6.0, 50.0, 7.0), 1, solid(P, "red"), extend=0.2, t2=2)
    w = a["arm_right"]["wrist"]                                                          # gold knuckle bracelet
    m.round_box(a["arm_right"]["bone"], w[0], w[2], 2.0, 2.0, w[1] + 0.4, w[1] + 3.0, metal(P, "gold", dark="gold_dark"),
                cut=1)
    for j in range(3):
        spike(m, a["arm_right"]["bone"], (w[0] - 1.6, w[1] + 1.6, w[2] - 1.0 + j), (-1, 0.4, 0), 0.8, 2.4,
              solid(P, "fire", glow=True), tip=0.8)
    tl = m.bone("tail", bd, (0, 32, 3))                                                  # banded arrow tail
    pts = [(0, 32.0, 3.0), (0, 26.0, 10.0), (2.0, 30.0, 16.0), (3.0, 40.0, 18.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 3 - i, LEATHER if i == 1 else HIDE, extend=0.4)
    spike(m, tl, pts[-1], (0.1, 1, 0.1), 2.4, 4.0, HIDE, tip=0.8)
    return m
