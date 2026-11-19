"""Spadamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little lion knight: a cream-furred lion cub with a big spiky silver-white mane, a blue spade-shaped
helm-mask, blue shoulder guards and boots, white gloves, a tufted tail, and a long curved ice-blue blade held high.
1 block. Child stage.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, fur, gem, solid, strands
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a little cream lion cub knight with a spiky silver mane, a blue spade helm-mask, blue guards and boots and a long ice-blue blade"
BASE = {"cream": (250, 240, 210), "cream_dark": (210, 190, 150), "silver": (230, 232, 240), "silver_dark": (160, 164, 180),
        "blue": (50, 110, 210), "blue_dark": (20, 50, 140), "white": (252, 252, 252), "ice": (150, 220, 250),
        "eye": (240, 200, 40), "black": (30, 26, 24)}
SHINY = {"blue": (210, 60, 70), "blue_dark": (120, 20, 26), "ice": (250, 160, 170)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "cream", "cream_dark", length=1.0)
BLUE = armour(P, "blue", "blue_dark")


def build():
    m = Model("spadamon")
    top = m.bone("spadamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7, 0))
    m.round_box(bd, 0, 0, 3.0, 2.6, 7.0, 15.0, FUR, cut=1)
    hd = m.bone("head", bd, (0, 15, 0))
    ball(m, hd, (0, 19.0, -0.2), 3.6, FUR, layers=3)
    m.round_box(hd, 0, -2.8, 3.2, 1.0, 18.6, 22.0, BLUE, cut=1)                               # spade helm-mask
    spike(m, hd, (0, 22.0, -3.0), (0, 1, 0), 1.6, 2.0, BLUE, tip=0.8)
    m.box(hd, -1.0, 19.6, -3.9, 1.0, 20.6, -3.7, solid(P, "eye"))
    for j in range(12):                                                                  # spiky silver mane
        ang = math.radians(-120 + j * 22)
        spike(m, hd, (3.0 * math.sin(ang), 19.6 + 3.0 * math.cos(ang), 1.0), (math.sin(ang), math.cos(ang) + 0.2, 0.5),
              1.6, 5.0, strands(P, "silver", "silver_dark"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.0, 14.0, 0))
        m.round_box(ab, sx * 3.6, 0, 1.6, 1.6, 12.6, 15.4, BLUE, cut=0)
        rod(m, ab, (sx * 3.4, 13.0, 0), (sx * 5.0, 9.6, -1.6), 2, FUR, extend=0.3)
        ball(m, ab, (sx * 5.2, 9.2, -2.0), 1.4, solid(P, "white"), layers=2)
    m.box("arm_right", -5.6, 9.0, -3.0, -4.8, 30.0, -1.4, gem(P, "ice", "white"), rotation=(0, 0, 10),
          pivot=(-5.2, 9.0, -2.2))                                                         # ice-blue blade
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.8, 7.0, 0))
        rod(m, lg, (sx * 1.8, 7.0, 0), (sx * 2.0, 2.6, 0), 2, FUR, extend=0.3)
        m.round_box(lg, sx * 2.0, -0.8, 1.6, 2.4, 0.0, 3.0, BLUE, cut=0)
    tl = m.bone("tail", bd, (0, 8, 3))
    rod(m, tl, (0, 8.0, 3.0), (2.0, 5.0, 8.0), 1, FUR, extend=0.2, t2=1)
    ball(m, tl, (2.4, 5.0, 8.6), 1.0, strands(P, "silver", "silver_dark"), layers=1)
    return m
