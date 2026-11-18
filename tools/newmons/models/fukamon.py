"""Fukamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
Baby I puff of smoke. A soft golden-yellow cloud blob with a curl on its brow, little blue eyes, a cat-like smile,
orange swirl cheeks, two curled cloud-paws and a wispy curling tail. 0.35 blocks tall.

Front is -z, y is up. 12 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 12
SCALE, HITBOX = sized(0.35, HEIGHT, 1.2)
KIND = "floater"
K = 4
LOOK = "a soft golden-yellow cloud blob with a brow curl, little blue eyes, a cat-like smile, orange swirl cheeks and a wispy tail"
BASE = {"yellow": (252, 220, 80), "yellow_dark": (230, 170, 40), "yellow_light": (255, 245, 190), "eye": (30, 50, 110),
        "shine": (250, 250, 250), "swirl": (240, 140, 40), "mouth": (80, 50, 30)}
SHINY = {"yellow": (200, 220, 255), "yellow_dark": (140, 160, 220), "yellow_light": (240, 246, 255)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "yellow", dark="yellow_dark", light="yellow_light")


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.4, y - 7.4)
            if d < 0.3:
                return tone(p["shine"], face), None
            if d < 0.8:
                return tone(p["eye"], face), None
            c = math.hypot(x - sx * 3.2, y - 6.0)
            if c < 1.2 and (math.atan2(y - 6.0, x - sx * 3.2) + c * 3.0) % 3.0 < 0.9:
                return tone(p["swirl"], face), None
        if abs(y - 6.0 - 0.5 * abs(math.sin(x * 3.0))) < 0.2 and abs(x) < 0.9:
            return tone(p["mouth"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("fukamon")
    top = m.bone("fukamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 6.4, 0), 4.8, bodyf, layers=4, ry=4.2)
    for c, r in (((-3.4, 7.6, 1.0), 2.2), ((3.0, 8.4, 1.4), 2.4), ((0.6, 9.6, 1.6), 2.4)):     # cloud puffs
        ball(m, bd, c, r, SKIN, layers=3)
    hd = m.bone("head", bd, (0, 10, 0))
    for j in range(3):                                                                         # brow curl
        ang = math.radians(j * 100)
        rod(m, hd, (0.6 + math.cos(ang), 11.4 + math.sin(ang), -1.4), (0.6 + math.cos(ang + 1.7),
            11.4 + math.sin(ang + 1.7), -1.4), 1, SKIN, extend=0.2, t2=1)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 1.6, 4.0, -4.0))
        m.round_box(ab, sx * 1.6, -4.4, 1.0, 0.8, 3.4, 5.0, SKIN, cut=0)
    tb = m.bone("tail", bd, (3, 2, 2))
    pts = [(3.0, 2.0, 2.0), (5.0, 0.6, 4.0), (6.6, 1.0, 5.0), (7.0, 2.4, 5.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tb, p0, p1, 1, SKIN, extend=0.3, t2=max(1, 2 - j))
    return m
