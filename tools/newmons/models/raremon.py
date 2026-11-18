"""Raremon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a slumping blue sludge of rotten data, oozing and dripping, with bolted steel plates and a goggle-eyed
metal faceplate sunk in its head, a gaping fanged maw breathing a sickly yellow gas, long raking claws of bone, and
a trail of sludge behind it. 15 blocks.

Front is -z, y is up. 30 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, riveted, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 3}
LOOK = "a slumping blue sludge with bolted steel plates, a goggle-eyed metal faceplate, a fanged maw breathing yellow gas and bone claws"
BASE = {"blue": (110, 130, 210), "blue_dark": (50, 60, 140), "steel": (150, 154, 166), "steel_dark": (70, 74, 86),
        "eye": (230, 40, 40), "mouth": (130, 20, 40), "bone": (236, 230, 214), "gas": (240, 220, 100, 170)}
SHINY = {"blue": (140, 190, 110), "blue_dark": (70, 120, 50)}


def P(v):
    return pal(BASE, SHINY, v)


SLUDGE = skin(P, "blue", dark="blue_dark", var=0.08)
PLATE = riveted(P, "steel", "steel_dark")


def build():
    m = Model("raremon")
    top = m.bone("raremon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    for c, r, ry in (((0, 8.0, 6.0), 10.0, 7.0), ((0, 14.0, -2.0), 8.0, 8.0), ((0, 4.0, 14.0), 7.0, 4.0)):
        ball(m, bd, c, r, SLUDGE, layers=5, ry=ry)
    for j in range(8):                                                                   # drips
        ang = 2 * math.pi * j / 8
        spike(m, bd, (9.0 * math.cos(ang), 6.0, 6.0 + 9.0 * math.sin(ang)), (0, -1, 0), 1.6, 5.0, SLUDGE, tip=0.8)
    hd = m.bone("head", bd, (0, 18, -6))
    ball(m, hd, (0, 22.0, -6.0), 6.0, SLUDGE, layers=5)
    m.round_box(hd, 0, -11.4, 5.0, 1.0, 21.0, 27.0, PLATE, cut=1)                           # metal faceplate
    for sx in (-1, 1):
        ball(m, hd, (sx * 2.6, 25.0, -12.4), 1.4, metal(P, "steel", dark="steel_dark"), layers=2)
        m.box(hd, sx * 2.6 - 0.6, 24.4, -13.8, sx * 2.6 + 0.6, 25.6, -13.6, solid(P, "eye", glow=True))
    m.box(hd, -4.0, 16.0, -12.0, 4.0, 20.0, -8.0, solid(P, "mouth"))                       # gaping maw
    for j in range(5):
        spike(m, hd, (-3.2 + j * 1.6, 20.0, -11.6), (0, -1, 0), 0.9, 2.4, solid(P, "bone"), tip=0.8)
        spike(m, hd, (-3.2 + j * 1.6, 16.0, -11.6), (0, 1, 0), 0.9, 1.8, solid(P, "bone"), tip=0.8)
    for j in range(3):                                                                   # yellow gas
        ball(m, hd, (-3.0 - j * 2.6, 18.0 + j, -15.0 - j * 3.0), 1.8 + j * 0.6, solid(P, "gas"), layers=2)
    for sx, nm in ((1, "leg_front_left"), (-1, "leg_front_right")):                      # raking bone claws
        lg = m.bone(nm, top, (sx * 8.0, 8.0, -8.0))
        rod(m, lg, (sx * 8.0, 10.0, -6.0), (sx * 10.0, 3.0, -12.0), 3, SLUDGE, extend=0.6)
        for f in range(4):
            spike(m, lg, (sx * 10.0 + (f - 1.5) * 1.4, 2.0, -12.0), ((f - 1.5) * 0.2, -0.2, -1), 1.0, 7.0,
                  solid(P, "bone"), tip=0.8)
    for sx, nm in ((1, "leg_back_left"), (-1, "leg_back_right")):
        lg = m.bone(nm, top, (sx * 6.0, 4.0, 10.0))
        m.round_box(lg, sx * 6.0, 10.0, 3.0, 3.0, 0.0, 6.0, SLUDGE, cut=1)
    return m
