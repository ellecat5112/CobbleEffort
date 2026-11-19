"""Valvemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a riveted brass machine: a chunky octagonal brass body engraved with square spirals, a little
chimney head with a grumpy red face, two long jointed pipe arms ending in heavy stepped brass blocks, puffs of steam,
two piston legs on round steel feet, and a brass base plate. 25 blocks.

Front is -z, y is up. Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, plane, riveted, solid
from _route import pal, tone

HEIGHT = 45
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a riveted brass machine with an octagonal body engraved with spirals, a chimney head and long pipe arms ending in stepped brass blocks"
BASE = {"brass": (220, 180, 90), "brass_dark": (140, 100, 40), "steel": (190, 194, 206), "steel_dark": (90, 94, 106),
        "red": (200, 50, 40), "pipe": (150, 110, 90), "pipe_dark": (80, 54, 40), "steam": (230, 230, 236, 170),
        "eye": (250, 230, 120), "black": (40, 30, 30)}
SHINY = {"brass": (180, 190, 200), "brass_dark": (100, 110, 130)}


def P(v):
    return pal(BASE, SHINY, v)


def brassf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    a, b = plane(x, y, z, face)
    u, v = a % 4.0, b % 4.0
    if min(u, v, 4.0 - u, 4.0 - v) < 0.3 or (abs(u - 2.0) < 1.2 and abs(v - 2.0) < 1.2 and
                                          min(abs(u - 2.0), abs(v - 2.0)) > 0.8):
        return tone(p["brass_dark"], face), None
    return metal(P, "brass", dark="brass_dark")(x, y, z, face, variant, box=box, **k)


def stepped(m, bone, c, s):
    x, y, z = c
    for j in range(4):
        w = s * (1.0 - j * 0.22)
        m.box(bone, x - w, y + j * s * 0.4, z - w, x + w, y + (j + 1) * s * 0.4, z + w, brassf)


def build():
    m = Model("valvemon")
    top = m.bone("valvemon", None, (0, 0, 0))
    m.box(top, -9.0, 0.0, -6.0, 9.0, 1.6, 6.0, riveted(P, "brass", "brass_dark"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 5.0, 14.0, 0))
        m.round_box(lg, sx * 5.0, 0, 3.4, 3.4, 1.6, 8.0, metal(P, "steel", dark="steel_dark"), cut=1)
        rod(m, lg, (sx * 5.0, 8.0, 0), (sx * 5.0, 16.0, 0), 2, metal(P, "pipe", dark="pipe_dark"), extend=0.4)
    bd = m.bone("body", top, (0, 16, 0))
    m.round_box(bd, 0, 0, 9.0, 7.0, 16.0, 32.0, brassf, cut=3)
    hd = m.bone("head", bd, (0, 32, 0))
    m.round_box(hd, 0, 0, 3.0, 3.0, 32.0, 38.0, brassf, cut=1)
    m.box(hd, -2.0, 33.4, -3.2, 2.0, 36.4, -2.9, solid(P, "red"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.4, sx * 1.6), 35.0, -3.4, max(sx * 0.4, sx * 1.6), 35.8, -3.1, solid(P, "eye", glow=True))
    m.box(hd, -1.0, 33.8, -3.4, 1.0, 34.3, -3.1, solid(P, "black"))
    for j in range(3):
        ball(m, hd, (3.0 + j * 1.6, 39.0 + j * 2.0, 0), 1.4 + j * 0.4, solid(P, "steam"), layers=1)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 8.0, 28.0, 0))
        pts = [(sx * 8.0, 28.0, 0), (sx * 11.0, 34.0, -1.0), (sx * 12.0, 40.0, -2.0)] if sx > 0 else \
              [(sx * 8.0, 28.0, 0), (sx * 13.0, 32.0, -1.0), (sx * 15.0, 38.0, -2.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 2, metal(P, "pipe", dark="pipe_dark"), extend=0.4)
        stepped(m, ab, (pts[-1][0], pts[-1][1], pts[-1][2]), 3.6)
    return m
