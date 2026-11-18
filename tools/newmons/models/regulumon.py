"""Regulumon (a Digimon of the CobbleEffort: Digital crossover; built after the manga sketch on wikimon.net, its only
picture): a swooping gargoyle-beast: a squat brown hide, a great wild mane of white hair round a snarling tusked face
with blazing yellow eyes and a white beard, pointed ears, wide lime-green bat wings, banded wrists and dark ragged
leggings. 35 blocks.

Front is -z, y is up. 48 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, bat_wing
from _digidetail import fabric, fur, skin, solid, strands
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "floater"
K = 3
LOOK = "a swooping brown gargoyle-beast with a great wild white mane, a snarling tusked face, blazing yellow eyes and lime-green bat wings"
BASE = {"hide": (170, 110, 80), "hide_dark": (110, 60, 40), "white": (240, 240, 236), "white_dark": (180, 180, 176),
        "green": (170, 220, 60), "green_dark": (90, 150, 20), "eye": (250, 220, 40), "black": (30, 28, 30),
        "tusk": (250, 248, 236), "band": (60, 90, 40), "mouth": (120, 30, 30)}
SHINY = {"hide": (90, 90, 110), "hide_dark": (40, 40, 56), "green": (200, 60, 120), "green_dark": (130, 20, 70)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = skin(P, "hide", dark="hide_dark")
MANE = strands(P, "white", "white_dark")


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 2.0) < 1.2 and abs(y - 33.6 + (x * sx - 2.0) * 0.5) < 0.5:
                return p["eye"], p["eye"]
        if 28.6 < y < 30.6 and abs(x) < 2.0:
            return tone(p["mouth"], face), None
    return HIDE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("regulumon")
    top = m.bone("regulumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    ball(m, bd, (0, 22.0, 1.0), 7.0, HIDE, layers=5, ry=7.6)
    hd = m.bone("head", bd, (0, 30, -2))
    m.round_box(hd, 0, -3.0, 4.0, 3.6, 27.0, 36.0, facef, cut=1)
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.6, 29.0, -6.4), (sx * 0.2, 1, -0.2), 0.9, 2.2, solid(P, "tusk"), tip=0.8)
        spike(m, hd, (sx * 4.0, 36.0, -2.0), (sx * 0.8, 1, 0.2), 1.4, 4.0, HIDE, tip=0.8)          # pointed ears
    for j in range(12):                                                                  # wild white mane
        ang = math.radians(-100 + j * 18)
        spike(m, hd, (4.2 * math.sin(ang), 33.0 + 3.4 * math.cos(ang), 1.0), (math.sin(ang), math.cos(ang) + 0.3, 0.6),
              2.0, 7.0 + (j % 3) * 2.0, MANE, tip=0.8)
    for j in range(3):                                                                   # white beard
        spike(m, hd, ((j - 1) * 1.4, 27.4, -5.0), ((j - 1) * 0.2, -1, -0.3), 1.4, 4.0, MANE, tip=0.8)
    for sx in (-1, 1):                                                                   # lime-green bat wings
        bat_wing(m, bd, (sx * 5.0, 26.0, 3.0), 30.0, 16.0, 4, HIDE, skin(P, "green", dark="green_dark"), side=sx,
                 sweep=20)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 6.0, 24.0, -2.0))
        rod(m, ab, (sx * 6.0, 24.0, -2.0), (sx * 8.0, 16.0, -6.0), 2, HIDE, extend=0.3)
        m.round_box(ab, sx * 8.0, -6.0, 1.6, 1.6, 15.0, 17.0, solid(P, "band"), cut=0)
        for f in range(3):
            spike(m, ab, (sx * 8.0 + (f - 1) * 0.8, 14.6, -6.4), ((f - 1) * 0.2, -1, -0.3), 0.8, 2.0, solid(P, "black"),
                  tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, bd, (sx * 3.0, 16.0, 2.0))
        m.round_box(lg, sx * 3.0, 3.0, 2.4, 2.4, 8.0, 17.0, fabric(P, "black", "black", axis="y"), cut=1)
        m.round_box(lg, sx * 3.0, 2.0, 1.8, 2.6, 5.0, 8.0, HIDE, cut=0)
    return m
