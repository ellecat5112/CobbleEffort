"""Danmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the art on wikimon.net, which shows only a
black silhouette with a question mark): a mystery known so far only as a shadow. A small upright dinosaur-like shape
with a big head, short arms, a wide tail and clawed feet, built as the silhouette itself: smoky black with a faint
grey question mark on its chest. Child stage (no level known).

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fbm, mix
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a small dinosaur-like shadow with a big head, short arms and a wide tail, with a faint question mark on its chest"
BASE = {"smoke": (40, 38, 44), "smoke_dark": (12, 12, 16), "mark": (150, 150, 160)}
SHINY = {"smoke": (210, 206, 214), "smoke_dark": (150, 146, 160), "mark": (60, 60, 70)}


def P(v):
    return pal(BASE, SHINY, v)


def shadowf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        r = math.hypot(x, y - 13.0)
        ang = math.atan2(y - 13.0, x)
        if 1.2 < r < 2.0 and ang > -0.8:
            return tone(p["mark"], face), None                       # the question mark's hook
        if abs(x) < 0.4 and 9.6 < y < 11.4 or math.hypot(x, y - 8.6) < 0.4:
            return tone(p["mark"], face), None
    n = fbm(x * 0.3, y * 0.3, z * 0.3, 5)
    return tone(mix(p["smoke_dark"], p["smoke"], n), face), None


def build():
    m = Model("danmon")
    top = m.bone("danmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0.6, 3.6, 3.2, 5.0, 17.0, shadowf, cut=1)
    m.round_box(bd, 0, 0.8, 4.6, 3.6, 4.0, 9.0, shadowf, cut=1)
    hd = m.bone("head", bd, (0, 17, 0))
    m.round_box(hd, 0, -1.0, 5.6, 5.0, 16.0, 26.0, shadowf, cut=2)
    m.box(hd, -2.6, 18.0, -8.0, 2.6, 22.0, -4.0, shadowf)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.4, 14.0, 0))
        rod(m, ab, (sx * 4.4, 14.0, 0), (sx * 9.0, 12.0, -2.0), 3, shadowf, extend=0.4)
        for j in range(3):
            spike(m, ab, (sx * 9.4, 12.0, -2.0), (sx, -0.4 + j * 0.4, -0.3), 1.0, 2.0, shadowf)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.4, 6.0, 0))
        rod(m, lg, (sx * 2.4, 6.4, 0), (sx * 3.0, 1.0, 0), 3, shadowf, extend=0.4)
        for j in range(3):
            spike(m, lg, (sx * 3.0 + (j - 1) * 1.2, 0.6, -1.4), (0, -0.2, -1), 1.0, 2.0, shadowf)
    tl = m.bone("tail", bd, (0, 7, 3))
    rod(m, tl, (0, 7.0, 3.0), (0, 3.0, 9.0), 4, shadowf, extend=0.6)
    return m
