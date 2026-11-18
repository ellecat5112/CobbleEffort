"""Frimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
Baby II frilled lizard-squirrel. A small cream head with big brown eyes, a happy fanged smile, pointed ears and a
great radiating golden-yellow frill round it, ending below in a curling brown tail. Half a block tall.

Front is -z, y is up. 16 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import local, skin, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.5, HEIGHT, 1.2)
KIND = "floater"
K = 4
LOOK = "a small cream head with big brown eyes and a fanged smile, a great golden-yellow frill and a curling brown tail"
BASE = {"cream": (240, 220, 190), "cream_dark": (190, 160, 120), "frill": (250, 200, 40), "frill_light": (255, 240, 150),
        "frill_dark": (220, 120, 20), "brown": (170, 120, 70), "brown_dark": (110, 70, 30), "eye": (110, 60, 30),
        "pupil": (20, 16, 16), "shine": (250, 250, 250), "mouth": (200, 60, 70), "tooth": (250, 250, 250)}
SHINY = {"frill": (250, 120, 200), "frill_light": (255, 210, 240), "frill_dark": (190, 50, 140)}


def P(v):
    return pal(BASE, SHINY, v)


CREAM = skin(P, "cream", dark="cream_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.6, y - 10.4)
            if d < 0.35:
                return tone(p["shine"], face), None
            if d < 0.8:
                return tone(p["pupil"], face), None
            if d < 1.3:
                return tone(p["eye"], face), None
        if abs(x) < 1.2 and 7.6 < y < 8.6 + 0.3 * (1 - abs(x)):
            return tone(p["tooth"] if abs(abs(x) - 0.7) < 0.25 and y > 8.2 else p["mouth"], face), None
    return CREAM(x, y, z, face, variant, box=box, **k)


def frillf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if abs(u - W / 2) < 0.25:
        return tone(p["frill_dark"], face), None
    return tone(p["frill_light"] if v > H * 0.6 else p["frill"], face), None


def build():
    m = Model("frimon")
    top = m.bone("frimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    hd = m.bone("head", bd, (0, 10, 0))
    m.round_box(hd, 0, 0, 3.4, 2.8, 6.0, 13.0, headf, cut=2)
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.6, 12.6, 0), (sx * 0.4, 1, 0.1), 1.4, 2.2, CREAM, tip=0.3)
    for i in range(9):                                                                 # radiating frill
        ang = math.radians(-40 + i * 32.5)
        cx, cy = 5.4 * math.cos(ang), 9.6 + 5.4 * math.sin(ang)
        m.box(hd, cx - 2.2, cy - 3.0, 1.4, cx + 2.2, cy + 3.0, 1.4, frillf,
              rotation=(0, 0, math.degrees(ang) - 90), pivot=(cx, cy, 1.4))
    pts = [(0, 6.0, 0.6), (0, 3.0, 1.0), (1.6, 1.0, 1.0), (3.0, 1.6, 1.0), (3.0, 3.4, 1.0), (1.8, 3.6, 1.0)]
    tb = m.bone("tail", bd, (0, 6, 0.6))
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):                                   # curling tail
        rod(m, tb, p0, p1, 1, skin(P, "brown", dark="brown_dark"), extend=0.3, t2=1)
    return m
