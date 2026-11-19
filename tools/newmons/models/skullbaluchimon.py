"""Skull Baluchimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): an undead giant rhino: a skeleton of pale blue-steel bones on four great columns of
legs, a long skull with red eye-lights and tusks, a ribcage crackling with dark energy, blade-bone spikes along its
spine and bony wing struts, and a long segmented tail. 25 blocks.

Front is -z, y is up. 44 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(25, HEIGHT, 8.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 5}
LOOK = "an undead giant rhino of pale blue-steel bones with a long red-eyed tusked skull, a dark-energy ribcage, spine blades and a segmented tail"
BASE = {"bone": (170, 190, 220), "bone_dark": (80, 96, 130), "dark": (40, 40, 60), "eye": (250, 40, 40),
        "energy": (140, 90, 220, 160)}
SHINY = {"bone": (230, 220, 190), "bone_dark": (150, 140, 110)}


def P(v):
    return pal(BASE, SHINY, v)


BONE = armour(P, "bone", "bone_dark")


def build():
    m = Model("skullbaluchimon")
    top = m.bone("skullbaluchimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    rod(m, bd, (0, 28.0, -12.0), (0, 28.0, 14.0), 2, BONE, extend=0.4)                       # spine
    for j in range(7):                                                                   # ribcage
        z = -10.0 + j * 3.4
        for sx in (-1, 1):
            pts = [(0, 28.0, z), (sx * 6.0, 24.0, z), (sx * 5.0, 17.0, z), (sx * 1.0, 15.0, z)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, bd, p0, p1, 1, BONE, extend=0.2)
        spike(m, bd, (0, 29.0, z), (0, 1, 0.4), 1.4, 5.0, BONE, tip=0.8)                    # spine blades
    ball(m, bd, (0, 22.0, 0), 4.0, solid(P, "energy", glow=True), layers=3)
    for sx in (-1, 1):                                                                   # bony wing struts
        for j in range(3):
            rod(m, bd, (sx * 4.0, 28.0, -4.0 + j * 3.0), (sx * (16.0 - j * 2.0), 38.0 - j * 2.0, 2.0 + j * 4.0), 1,
                BONE, extend=0.2)
    hd = m.bone("head", bd, (0, 26, -14))
    m.round_box(hd, 0, -20.0, 3.6, 7.0, 22.0, 30.0, BONE, cut=1)                              # long skull
    for sx in (-1, 1):
        m.box(hd, min(sx * 3.5, sx * 3.8), 27.0, -20.0, max(sx * 3.5, sx * 3.8), 28.0, -18.4, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.4, 22.0, -26.0), (sx * 0.4, -0.3, -1), 1.2, 6.0, BONE, tip=0.8)   # tusks
    spike(m, hd, (0, 30.0, -24.0), (0, 1, -0.6), 1.6, 6.0, BONE, tip=0.8)
    for sx, nm in ((1, "leg_front_left"), (-1, "leg_front_right"), (1, "leg_back_left"), (-1, "leg_back_right")):
        zz = -8.0 if "front" in nm else 10.0
        lg = m.bone(nm, top, (sx * 5.0, 20.0, zz))
        rod(m, lg, (sx * 5.0, 20.0, zz), (sx * 6.0, 10.0, zz - 1.0), 3, BONE, extend=0.4)
        rod(m, lg, (sx * 6.0, 10.0, zz - 1.0), (sx * 6.0, 1.0, zz), 2, BONE, extend=0.4)
        m.round_box(lg, sx * 6.0, zz - 0.6, 2.4, 2.6, 0.0, 1.6, BONE, cut=0)
    tl = m.bone("tail", bd, (0, 28, 14))
    pts = [(0, 28.0, 14.0), (0, 24.0, 20.0), (0, 18.0, 26.0), (0, 14.0, 30.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, BONE, extend=0.2)
        m.round_box(tl, p1[0], p1[2], 1.4, 1.4, p1[1] - 0.6, p1[1] + 0.6, solid(P, "bone_dark"), cut=0)
    return m
