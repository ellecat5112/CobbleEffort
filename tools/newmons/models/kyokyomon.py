"""Kyokyomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a Baby
II yellow serpent-headed Digimon: a big rounded dragon head with a green eye, a red-edged spiky crest of yellow fins
tipped violet, and a short curling yellow snake tail. Half a block tall.

Front is -z, y is up. 18 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.5, HEIGHT, 1.2)
KIND = "floater"
K = 4
LOOK = "a yellow serpent-headed baby with a green eye, a crest of violet-tipped yellow fins and a short curling tail"
BASE = {"yellow": (250, 210, 60), "yellow_dark": (200, 150, 20), "grey": (130, 120, 110), "violet": (180, 80, 160),
        "red": (220, 60, 50), "eye": (60, 180, 80), "pupil": (16, 16, 20), "white": (250, 250, 250)}
SHINY = {"yellow": (120, 200, 240), "yellow_dark": (40, 130, 200)}


def P(v):
    return pal(BASE, SHINY, v)


SK = skin(P, "yellow", dark="yellow_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west", "north"):
        for sx in (-1, 1):
            if face == "north" and math.hypot(x - sx * 2.0, y - 11.0) < 0.9:
                return tone(p["eye"], face), None
    return SK(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("kyokyomon")
    top = m.bone("kyokyomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    hd = m.bone("head", bd, (0, 10, 0))
    m.round_box(hd, 0, -1.0, 3.6, 4.4, 7.0, 13.6, headf, cut=2)
    m.round_box(hd, 0, -5.4, 2.4, 1.6, 7.4, 10.4, SK, cut=1)                           # snout
    for j, (dy, dz, ln) in enumerate(((1.0, 1.0, 5.0), (0.0, 3.0, 6.0), (-1.4, 4.0, 4.0))):   # fin crest
        for sx in (-1, 1):
            spike(m, hd, (sx * 1.6, 12.6 + dy, -1.0 + dz), (sx * 0.8, 0.6, 0.8), 1.4, ln, SK, tip=0.8)
            spike(m, hd, (sx * (1.6 + ln * 0.5), 12.6 + dy + ln * 0.35, -1.0 + dz + ln * 0.5), (sx * 0.8, 0.6, 0.8), 0.8,
                  1.4, solid(P, "violet"), tip=0.8)
    tb = m.bone("tail", bd, (0, 6, 2))
    pts = [(0, 7.0, 1.0), (0, 3.0, 2.0), (2.0, 1.0, 5.0), (4.0, 3.0, 6.0), (5.0, 6.0, 5.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tb, p0, p1, max(1, 2 - j // 2), SK if j > 0 else solid(P, "grey"), extend=0.4)
    return m
