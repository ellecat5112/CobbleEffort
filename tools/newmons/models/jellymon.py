"""Jellymon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
jellyfish girl: a small girl-shaped Digimon with a round translucent blue jellyfish cap patterned with a pink-and-white
target mark, long flowing pale-blue tentacle hair, big dark eyes, a pink-and-black striped bodysuit, pink boots and
lime-green tentacle ribbons that crackle with yellow sparks. Child stage, 1 block tall.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, skin, solid, strands
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = ("a small jellyfish girl with a translucent blue cap and target mark, long pale-blue tentacle hair, a pink-and-"
        "black striped bodysuit and lime-green sparking tentacles")
BASE = {"cap": (110, 170, 250, 200), "cap_light": (210, 236, 255, 220), "pink": (240, 80, 170), "pink_dark": (160, 30, 110),
        "black": (40, 30, 50), "white": (250, 250, 250), "hair": (200, 220, 250), "hair_dark": (120, 150, 210),
        "skin": (250, 226, 212), "skin_dark": (210, 170, 150), "eye": (30, 30, 60), "lime": (180, 240, 80),
        "lime_dark": (90, 160, 30), "spark": (250, 240, 80)}
SHINY = {"cap": (250, 170, 110, 200), "pink": (80, 200, 170), "pink_dark": (20, 120, 100), "hair": (250, 230, 200)}


def P(v):
    return pal(BASE, SHINY, v)


def capf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        r = math.hypot(x, y - 26.0)
        if r < 0.8 or 1.6 < r < 2.4:
            return p["pink"], None
        if r < 1.6:
            return p["white"], None
    return (p["cap_light"] if y > 28.0 else p["cap"]), None


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 1.2, y - 20.6) < 0.7:
                return tone(p["eye"], face), None
    return skin(P, "skin", dark="skin_dark")(x, y, z, face, variant, box=box, **k)


def suitf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["pink"] if (y % 1.6) < 0.8 else p["black"], face), None


def build():
    m = Model("jellymon")
    top = m.bone("jellymon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 9, 0))
    m.round_box(bd, 0, 0, 2.2, 1.6, 9.0, 17.6, suitf, cut=1)
    hd = m.bone("head", bd, (0, 18, 0))
    m.round_box(hd, 0, 0, 2.4, 2.4, 17.6, 22.6, facef, cut=1)
    ball(m, hd, (0, 24.6, 0.4), 4.6, capf, layers=4, squash=0.8)
    for i in range(9):                                                               # tentacle hair
        ang = math.radians(-110 + i * 27)
        pts = [(3.4 * math.sin(ang), 23.0, 0.4 + 3.0 * math.cos(ang)), (4.4 * math.sin(ang), 14.0, 2.0 + 2.6 * math.cos(ang)),
               (5.0 * math.sin(ang), 6.0, 4.0 + 2.0 * math.cos(ang))]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, strands(P, "hair", "hair_dark"), extend=0.2, t2=1)
    for sx in (-1, 1):                                                               # sparking tentacles
        pts = [(sx * 2.4, 22.0, 0), (sx * 7.0, 20.0, -2.0), (sx * 9.0, 15.0, -1.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, strands(P, "lime", "lime_dark"), extend=0.2, t2=2)
        m.round_box(hd, sx * 9.0, -1.0, 0.8, 0.8, 14.0, 15.4, solid(P, "spark", glow=True), cut=0)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 2.2, 16.6, 0))
        rod(m, ab, (sx * 2.2, 16.6, 0), (sx * 4.0, 12.4, -0.6), 1, suitf, extend=0.3, t2=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.2, 9.0, 0))
        rod(m, lg, (sx * 1.2, 9.4, 0), (sx * 1.4, 3.0, 0), 1, suitf, extend=0.3, t2=1)
        m.round_box(lg, sx * 1.4, -0.4, 1.0, 1.6, 0.0, 3.4, fabric(P, "pink", "pink_dark"), cut=0)
    return m
