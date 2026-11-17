"""Būmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official pixel
sprite on wikimon.net): a little piglet. A round pink piglet with a broad flat snout, two small dark eyes, perky ears,
four short legs and a curly tail. Child stage.

Front is -z, y is up. 24 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "quadruped"
K = 4
ANIM = {"leg_amp": 16}
LOOK = "a round pink piglet with a broad flat snout, small dark eyes, perky ears, short legs and a curly tail"
BASE = {"pink": (226, 170, 150), "pink_dark": (170, 110, 96), "pink_light": (250, 214, 200), "nose": (200, 120, 110),
        "nostril": (90, 40, 40), "eye": (30, 20, 20)}
SHINY = {"pink": (190, 170, 120), "pink_dark": (130, 110, 70), "pink_light": (236, 220, 180), "nose": (160, 130, 80)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = skin(P, "pink", dark="pink_dark", light="pink_light", var=0.03)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 3.0, y - 15.6) < 0.8:
                return tone(p["eye"], face), None
    return HIDE(x, y, z, face, variant, box=box, **k)


def snoutf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 1.0, y - 12.6) < 0.5:
                return tone(p["nostril"], face), None
    return tone(p["nose"], face), None


def build():
    m = Model("bumon")
    top = m.bone("bumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    ball(m, bd, (0, 12.0, 0.4), 8.2, bodyf, layers=7)
    m.round_box(bd, 0, -8.4, 2.8, 1.4, 10.8, 14.4, snoutf, cut=1)                    # broad flat snout
    hd = m.bone("head", bd, (0, 19, -2))
    for sx in (-1, 1):                                                              # perky ears
        m.box(hd, sx * 4.0 - 1.6, 18.6, -3.4, sx * 4.0 + 1.6, 22.4, -2.4, HIDE, rotation=(-20, 0, -sx * 20),
              pivot=(sx * 4.0, 18.6, -2.9))
    for fz, nm in ((-3.6, "front"), (3.6, "back")):
        for sx in (-1, 1):
            lg = m.bone(f"leg_{nm}_{'left' if sx > 0 else 'right'}", top, (sx * 4.0, 4.0, fz))
            m.round_box(lg, sx * 4.0, fz, 1.6, 1.6, 0.0, 5.4, HIDE, cut=1)
            m.box(lg, sx * 4.0 - 1.2, 0.0, fz - 1.8, sx * 4.0 + 1.2, 0.8, fz - 1.2, solid(P, "nostril"))
    tl = m.bone("tail", bd, (0, 12, 8))                                             # curly tail
    pts = [(0, 12.0, 8.4)] + [(1.4 * math.cos(t), 12.0 + 1.4 * math.sin(t), 9.4 + t * 0.3)
                              for t in (0.0, 1.6, 3.2, 4.8, 6.4)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, HIDE, extend=0.3)
    return m
