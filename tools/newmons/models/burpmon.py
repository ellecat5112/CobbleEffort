"""Burpmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the gluttonous pig. An enormous round pink pig-blob sitting on stubby legs, tiny dot eyes, a
wobbly crumb-flecked grin with its tongue poking out, pointed pink ears, a curly tail and a meat-on-the-bone in each
little hand, with gnawed bones scattered at its feet. 15 blocks tall.

Front is -z, y is up. 34 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("an enormous round pink pig-blob with tiny dot eyes, a wobbly crumb-flecked grin, pointed ears, a curly tail "
        "and a meat-on-the-bone in each little hand")
BASE = {"pink": (236, 100, 150), "pink_dark": (180, 50, 100), "pink_light": (255, 180, 210), "eye": (250, 250, 250),
        "pupil": (20, 16, 20), "mouth": (40, 20, 30), "tongue": (240, 90, 110), "crumb": (160, 100, 60),
        "meat": (150, 60, 40), "meat_light": (200, 110, 80), "bone": (246, 240, 226)}
SHINY = {"pink": (240, 200, 120), "pink_dark": (190, 140, 60), "pink_light": (255, 236, 190)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = skin(P, "pink", dark="pink_dark", light="pink_light", var=0.03)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 3.4, y - 26.0)
            if d < 1.1:
                return tone(p["pupil"] if d > 0.7 else p["eye"], face), None
        wob = 21.0 + 0.6 * math.sin(x * 1.4)
        if abs(y - wob) < 0.25 and abs(x) < 4.4:
            return tone(p["mouth"], face), None
        if 1.0 < x < 2.4 and wob - 1.6 < y < wob:
            return tone(p["tongue"], face), None
        if ((x * 3.1 + y * 1.7) % 4.0 < 0.3) and 17 < y < 22 and abs(x) < 6:
            return tone(p["crumb"], face), None
    return HIDE(x, y, z, face, variant, box=box, **k)


def meat(m, bone, c, d):
    ball(m, bone, c, 2.4, solid(P, "meat"), layers=3)
    end = tuple(a + b * 4.0 for a, b in zip(c, d))
    rod(m, bone, c, end, 1, solid(P, "bone"), extend=0.3)
    m.box(bone, end[0] - 0.8, end[1] - 0.8, end[2] - 0.8, end[0] + 0.8, end[1] + 0.8, end[2] + 0.8, solid(P, "bone"))


def build():
    m = Model("burpmon")
    top = m.bone("burpmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 18.0, 0), 15.0, bodyf, layers=9, squash=0.86)
    hd = m.bone("head", bd, (0, 30, 0))
    for sx in (-1, 1):                                                         # pointed ears
        spike(m, hd, (sx * 7.0, 30.0, -1.0), (sx * 0.7, 1, -0.2), 4.0, 4.0, HIDE, tip=1.0)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                        # little hands with meat
        ab = m.bone(nm, bd, (sx * 13.0, 20.0, -4.0))
        m.round_box(ab, sx * 14.0, -6.0, 2.0, 2.0, 18.0, 22.0, HIDE, cut=1)
        meat(m, ab, (sx * 15.0, 23.4, -7.0), (sx * 0.3, 1, 0))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                        # stubby legs
        lg = m.bone(nm, top, (sx * 8.0, 4.0, -2.0))
        m.round_box(lg, sx * 8.0, -3.0, 3.6, 3.6, 0.0, 6.0, HIDE, cut=1)
    tl = m.bone("tail", bd, (0, 12, 13))
    pts = [(0, 12.0, 12.6)] + [(1.6 * math.cos(t), 12.0 + 1.6 * math.sin(t), 14.0 + t * 0.4)
                               for t in (0.0, 1.6, 3.2, 4.8)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, HIDE, extend=0.3)
    return m
