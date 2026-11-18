"""Kokabuterimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the little beetle warrior: a squat blue armoured beetle with a green-eyed visored face, a long blue horn tipped with
red, red-edged shell spines, big curved silver claws on both arms and stubby clawed legs. Child stage, 1 block tall.

Front is -z, y is up. 26 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 26
SCALE, HITBOX = sized(1.0, HEIGHT, 2.2)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a squat blue armoured beetle with a green-eyed visored face, a long red-tipped horn and big curved silver claws"
BASE = {"blue": (40, 70, 180), "blue_dark": (14, 24, 90), "blue_light": (120, 160, 240), "red": (210, 40, 40),
        "silver": (220, 224, 234), "silver_dark": (110, 116, 130), "eye": (90, 230, 90), "black": (24, 24, 30)}
SHINY = {"blue": (200, 60, 50), "blue_dark": (110, 20, 14), "blue_light": (250, 140, 120)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "blue", "blue_dark", light="blue_light", trim="red", trim_w=0.2)
SILVER = metal(P, "silver", dark="silver_dark")


def build():
    m = Model("kokabuterimon")
    top = m.bone("kokabuterimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 1.0, 4.6, 4.6, 6.0, 15.0, ARM, cut=2)
    for sx in (-1, 1):                                                               # red-edged shell spines
        spike(m, bd, (sx * 4.0, 14.0, 2.0), (sx * 0.6, 1, 0.4), 1.6, 4.0, solid(P, "red"), tip=0.8)
    hd = m.bone("head", bd, (0, 15, -2))
    m.round_box(hd, 0, -2.0, 2.6, 2.4, 14.0, 19.0, ARM, cut=1)
    m.round_box(hd, 0, -4.4, 2.0, 0.3, 15.6, 17.0, solid(P, "black"), cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.4, sx * 1.6), 15.8, -4.8, max(sx * 0.4, sx * 1.6), 16.8, -4.7, solid(P, "eye", glow=True))
    pts = [(0, 18.6, -2.0), (0, 22.0, -3.0), (0, 25.0, -1.0)]                         # long horn
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, hd, p0, p1, 2 - j, ARM, extend=0.4)
    spike(m, hd, pts[-1], (0, 0.6, 1), 1.4, 3.0, solid(P, "red"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # curved silver claws
        ab = m.bone(nm, bd, (sx * 4.6, 12.0, -1.0))
        rod(m, ab, (sx * 4.6, 12.0, -1.0), (sx * 7.0, 9.0, -3.0), 2, ARM, extend=0.4)
        for j in range(3):
            pts = [(sx * 7.0, 9.0, -3.0), (sx * (8.0 + j * 0.8), 6.0 - j, -5.0), (sx * (7.0 + j * 0.8), 3.0 - j, -6.4)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, ab, p0, p1, 1, SILVER, extend=0.2, t2=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.6, 6.0, 0))
        rod(m, lg, (sx * 2.6, 6.4, 0), (sx * 3.0, 1.4, -0.6), 2, ARM, extend=0.4)
        for j in range(3):
            spike(m, lg, (sx * 3.0 + (j - 1) * 0.8, 0.8, -1.4), (0, -0.2, -1), 0.9, 2.4, SILVER, tip=0.8)
    return m
