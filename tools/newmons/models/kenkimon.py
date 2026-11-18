"""Kenkimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
construction machine: a yellow tracked work vehicle with a cab of hazard-striped panels, a long forklift of two steel
tines in front, a jointed steel arm carrying a great grey grab-bucket head with a visor, black caterpillar tracks and a
trailing power cable. 15 blocks long.

Front is -z, y is up. 30 units tall; Adult stage (Armor).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
LOOK = "a yellow tracked work vehicle with a hazard-striped cab, a long forklift, a jointed arm with a grey grab-bucket head and caterpillar tracks"
BASE = {"yellow": (240, 200, 50), "yellow_dark": (170, 120, 10), "yellow_light": (255, 240, 150), "black": (30, 30, 34),
        "grey": (150, 156, 170), "grey_dark": (70, 76, 90), "steel": (200, 204, 216), "steel_dark": (90, 94, 106),
        "glass": (120, 190, 230), "eye": (240, 60, 40)}
SHINY = {"yellow": (230, 90, 40), "yellow_dark": (150, 40, 10), "yellow_light": (255, 170, 130)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = armour(P, "yellow", "yellow_dark", light="yellow_light", trim="black", trim_w=0.2, rivets=True)


def hazardf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (x + y) % 2.4 < 1.2:
        return tone(p["black"], face), None
    return tone(p["yellow"], face), None


def trackf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["grey_dark"] if (z % 1.6) < 0.5 else p["black"], face), None


def build():
    m = Model("kenkimon")
    top = m.bone("kenkimon", None, (0, 0, 0))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                              # caterpillar tracks
        lg = m.bone(nm, top, (sx * 6.0, 3.0, 0))
        m.round_box(lg, sx * 6.0, 2.0, 2.4, 10.0, 0.0, 6.0, trackf, cut=2)
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 2.0, 6.0, 9.0, 6.0, 12.0, BODY, cut=1)
    m.round_box(bd, 0, 5.0, 4.6, 4.0, 12.0, 20.0, BODY, cut=1)                         # cab
    m.round_box(bd, 0, 0.8, 4.0, 0.3, 14.0, 18.6, solid(P, "glass"), cut=0)
    m.round_box(bd, 0, 9.2, 5.0, 0.4, 7.0, 11.0, hazardf, cut=0)
    for sx in (-1, 1):                                                               # forklift tines
        rod(m, bd, (sx * 2.4, 7.0, -7.0), (sx * 2.4, 14.0, -7.0), 1, metal(P, "steel", dark="steel_dark"), extend=0, t2=1)
        m.box(bd, sx * 2.4 - 0.6, 3.0, -20.0, sx * 2.4 + 0.6, 3.8, -7.0, metal(P, "steel", dark="steel_dark"))
    hd = m.bone("head", bd, (0, 20, 4))                                               # jointed arm + bucket head
    rod(m, hd, (0, 18.0, 6.0), (0, 26.0, 2.0), 2, BODY, extend=0.6)
    rod(m, hd, (0, 26.0, 2.0), (0, 26.0, -6.0), 2, BODY, extend=0.6)
    m.round_box(hd, 0, -9.0, 4.0, 4.0, 22.0, 29.0, metal(P, "grey", dark="grey_dark"), cut=1)
    m.round_box(hd, 0, -13.2, 3.0, 0.3, 25.0, 26.6, solid(P, "eye", glow=True), cut=0)
    for j in range(4):
        spike(m, hd, ((j - 1.5) * 1.8, 22.0, -12.0), (0, -1, -0.3), 1.0, 2.6, metal(P, "steel", dark="steel_dark"), tip=0.8)
    pts = [(0, 10.0, 11.0), (2.0, 4.0, 16.0), (4.0, 1.0, 20.0)]                       # power cable
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, bd, p0, p1, 1, solid(P, "black"), extend=0.3, t2=1)
    return m
