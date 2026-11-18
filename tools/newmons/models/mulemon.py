"""Mulemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a four-legged pack machine: a rounded silver-and-blue hull with green lens windows and round
shoulder joints, four long thin legs ending in red-tipped spikes, a jointed neck carrying a red-and-white torpedo of a
head with a green lens eye and a jagged jaw, and a yellow beacon on its back. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, gem, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a four-legged pack machine with a silver-and-blue hull, green lens windows, long thin red-tipped legs, a "
        "torpedo head with a green lens eye and a yellow beacon")
BASE = {"silver": (200, 204, 216), "silver_dark": (100, 104, 118), "blue": (70, 90, 190), "blue_dark": (24, 34, 110),
        "red": (210, 50, 40), "white": (240, 240, 244), "green": (60, 200, 110), "green_light": (200, 255, 220),
        "beacon": (255, 240, 120)}
SHINY = {"blue": (190, 70, 70), "blue_dark": (110, 24, 24), "silver": (220, 200, 140), "silver_dark": (150, 120, 60)}


def P(v):
    return pal(BASE, SHINY, v)


HULL = armour(P, "silver", "silver_dark", trim="blue", trim_w=0.4)
BLUE = armour(P, "blue", "blue_dark")
STEEL = metal(P, "silver", dark="silver_dark")
LENS = gem(P, "green", "green_light")


def build():
    m = Model("mulemon")
    top = m.bone("mulemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 22, 0))
    m.round_box(bd, 0, 0, 6.0, 9.0, 18.0, 28.0, HULL, cut=2)                              # rounded hull
    for sx in (-1, 1):
        ball(m, bd, (sx * 6.0, 22.0, -6.0), 3.0, BLUE, layers=3)                          # shoulder joints
        ball(m, bd, (sx * 6.0, 22.0, 6.0), 3.0, BLUE, layers=3)
        m.box(bd, min(sx * 6.0, sx * 6.2), 22.0, -1.6, max(sx * 6.0, sx * 6.2), 24.4, 1.6, LENS)
    for sx, sz, nm in ((1, -1, "leg_front_left"), (-1, -1, "leg_front_right"), (1, 1, "leg_back_left"),
                       (-1, 1, "leg_back_right")):                                       # long thin legs
        lg = m.bone(nm, bd, (sx * 6.0, 22.0, sz * 6.0))
        knee = (sx * 11.0, 16.0, sz * 9.0)
        foot = (sx * 12.0, 3.0, sz * 10.0)
        rod(m, lg, (sx * 6.0, 22.0, sz * 6.0), knee, 2, STEEL, extend=0.3)
        ball(m, lg, knee, 1.4, BLUE, layers=2)
        rod(m, lg, knee, foot, 1, STEEL, extend=0.2, t2=2)
        spike(m, lg, foot, (0, -1, 0), 1.6, 3.0, solid(P, "red"), tip=0.8)
    nk = m.bone("neck", bd, (0, 28, -6))
    for j in range(3):                                                                   # jointed neck
        p0 = (0, 28.0 + j * 2.4, -6.0 - j * 1.0)
        p1 = (0, 30.4 + j * 2.4, -7.0 - j * 1.0)
        rod(m, nk, p0, p1, 2, STEEL, extend=0.2)
    hd = m.bone("head", nk, (0, 35, -9))
    rod(m, hd, (0, 36.0, -4.0), (0, 36.0, -16.0), 4, armour(P, "red", "red", trim="white", trim_w=0.6), extend=0.4)
    spike(m, hd, (0, 36.0, -16.0), (0, 0, -1), 2.0, 3.0, solid(P, "white"), tip=0.8)
    ball(m, hd, (0, 37.6, -10.0), 1.4, LENS, layers=2)
    for j in range(4):
        spike(m, hd, (-1.2 + j * 0.8, 34.0, -12.0 + j), (0, -1, 0), 0.8, 1.4, solid(P, "white"), tip=0.8)
    ball(m, bd, (-3.0, 29.0, 4.0), 1.2, solid(P, "beacon", glow=True), layers=2)            # beacon
    rod(m, bd, (-3.0, 28.0, 4.0), (-3.0, 34.0, 6.0), 1, solid(P, "beacon", glow=True), extend=0.2)
    return m
