"""Bacchusmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Olympus god of wine and revelry. A round glossy magenta body that is mostly a huge toothy
grin, a little violet crown with a red jewel, a violet cape, long magenta arms ending in green clawed gauntlets bound
with leather straps, and a cream-banded tail coiled beneath it. 35 blocks tall.

Front is -z, y is up. 56 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape
from _digidetail import armour, fabric, gem, leather, plane, skin, solid
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(35, HEIGHT, 2.8)
KIND = "floater"
K = 3
LOOK = ("the god of wine: a round glossy magenta body with a huge toothy grin, a little violet crown, a violet cape, "
        "long arms with green clawed gauntlets and a cream-banded coiled tail")
BASE = {"pink": (220, 40, 140), "pink_dark": (130, 14, 80), "pink_light": (255, 150, 210), "violet": (110, 60, 180),
        "violet_dark": (60, 30, 110), "green": (110, 200, 120), "green_dark": (40, 120, 60), "cream": (240, 220, 160),
        "cream_dark": (190, 160, 100), "strap": (110, 70, 40), "mouth": (90, 10, 40), "tooth": (250, 250, 246),
        "red": (220, 40, 40), "red_light": (255, 160, 160)}
SHINY = {"pink": (240, 150, 40), "pink_dark": (170, 90, 10), "pink_light": (255, 220, 140), "violet": (40, 120, 90),
         "violet_dark": (16, 70, 50)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = skin(P, "pink", dark="pink_dark", light="pink_light", var=0.03)
GREEN = armour(P, "green", "green_dark")


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        if abs(a) < 9.0 and 24.0 < b < 29.0:
            jag = abs(((a * 0.6) % 2) - 1) * 1.6
            if b < 24.0 + jag or b > 29.0 - jag:
                return p["tooth"], None
            return p["mouth"], None
    return BODY(x, y, z, face, variant, box=box, **k)


def bandf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = (box.lo[2] + box.size[2] - z) if box else 0
    return tone(p["cream_dark"] if (t % 1.6) < 0.35 else p["cream"], face), None


def build():
    m = Model("bacchusmon")
    top = m.bone("bacchusmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 28, 0))
    ball(m, bd, (0, 30.0, 0), 13.0, bodyf, layers=8, squash=0.85, ry=12.0)
    hd = m.bone("head", bd, (0, 42, -2))
    m.round_box(hd, 0, -2.0, 3.0, 2.6, 41.0, 44.0, armour(P, "violet", "violet_dark"), cut=1)   # little crown
    for i in range(5):
        spike(m, hd, (-2.4 + i * 1.2, 44.0, -2.0), (0, 1, 0), 1.0, 2.0 + (i % 2), armour(P, "violet", "violet_dark"))
    m.box(hd, -0.8, 42.0, -4.8, 0.8, 43.6, -4.4, gem(P, "red", "red_light"))
    cb = m.bone("cap", bd, (0, 40, 6))
    cape(m, cb, 41.0, 26.0, 24.0, fabric(P, "violet", "violet_dark"), z=8.0, flare=1.0, panels=10, sweep=(0, 10))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):          # long arms with green gauntlets
        ab = m.bone(nm, bd, (sx * 11.0, 34.0, 0))
        el = (sx * 20.0, 30.0, -2.0)
        wr = (sx * 22.0, 18.0, -3.0)
        rod(m, ab, (sx * 11.0, 34.0, 0), el, 4, BODY, extend=0.6)
        rod(m, ab, el, wr, 5, GREEN, extend=0.6)
        for j in range(3):
            p = tuple(e + (w - e) * (0.2 + j * 0.3) for e, w in zip(el, wr))
            rod(m, ab, p, (p[0], p[1] - 1.0, p[2]), 6, leather(P, "strap", "pink_dark"), extend=0)
        for f in range(3):
            spike(m, ab, wr, (sx * 0.3 + (f - 1) * 0.4, -1, -0.3), 1.6, 5.0, GREEN, tip=0.6)
    tl = m.bone("tail", bd, (0, 18, 2))
    p = (0.0, 18.0, 2.0)
    for j in range(14):                                          # the coiled tail
        ang = j * 0.55
        r = 6.0 - j * 0.25
        q = (r * math.sin(ang), 14.0 - j * 0.7, -r * math.cos(ang) + 2.0)
        rod(m, tl, p, q, max(1, round(4 - j * 0.2)), bandf, extend=0.5)
        p = q
    return m
