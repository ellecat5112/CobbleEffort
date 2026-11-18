"""Shared builder for Palmon and Palmon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): a little plant creature with a green body, a big pink-red tropical flower blooming on its head with a
yellow centre and a curled stem, dark round eyes, and long green vine-like arms ending in claw fingers, root-like feet.
The X-Antibody ("x"): a rainbow flower of blue, yellow and pink petals, a blue leaf cape and a seed-pendant.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

BASE = {"green": (140, 210, 90), "green_dark": (70, 140, 40), "pink": (230, 70, 150), "pink_dark": (150, 30, 90),
        "yellow": (250, 220, 60), "orange": (240, 120, 40), "black": (24, 24, 20), "brown": (140, 100, 50),
        "blue": (60, 110, 210), "cyan": (90, 200, 220), "violet": (150, 70, 170), "gold": (220, 180, 70)}
SHINY = {"green": (110, 190, 170), "green_dark": (40, 120, 100), "pink": (250, 200, 60), "pink_dark": (190, 140, 20)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    BODY = skin(P, "green", dark="green_dark")

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 6, 0))
        ball(m, bd, (0, 9.0, 0.4), 3.6, BODY, layers=4, ry=4.4)
        hd = m.bone("head", bd, (0, 13, 0))
        ball(m, hd, (0, 15.6, -0.2), 3.6, BODY, layers=4, ry=3.2)
        for sx in (-1, 1):
            m.round_box(hd, sx * 1.4, -3.4, 0.8, 0.3, 15.0, 16.8, solid(P, "black"), cut=0)
        petals = ["pink"] * 6 if not x else ["cyan", "yellow", "pink", "violet", "cyan", "yellow"]
        for i, key in enumerate(petals):                                               # big flower
            ang = 2 * math.pi * i / 6
            m.box(hd, -2.0, 18.4, 0, 2.0, 18.9, 5.6, skin(P, key, dark="pink_dark"), rotation=(-20, -math.degrees(ang), 0),
                  pivot=(0, 18.6, 0))
        ball(m, hd, (0, 19.4, 0), 1.2, solid(P, "yellow"), layers=1)
        pts = [(0, 19.6, 0), (0.6, 22.0, 0.4), (1.6, 23.0, 0.4), (1.8, 22.0, 0.2)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "orange" if not x else "green"), extend=0.1)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                             # long vine arms
            ab = m.bone(nm, bd, (sx * 3.0, 11.0, 0))
            pts = [(sx * 3.0, 11.0, 0), (sx * 6.0, 8.0, -1.0), (sx * 8.0, 4.0, -2.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, ab, p0, p1, 1, BODY, extend=0.2, t2=2)
            for f in range(3):
                spike(m, ab, pts[-1], (sx * 0.2 + (f - 1) * 0.4, -1, -0.4), 0.8, 2.6, solid(P, "violet"), tip=0.8)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                             # root feet
            lg = m.bone(nm, top, (sx * 1.6, 5.0, 0))
            rod(m, lg, (sx * 1.6, 6.0, 0), (sx * 2.0, 1.0, 0), 2, BODY, extend=0.2)
            for f in range(3):
                spike(m, lg, (sx * 2.0, 0.6, 0), ((f - 1) * 0.6, -0.2, -1), 0.8, 2.4, solid(P, "brown"), tip=0.8)
        if x:
            for sx in (-1, 1):                                                          # blue leaf cape
                x0, x1 = sorted((sx * 1.0, sx * 5.0))
                m.box(bd, x0, 3.0, 3.6, x1, 12.0, 3.8, skin(P, "blue", dark="pink_dark"), rotation=(10, 0, sx * 10),
                      pivot=(sx * 1.0, 12.0, 3.6))
            ball(m, bd, (0, 10.0, -3.6), 0.8, solid(P, "gold"), layers=1)
        return m

    return build
