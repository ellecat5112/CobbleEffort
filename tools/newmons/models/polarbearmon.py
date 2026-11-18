"""Polar Bearmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a round white polar bear snowboarder in a puffy cyan ski jacket with a blue-and-white
striped scarf, ski goggles pushed up on its head, yellow mittens, two snow cannons strapped over its shoulders, an ice
ski pole in one hand, pink boots clipped to an ice-blue snowboard. 25 blocks tall.

Front is -z, y is up. 56 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, fur, metal, solid
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 4}
LOOK = "a round white polar bear snowboarder in a puffy cyan ski jacket and striped scarf with goggles, yellow mittens and twin snow cannons"
BASE = {"white": (246, 248, 252), "white_dark": (180, 196, 214), "cyan": (70, 200, 230), "cyan_dark": (20, 120, 170),
        "blue": (40, 70, 170), "blue_dark": (16, 30, 100), "yellow": (250, 210, 40), "yellow_dark": (200, 150, 10),
        "pink": (230, 70, 140), "pink_dark": (150, 20, 80), "ice": (160, 230, 250), "black": (24, 24, 30),
        "goggle": (200, 60, 120), "steel": (40, 50, 80), "steel_dark": (14, 18, 40)}
SHINY = {"cyan": (250, 140, 60), "cyan_dark": (190, 80, 20), "pink": (60, 180, 90), "pink_dark": (20, 110, 40)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "white", "white_dark", length=1.2, density=1.6)
JACKET = fabric(P, "cyan", "cyan_dark", axis="y", period=3.0)


def scarff(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["blue"] if (x + y) % 2.4 < 1.2 else p["white"], face), None


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 2.0, y - 44.6) < 0.8:
                return tone(p["black"], face), None
        if math.hypot(x, (y - 42.6) * 1.3) < 1.0:
            return tone(p["black"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("polarbearmon")
    top = m.bone("polarbearmon", None, (0, 0, 0))
    m.box(top, -18.0, 0.0, -5.0, 18.0, 1.0, 5.0, solid(P, "ice"))                         # snowboard
    bd = m.bone("body", top, (0, 20, 0))
    ball(m, bd, (0, 26.0, 0), 11.0, JACKET, layers=7, ry=11.0)                          # puffy jacket
    for j in range(5):
        m.round_box(bd, 0, 0, 11.4 - abs(j - 2) * 1.6, 11.0 - abs(j - 2) * 1.6, 18.6 + j * 3.4, 19.4 + j * 3.4,
                    solid(P, "cyan_dark"), cut=3)
    m.box(bd, -0.4, 16.0, -11.6, 0.4, 36.0, -11.2, metal(P, "steel"))                     # zip
    m.round_box(bd, 0, 0, 6.6, 6.0, 35.0, 38.0, scarff, cut=2)                             # scarf
    rod(m, bd, (3.0, 36.0, -5.0), (5.0, 28.0, -9.0), 2, scarff, extend=0.2, t2=1)
    hd = m.bone("head", bd, (0, 38, 0))
    ball(m, hd, (0, 44.0, -0.6), 6.0, headf, layers=5, ry=5.6)
    m.round_box(hd, 0, -5.6, 2.6, 1.6, 41.0, 44.0, FUR, cut=1)                            # muzzle
    for sx in (-1, 1):
        ball(m, hd, (sx * 4.6, 49.4, 0), 1.6, FUR, layers=2)
    m.round_box(hd, 0, 0, 6.4, 6.4, 47.6, 49.2, solid(P, "blue"), cut=2)                   # goggle strap
    for sx in (-1, 1):
        m.round_box(hd, sx * 2.2, -5.6, 2.0, 0.8, 47.0, 50.0, solid(P, "goggle", glow=False), cut=0)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 10.0, 30.0, 0))
        rod(m, ab, (sx * 10.0, 30.0, 0), (sx * 15.0, 34.0, -4.0), 4, JACKET, extend=0.4)
        ball(m, ab, (sx * 16.0, 36.0, -5.0), 3.2, solid(P, "yellow"), layers=3)           # mittens
        m.round_box(ab, sx * 16.0, -5.0, 3.2, 3.2, 32.0, 33.6, FUR, cut=1)
    rod(m, "arm_left", (16.0, 36.0, -5.0), (19.0, 2.0, -8.0), 1, solid(P, "ice"), extend=0.4)  # ice ski pole
    m.round_box("arm_left", 19.0, -8.0, 1.6, 1.6, 6.0, 6.8, solid(P, "ice"), cut=0)
    for sx in (-1, 1):                                                                    # twin snow cannons
        rod(m, bd, (sx * 6.0, 32.0, 8.0), (sx * 9.0, 52.0, 2.0), 5, metal(P, "steel", dark="steel_dark"), extend=0.4)
        m.round_box(bd, sx * 9.2, 1.6, 1.4, 1.4, 52.0, 53.0, solid(P, "black"), cut=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 16.0, 0))
        m.round_box(lg, sx * 4.0, 0, 3.0, 3.0, 8.0, 17.0, FUR, cut=1)
        m.round_box(lg, sx * 4.0, -1.0, 3.4, 4.6, 1.0, 9.0,
                    fabric(P, "pink", "pink_dark", axis="y"), cut=1)                      # pink boots
    return m
