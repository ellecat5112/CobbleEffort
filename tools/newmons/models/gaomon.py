"""Gaomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
boxing pup: a blue dog standing on its hind legs with a white muzzle, chest and tail tip, yellow eyes, a long red
headband trailing behind, big red boxing gloves and black claws on its feet. Child stage, 1 block tall.

Front is -z, y is up. 32 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fabric, fur, leather, solid
from _route import pal, tone

HEIGHT = 32
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 14}
LOOK = "a blue boxing pup with a white muzzle and chest, yellow eyes, a long red headband and big red boxing gloves"
BASE = {"blue": (50, 100, 200), "blue_dark": (20, 50, 130), "white": (246, 246, 250), "white_dark": (190, 192, 206),
        "red": (210, 40, 30), "red_dark": (130, 14, 10), "eye": (250, 220, 40), "pupil": (16, 16, 20),
        "black": (30, 28, 32), "nose": (30, 28, 32)}
SHINY = {"blue": (60, 60, 70), "blue_dark": (24, 24, 30)}


def P(v):
    return pal(BASE, SHINY, v)


BLUE = fur(P, "blue", "blue_dark", length=0.8, density=2.2)
WHITE = fur(P, "white", "white_dark", length=0.8, density=2.2)
GLOVE = leather(P, "red", "red_dark")


def bodyf(x, y, z, face, variant, box=None, **k):
    if face == "north" and abs(x) < 2.2:
        return WHITE(x, y, z, face, variant, box=box, **k)
    return BLUE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("gaomon")
    top = m.bone("gaomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0.4, 3.4, 2.8, 9.0, 19.0, bodyf, cut=1)
    hd = m.bone("head", bd, (0, 20, -1))
    m.round_box(hd, 0, -0.4, 3.6, 3.4, 19.0, 26.0, BLUE, cut=2)
    m.round_box(hd, 0, -4.8, 2.0, 1.8, 19.6, 22.6, WHITE, cut=1)                    # white muzzle
    m.box(hd, -0.7, 21.8, -6.8, 0.7, 22.8, -6.5, solid(P, "nose"))
    for sx in (-1, 1):
        m.round_box(hd, sx * 1.6, -3.5, 0.8, 0.3, 22.8, 24.2, solid(P, "eye"), cut=0)
        m.box(hd, sx * 1.6 - 0.2, 23.0, -3.9, sx * 1.6 + 0.2, 23.8, -3.7, solid(P, "pupil"))
        spike(m, hd, (sx * 2.6, 25.4, 0.4), (sx * 0.4, 0.6, 0.6), 1.6, 3.0, BLUE, tip=0.8)      # folded ears
    m.round_box(hd, 0, -0.2, 3.8, 3.6, 24.0, 25.2, fabric(P, "red", "red_dark"), cut=1)       # headband
    for j, (p0, p1) in enumerate((((1.0, 24.6, 3.4), (4.0, 28.0, 10.0)), ((4.0, 28.0, 10.0), (6.0, 32.0, 16.0)))):
        rod(m, hd, p0, p1, 1, fabric(P, "red", "red_dark"), extend=0.3, t2=2)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.4, 17.0, -1.0))
        rod(m, ab, (sx * 3.4, 17.0, -1.0), (sx * 4.6, 13.0, -4.0), 1, BLUE, extend=0.3, t2=2)
        m.round_box(ab, sx * 4.8, -5.4, 2.2, 2.2, 11.0, 15.6, GLOVE, cut=1)                    # boxing gloves
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.0, 10.0, 0))
        rod(m, lg, (sx * 2.0, 10.0, 0), (sx * 2.4, 5.0, 1.4), 2, BLUE, extend=0.4)
        rod(m, lg, (sx * 2.4, 5.0, 1.4), (sx * 2.4, 1.0, 0.0), 2, BLUE, extend=0.4)
        m.round_box(lg, sx * 2.4, -1.4, 1.4, 2.2, 0.0, 1.6, WHITE, cut=1)
        for j in range(3):
            spike(m, lg, (sx * 2.4 + (j - 1) * 0.9, 0.5, -3.4), (0, -0.2, -1), 0.8, 1.6, solid(P, "black"), tip=0.8)
    tb = m.bone("tail", bd, (0, 11, 3))
    rod(m, tb, (0, 11.0, 3.0), (2.0, 15.0, 8.0), 2, BLUE, extend=0.4)
    rod(m, tb, (2.0, 15.0, 8.0), (3.0, 19.0, 10.0), 2, WHITE, extend=0.4)
    return m
