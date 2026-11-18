"""Rurimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little blue reptile scholar: a blue hide with a pale belly, a toothy grin, a pink horn-tuft, mint
spines down its back and tail, mint claws, an orange satchel with a star badge slung on a strap, an open book in one
claw and a flame dancing on the other fingertip. 1 block. Child stage (no level on wikimon; by analogy).

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import leather, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a little blue reptile scholar with a toothy grin, mint spines and claws, an orange star satchel, an open book and a fingertip flame"
BASE = {"blue": (60, 90, 200), "blue_dark": (24, 40, 130), "belly": (200, 210, 240), "mint": (130, 230, 170),
        "pink": (240, 120, 170), "orange": (240, 150, 40), "orange_dark": (180, 90, 10), "star": (60, 90, 200),
        "book": (150, 90, 60), "page": (250, 246, 230), "flame": (250, 160, 50), "eye": (60, 60, 70),
        "white": (255, 255, 255), "mouth": (170, 40, 50), "tooth": (250, 250, 240)}
SHINY = {"blue": (230, 120, 60), "blue_dark": (160, 60, 20)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = skin(P, "blue", dark="blue_dark")


def build():
    m = Model("rurimon")
    top = m.bone("rurimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7, 0))
    ball(m, bd, (0, 12.0, 0.4), 4.4, HIDE, layers=4, ry=5.0)
    m.round_box(bd, 0, -3.2, 2.6, 1.4, 8.0, 15.0, solid(P, "belly"), cut=1)
    hd = m.bone("head", bd, (0, 17, 0))
    m.round_box(hd, 0, -1.6, 3.4, 3.6, 16.6, 22.6, HIDE, cut=1)
    m.round_box(hd, 0, -5.4, 2.6, 1.8, 16.6, 19.6, HIDE, cut=1)
    m.box(hd, -2.4, 17.0, -7.3, 2.4, 18.0, -4.0, solid(P, "mouth"))
    for j in range(4):
        for sx in (-1, 1):
            spike(m, hd, (sx * 2.2, 18.0, -6.8 + j * 1.0), (0, -1, 0), 0.8, 1.0, solid(P, "tooth"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.4, sx * 2.6), 20.4, -5.3, max(sx * 1.4, sx * 2.6), 21.6, -5.0, solid(P, "white"))
        m.box(hd, min(sx * 1.8, sx * 2.4), 20.6, -5.4, max(sx * 1.8, sx * 2.4), 21.4, -5.2, solid(P, "eye"))
    spike(m, hd, (0, 22.6, -1.0), (0, 1, 0.2), 1.6, 3.0, solid(P, "pink"), tip=0.8)
    for j in range(5):                                                                   # mint spines
        spike(m, bd, (0, 18.0 - j * 2.0, 3.6 + j * 0.6), (0, 0.4, 1), 1.0, 2.4, solid(P, "mint"), tip=0.8)
    m.box(bd, -4.0, 14.0, -4.6, 4.0, 15.0, -4.2, leather(P, "orange_dark", "orange_dark"), rotation=(0, 0, -35),
          pivot=(0, 14.5, -4.4))                                                          # strap
    m.round_box(bd, 4.6, 0, 1.6, 2.6, 7.0, 11.0, leather(P, "orange", "orange_dark"), cut=1)   # satchel
    m.box(bd, 6.0, 8.4, -0.8, 6.4, 9.6, 0.4, solid(P, "star"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.0, 15.0, -1.0))
        rod(m, ab, (sx * 4.0, 15.0, -1.0), (sx * 6.0, 12.0, -4.0), 1, HIDE, extend=0.2, t2=2)
        for f in range(3):
            spike(m, ab, (sx * 6.0, 12.0, -4.0), ((f - 1) * 0.3, -0.6, -1), 0.8, 1.6, solid(P, "mint"), tip=0.8)
    m.box("arm_right", -9.0, 10.0, -6.0, -5.0, 13.0, -5.4, solid(P, "page"), rotation=(30, 0, 0), pivot=(-7.0, 11.5, -5.7))
    m.box("arm_right", -9.2, 10.0, -5.4, -4.8, 13.0, -5.0, solid(P, "book"), rotation=(30, 0, 0), pivot=(-7.0, 11.5, -5.2))
    spike(m, "arm_left", (6.0, 13.6, -5.0), (0, 1, 0), 1.6, 3.0, solid(P, "flame", glow=True), tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.2, 7.0, 0))
        m.round_box(lg, sx * 2.2, 0, 1.8, 1.8, 2.0, 8.0, HIDE, cut=0)
        m.round_box(lg, sx * 2.2, -1.0, 2.0, 2.8, 0.0, 2.4, HIDE, cut=0)
        for f in range(3):
            spike(m, lg, (sx * 2.2 + (f - 1) * 1.2, 0.8, -3.6), (0, -0.2, -1), 0.8, 1.6, solid(P, "mint"), tip=0.8)
    tl = m.bone("tail", bd, (0, 9, 4))
    pts = [(0, 9.0, 4.0), (0, 5.0, 9.0), (0, 4.0, 13.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 2, HIDE, extend=0.3)
    spike(m, tl, pts[-1], (0, 0.2, 1), 1.2, 2.4, solid(P, "mint"), tip=0.8)
    return m
