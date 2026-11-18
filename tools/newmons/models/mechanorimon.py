"""Mechanorimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the walking machine: a hunched grey mecha with a blue glass dome cockpit on top, a slotted visor with red eyes, a big
red chest lamp, a backpack of twin exhausts, very long mechanical arms with clawed fingers reaching to the ground and
long jointed legs with talon feet. 15 blocks tall.

Front is -z, y is up. 50 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, gem, metal, riveted, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a hunched grey mecha with a blue dome cockpit, a red chest lamp, twin exhausts, long clawed arms and jointed talon legs"
BASE = {"grey": (170, 174, 186), "grey_dark": (70, 74, 86), "grey_light": (220, 224, 234), "blue": (60, 110, 220),
        "blue_light": (190, 220, 255), "red": (220, 40, 40), "red_light": (255, 170, 160), "black": (30, 30, 34)}
SHINY = {"grey": (210, 180, 90), "grey_dark": (130, 100, 30), "grey_light": (250, 230, 160)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = riveted(P, "grey", "grey_dark", light="grey_light")
MET = metal(P, "grey", dark="grey_dark", light="grey_light")


def build():
    m = Model("mechanorimon")
    top = m.bone("mechanorimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 22, 0))
    m.round_box(bd, 0, 1.0, 7.0, 6.0, 22.0, 38.0, ARM, cut=2)
    m.round_box(bd, 0, -5.2, 2.0, 0.8, 26.0, 30.0, gem(P, "red", "red_light"), cut=1)
    m.round_box(bd, 0, -5.2, 5.0, 0.4, 32.0, 34.0, solid(P, "black"), cut=0)
    m.box(bd, -2.4, 32.6, -5.7, -1.0, 33.4, -5.6, solid(P, "red", glow=True))
    m.box(bd, 1.0, 32.6, -5.7, 2.4, 33.4, -5.6, solid(P, "red", glow=True))
    hd = m.bone("head", bd, (0, 38, 0))
    m.round_box(hd, 0, 0, 4.0, 4.0, 38.0, 43.0, gem(P, "blue", "blue_light", glow=False), cut=2)   # dome cockpit
    for sx in (-1, 1):                                                               # twin exhausts
        rod(m, bd, (sx * 3.0, 36.0, 6.0), (sx * 3.4, 46.0, 7.0), 1, MET, extend=0, t2=1)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # very long clawed arms
        ab = m.bone(nm, bd, (sx * 7.0, 34.0, 0))
        pts = [(sx * 7.0, 34.0, 0), (sx * 14.0, 26.0, -4.0), (sx * 18.0, 12.0, -6.0), (sx * 20.0, 2.0, -8.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 2, ARM, extend=0.6)
        for j in range(4):
            spike(m, ab, pts[-1], (sx * 0.3 + (j - 1.5) * 0.4, -0.6, -1), 1.0, 5.0, MET, tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 22.0, 0))
        pts = [(sx * 4.0, 22.0, 0), (sx * 7.0, 12.0, -4.0), (sx * 7.0, 2.0, 2.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, lg, p0, p1, 2, ARM, extend=0.6)
        for j in range(3):
            spike(m, lg, (sx * 7.0 + (j - 1) * 1.4, 1.0, 1.0), ((j - 1) * 0.4, -0.2, -1), 1.2, 5.0, MET, tip=0.8)
    return m
