"""Mimicmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a living treasure chest: a black iron-banded chest for a body, its lid a grinning jaw with one golden
keyhole eye, a gold paper charm pasted across the top, horns and ragged white feathers sprouting from its corners, a
tattered arm in a black glove swinging an iron ball on a chain, and a second arm that is a heavy gun barrel. 15
blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, fabric, metal, riveted, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "floater"
K = 3
LOOK = ("a living black iron-banded treasure chest with a golden keyhole eye, a paper charm, horns and ragged feathers, "
        "an arm swinging an iron ball on a chain and a gun-barrel arm")
BASE = {"black": (50, 48, 56), "black_dark": (16, 16, 20), "iron": (150, 154, 166), "iron_dark": (70, 74, 86),
        "gold": (240, 190, 60), "charm": (240, 200, 90), "red": (180, 30, 30), "white": (240, 240, 236),
        "horn": (220, 214, 200), "mouth": (30, 10, 20), "glove": (40, 40, 46), "skin": (120, 170, 160)}
SHINY = {"black": (130, 60, 40), "black_dark": (70, 26, 14), "gold": (120, 220, 250)}


def P(v):
    return pal(BASE, SHINY, v)


CHEST = riveted(P, "black", "black_dark", spacing=2.4)
IRON = metal(P, "iron", dark="iron_dark")


def build():
    m = Model("mimicmon")
    top = m.bone("mimicmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    m.round_box(bd, 0, 0, 8.0, 6.0, 16.0, 26.0, CHEST, cut=1)                             # chest body
    for j in range(3):                                                                   # iron bands
        m.round_box(bd, -5.0 + j * 5.0, 0, 0.8, 6.3, 15.8, 34.4, IRON, cut=0)
    hd = m.bone("head", bd, (0, 26, 5))
    m.round_box(hd, 0, 0, 8.0, 6.0, 27.0, 34.0, CHEST, cut=1)                             # grinning lid
    m.box(hd, -7.0, 26.0, -6.2, 7.0, 27.0, -5.9, solid(P, "mouth"))
    for j in range(7):
        spike(m, hd, (-6.0 + j * 2.0, 27.0, -6.0), (0, -1, 0), 1.0, 1.6, solid(P, "white"), tip=0.8)
    m.round_box(hd, 2.6, -6.2, 1.8, 0.4, 28.6, 32.6, solid(P, "gold"), cut=0)            # keyhole eye
    m.box(hd, 2.2, 29.4, -6.7, 3.0, 31.6, -6.6, solid(P, "black_dark"))
    m.box(hd, -6.0, 34.0, -3.0, 0.0, 34.4, 3.0, solid(P, "charm"))                       # paper charm
    m.box(hd, -4.6, 34.4, -1.0, -1.4, 34.5, 1.0, solid(P, "red"))
    for sx in (-1, 1):
        spike(m, hd, (sx * 7.0, 34.0, 4.0), (sx * 0.4, 1, 0.3), 1.6, 6.0, solid(P, "horn"), tip=0.8)
    for j in range(5):                                                                   # ragged feathers
        spike(m, hd, (7.0, 30.0 + j, 2.0 + j * 0.6), (1, 0.4 + j * 0.15, 0.4), 1.4, 6.0, solid(P, "white"), tip=0.8)
    al = m.bone("arm_left", bd, (-8.0, 20.0, 0))                                         # arm swinging a chain ball
    rod(m, al, (-8.0, 20.0, 0), (-14.0, 16.0, -2.0), 3, fabric(P, "skin", "black_dark"), extend=0.4)
    ball(m, al, (-16.0, 15.0, -2.6), 2.6, solid(P, "glove"), layers=3)
    for j in range(6):
        y0 = 13.0 - j * 1.6
        m.box(al, -16.8 - j * 0.8, y0 - 1.6, -3.0, -16.0 - j * 0.8, y0, -2.2, IRON)
    ball(m, al, (-22.0, 1.0, -2.6), 4.0, IRON, layers=4)
    ar = m.bone("arm_right", bd, (8.0, 18.0, 0))                                         # gun-barrel arm
    rod(m, ar, (8.0, 18.0, 0), (12.0, 10.0, -1.0), 3, fabric(P, "skin", "black_dark"), extend=0.4)
    m.round_box(ar, 13.0, -2.0, 3.6, 3.6, 0.0, 10.0, IRON, cut=1)
    m.round_box(ar, 13.0, -2.0, 1.8, 1.8, -0.1, 0.2, solid(P, "black_dark"), cut=0)
    return m
