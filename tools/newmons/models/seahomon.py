"""Seahomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Armor Digimon of purity: a seahorse-bird of violet feather-fins, a silver helmet with a long
trumpet-bell snout and a crown of spiky violet crest feathers, a golden tendril moustache, red bands on its chest and a
curling segmented silver tail. 15 blocks.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import feathers, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "a seahorse-bird of violet feather-fins with a silver trumpet-bell snout helm, a spiky violet crest and a curling silver tail"
BASE = {"violet": (120, 110, 200), "violet_dark": (60, 50, 140), "silver": (220, 224, 236), "silver_dark": (130, 134, 150),
        "gold": (230, 190, 80), "red": (200, 40, 50), "eye": (200, 40, 40)}
SHINY = {"violet": (70, 170, 170), "violet_dark": (24, 100, 100)}


def P(v):
    return pal(BASE, SHINY, v)


FEATH = feathers(P, "violet", "violet_dark")
SILVER = metal(P, "silver", dark="silver_dark")


def build():
    m = Model("seahomon")
    top = m.bone("seahomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    ball(m, bd, (0, 20.0, 0.6), 5.0, FEATH, layers=5, ry=7.0)
    for j in range(3):
        m.round_box(bd, 0, -3.6, 1.0, 0.4, 16.0 + j * 2.0, 17.0 + j * 2.0, solid(P, "red"), cut=0)
    for sx in (-1, 1):                                                                   # feather-fin wings
        for j in range(5):
            ang = math.radians(-60 + j * 18)
            spike(m, bd, (sx * 4.0, 18.0, 1.0), (sx * math.cos(ang), math.sin(ang), 0.4), 1.8, 10.0 - abs(j - 2), FEATH,
                  tip=0.8)
    hd = m.bone("head", bd, (0, 27, -1))
    m.round_box(hd, 0, -1.0, 2.8, 3.0, 26.0, 31.0, SILVER, cut=1)
    rod(m, hd, (0, 28.0, -3.6), (0, 28.0, -12.0), 1, SILVER, extend=0.2, t2=2)              # trumpet snout
    m.round_box(hd, 0, -12.6, 1.8, 0.8, 26.2, 29.8, SILVER, cut=0)
    m.box(hd, -0.8, 27.2, -13.5, 0.8, 28.8, -13.3, solid(P, "silver_dark"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.7, sx * 2.9), 29.0, -2.6, max(sx * 2.7, sx * 2.9), 29.8, -1.4, solid(P, "eye"))
        pts = [(sx * 1.0, 27.0, -4.0), (sx * 4.0, 25.0, -4.0), (sx * 6.0, 27.0, -2.0)]
        for p0, p1 in zip(pts, pts[1:]):                                                  # golden tendrils
            rod(m, hd, p0, p1, 1, solid(P, "gold"), extend=0.1, t2=1)
    for j in range(7):                                                                   # spiky crest
        spike(m, hd, ((j - 3) * 0.8, 31.0, 0.4), ((j - 3) * 0.25, 1, 0.3), 1.2, 6.0 + (3 - abs(j - 3)), FEATH, tip=0.8)
    tl = m.bone("tail", bd, (0, 14, 1))                                                  # curling silver tail
    pts = [(0, 14.0, 1.0), (0, 9.0, 2.0), (1.0, 5.0, 1.0), (3.0, 3.0, -1.0), (4.0, 5.0, -3.0), (2.0, 6.0, -3.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, max(1, 3 - i // 2), SILVER, extend=0.4)
    return m
