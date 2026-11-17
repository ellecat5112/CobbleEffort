"""Ebidramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the lobster dragon. A long armoured crimson crustacean with a segmented shell, a fierce dragon-like
head full of fangs with long whip antennae, two huge serrated claws on jointed arms, many small walking legs and a fan
of violet tail fins. 15 blocks long.

Front is -z, y is up. 22 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, solid
from _route import pal, tone

HEIGHT = 22
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a long armoured crimson lobster dragon with a fanged head, whip antennae, two huge serrated claws, many little "
        "legs and violet tail fins")
BASE = {"red": (200, 40, 30), "red_dark": (100, 10, 10), "red_light": (250, 130, 100), "violet": (150, 60, 160),
        "cream": (240, 220, 180), "tooth": (250, 248, 240), "eye": (250, 220, 60), "mouth": (100, 20, 30)}
SHINY = {"red": (60, 80, 180), "red_dark": (20, 30, 90), "red_light": (140, 170, 250), "violet": (230, 180, 60)}


def P(v):
    return pal(BASE, SHINY, v)


SHELL = armour(P, "red", "red_dark", light="red_light", trim="red_dark", trim_w=0.4)


def build():
    m = Model("ebidramon")
    top = m.bone("ebidramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    for i in range(7):                                                                # segmented shell
        r = 5.0 - abs(i - 2) * 0.5
        m.round_box(bd, 0, -8.0 + i * 4.0, r, 2.2, 4.0 + (2 - abs(i - 2)) * 0.3, 10.0 + r * 0.4, SHELL, cut=1)
    hd = m.bone("head", bd, (0, 10, -12))
    m.round_box(hd, 0, -14.0, 3.6, 4.0, 6.0, 12.0, SHELL, cut=1)
    spike(m, hd, (0, 11.0, -17.0), (0, 0.2, -1), 2.0, 5.0, SHELL, tip=0.5)            # rostrum
    m.box(hd, -2.6, 6.0, -18.0, 2.6, 7.4, -12.0, solid(P, "mouth"))
    for j in range(4):
        for sx in (-1, 1):
            spike(m, hd, (sx * 2.2, 7.4, -17.0 + j * 1.4), (0, -1, 0), 0.7, 1.4, solid(P, "tooth"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 3.4, sx * 3.8), 10.0, -16.0, max(sx * 3.4, sx * 3.8), 11.2, -14.6, solid(P, "eye", glow=True))
        pts = [(sx * 1.6, 11.0, -17.0), (sx * 5.0, 15.0, -22.0), (sx * 10.0, 16.0, -18.0), (sx * 14.0, 12.0, -10.0)]
        for p0, p1 in zip(pts, pts[1:]):                                              # whip antennae
            rod(m, hd, p0, p1, 1, solid(P, "red"), extend=0.4)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # huge serrated claws
        ab = m.bone(nm, bd, (sx * 4.0, 8.0, -10.0))
        rod(m, ab, (sx * 4.0, 8.0, -10.0), (sx * 9.0, 7.0, -16.0), 2, SHELL, extend=0.5)
        rod(m, ab, (sx * 9.0, 7.0, -16.0), (sx * 9.0, 8.0, -22.0), 3, SHELL, extend=0.5)
        m.round_box(ab, sx * 9.0, -25.0, 3.0, 4.0, 5.0, 11.0, SHELL, cut=1)
        for jaw, y0 in ((0, 9.0), (1, 5.4)):
            m.box(ab, sx * 9.0 - 1.2, y0, -34.0, sx * 9.0 + 1.2, y0 + 1.6, -28.0, SHELL)
            for j in range(4):
                spike(m, ab, (sx * 9.0, y0 + (0 if jaw else 1.6), -33.0 + j * 1.4), (0, -1 if jaw == 0 else 1, 0), 0.6,
                      1.2, solid(P, "cream"))
    for i in range(4):                                                                # little walking legs
        for sx in (-1, 1):
            nm = ("leg_front_" if i < 2 else "leg_back_") + ("left" if sx > 0 else "right")
            if i in (0, 2):                                                       # two legs on each leg bone
                m.bone(nm, bd, (sx * 4.0, 6.0, -6.0 + i * 4.0))
            lb = nm
            z = -6.0 + i * 4.0
            rod(m, lb, (sx * 4.0, 6.0, z), (sx * 8.0, 4.0, z), 1, SHELL, extend=0.3)
            rod(m, lb, (sx * 8.0, 4.0, z), (sx * 9.0, 0.0, z - 1.0), 1, SHELL, extend=0.3)
    tl = m.bone("tail", bd, (0, 8, 18))
    for j in range(5):                                                                # violet tail fins
        ang = math.radians(-50 + j * 25)
        m.box(tl, -1.4, 7.0, 18.0, 1.4, 7.0, 25.0, solid(P, "violet"), rotation=(0, math.degrees(ang), 0),
              pivot=(0, 7.0, 18.0))
    return m
