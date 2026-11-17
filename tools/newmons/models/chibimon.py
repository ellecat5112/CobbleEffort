"""Chibimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little blue baby dragon. A round blue body with a white belly and muzzle, big red-brown eyes, a
tall pointed horn and two swept pointed ears, stubby arms and feet and a short pointed tail. Baby II.

Front is -z, y is up. 26 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, skin, solid
from _route import pal, tone

HEIGHT = 26
SCALE, HITBOX = sized(0.5, HEIGHT, 0.55)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 16}
LOOK = "a little round blue baby dragon with a white belly, big red-brown eyes, a tall horn and swept pointed ears"
BASE = {"blue": (60, 110, 210), "blue_dark": (24, 54, 140), "blue_light": (130, 170, 240), "white": (250, 250, 252),
        "eye": (190, 60, 40), "pupil": (30, 10, 10), "mouth": (220, 80, 90), "cheek": (250, 170, 180)}
SHINY = {"blue": (230, 160, 60), "blue_dark": (170, 100, 20), "blue_light": (255, 210, 140)}


def P(v):
    return pal(BASE, SHINY, v)


BLUE = skin(P, "blue", dark="blue_dark", light="blue_light", var=0.03)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            c = eye(p, x - sx * 2.4, y - 15.6, 1.4, "eye")
            if c is not None:
                return c, None
        if y < 13.6 and abs(x) < 3.4 - max(0.0, (y - 11.0) * 0.6):
            if 11.6 < y < 12.6 and abs(x) < 1.0:
                return tone(p["mouth"], face), None
            return tone(p["white"], face), None
    return BLUE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("chibimon")
    top = m.bone("chibimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    ball(m, bd, (0, 13.0, 0), 6.6, bodyf, layers=6)
    m.round_box(bd, 0, -2.0, 3.4, 3.0, 4.0, 9.0, BLUE, cut=1)                      # little body below
    m.box(bd, -2.4, 4.6, -5.2, 2.4, 8.6, -4.8, solid(P, "white"))
    hd = m.bone("head", bd, (0, 19, 0))
    spike(m, hd, (0, 19.0, -1.0), (0.1, 1, 0.2), 2.6, 6.0, BLUE, tip=0.6)            # tall horn
    for sx in (-1, 1):
        spike(m, hd, (sx * 4.6, 17.0, 0.6), (sx, 0.5, 0.4), 2.4, 6.0, BLUE, tip=0.5)  # swept ears
        ab = m.bone("arm_left" if sx > 0 else "arm_right", bd, (sx * 3.2, 8.0, 0))
        spike(m, ab, (sx * 3.0, 8.0, -0.6), (sx, -0.6, -0.3), 1.8, 3.4, BLUE, tip=0.6)
        lg = m.bone("leg_left" if sx > 0 else "leg_right", top, (sx * 2.0, 4.0, 0))
        m.round_box(lg, sx * 2.0, -0.6, 1.6, 2.0, 0.0, 4.4, BLUE, cut=1)
    tl = m.bone("tail", bd, (0, 6, 3))
    spike(m, tl, (0, 6.0, 3.0), (0.3, 0.3, 1), 1.8, 4.0, BLUE, tip=0.4)
    return m
