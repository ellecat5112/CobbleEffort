"""Gumdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
mischievous dragon kid: a violet little dragon with long swept ears, cheeky blue eyes and a fanged grin, a red vest
with a yellow collar, white-gloved paws, and a long striped tail ending in a big steel hammer-head trailing fire.
Child stage, 1 block tall.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import cutout, fabric, flame_inside, local, metal, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.8)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 12}
LOOK = ("a violet little dragon with long swept ears, blue eyes, a fanged grin, a red vest, white paws and a long tail "
        "ending in a steel hammer-head trailing fire")
BASE = {"violet": (150, 130, 210), "violet_dark": (90, 70, 150), "white": (246, 246, 250), "white_dark": (190, 192, 206),
        "red": (210, 40, 40), "red_dark": (130, 14, 18), "yellow": (250, 210, 60), "eye": (60, 180, 220),
        "steel": (200, 204, 220), "steel_dark": (100, 104, 120), "black": (30, 28, 32), "tooth": (250, 250, 240),
        "fire": (255, 150, 40, 215), "fire_core": (255, 240, 170, 240)}
SHINY = {"violet": (240, 170, 80), "violet_dark": (190, 110, 30)}


def P(v):
    return pal(BASE, SHINY, v)


SK = skin(P, "violet", dark="violet_dark")


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if u / max(W, 1e-6) < 0.3 else p["fire"]
    return c, c[:3]


def build():
    m = Model("gumdramon")
    top = m.bone("gumdramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 0.4, 3.2, 2.6, 8.0, 15.0, fabric(P, "red", "red_dark"), cut=1)          # red vest
    m.round_box(bd, 0, 0.4, 3.4, 2.8, 14.4, 15.6, solid(P, "yellow"), cut=1)
    hd = m.bone("head", bd, (0, 16, -1))
    m.round_box(hd, 0, -1.0, 3.8, 3.4, 15.4, 22.6, SK, cut=2)
    m.round_box(hd, 0, -4.4, 2.4, 1.4, 16.0, 18.6, skin(P, "white", dark="white_dark"), cut=1)
    m.box(hd, -1.6, 16.4, -5.9, 1.6, 17.2, -5.7, solid(P, "black"))
    spike(m, hd, (1.0, 17.2, -5.8), (0, -1, 0), 0.6, 1.0, solid(P, "tooth"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.2), 19.6, -4.5, max(sx * 0.8, sx * 2.2), 20.6, -4.3, solid(P, "eye"))
        pts = [(sx * 2.6, 22.0, 0), (sx * 6.0, 25.0, 4.0), (sx * 9.0, 25.0, 8.0)]              # long swept ears
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 1, SK, extend=0.3, t2=3 - j)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.2, 13.6, -1.0))
        rod(m, ab, (sx * 3.2, 13.6, -1.0), (sx * 5.6, 10.0, -3.0), 1, SK, extend=0.3, t2=2)
        m.round_box(ab, sx * 6.0, -3.4, 1.6, 1.6, 8.0, 10.6, skin(P, "white", dark="white_dark"), cut=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.8, 8.0, 0))
        rod(m, lg, (sx * 1.8, 8.0, 0), (sx * 2.2, 1.6, -0.4), 2, SK, extend=0.3)
        m.round_box(lg, sx * 2.2, -1.2, 1.6, 2.4, 0.0, 1.8, SK, cut=1)
    tb = m.bone("tail", bd, (0, 9, 3))                                                          # hammer tail
    pts = [(0, 9.0, 3.0), (3.0, 7.0, 9.0), (8.0, 9.0, 13.0), (12.0, 13.0, 14.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tb, p0, p1, 2 if j < 2 else 1, SK, extend=0.3)
    m.round_box(tb, 13.0, 14.0, 3.0, 2.6, 11.0, 17.0, metal(P, "steel", dark="steel_dark"), cut=1)
    for ang in (0, 90):
        m.box(tb, 16.0, 12.0, 14.0, 24.0, 16.0, 14.0, cutout(flame_inside(4, 0.1, 3), firef), rotation=(ang, 0, 0),
              pivot=(16.0, 14.0, 14.0))
    return m
