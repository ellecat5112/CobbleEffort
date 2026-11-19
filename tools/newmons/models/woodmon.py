"""Woodmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a walking dead tree: a hunched trunk of split golden-brown wood with a fierce face of knot-hole
eyes glowing blue and a jagged mouth, a crown of broken branches, long root-arms hanging to the ground, and gnarled
root feet. 15 blocks.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import plane, solid
from _route import pal, tone

HEIGHT = 35
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a walking dead tree of split golden-brown wood with knot-hole blue eyes, a jagged mouth, broken branches and long root-arms"
BASE = {"wood": (170, 140, 70), "wood_dark": (100, 76, 30), "eye": (90, 170, 255), "black": (30, 20, 14),
        "tooth": (240, 230, 200)}
SHINY = {"wood": (150, 150, 160), "wood_dark": (80, 80, 90)}


def P(v):
    return pal(BASE, SHINY, v)


def barkf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    a, b = plane(x, y, z, face)
    if (a * 1.2 + math.sin(b * 0.4) * 0.6) % 2.2 < 0.4:
        return tone(p["wood_dark"], face), None
    return tone(p["wood"], face), None


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            d = math.hypot(a - sx * 2.4, b - 25.0)
            if d < 0.7:
                return p["eye"], p["eye"]
            if d < 1.4:
                return p["black"], None
        if 20.0 < b < 22.6 and abs(a) < 3.4:
            if (a * 1.4) % 1.0 < 0.4 and abs(b - 21.3) > 0.5:
                return p["tooth"], None
            return p["black"], None
    return barkf(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("woodmon")
    top = m.bone("woodmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 6.0, 5.0, 6.0, 30.0, facef, cut=2)
    for j in range(7):                                                                  # crown of broken branches
        ang = (j - 3) * 0.4
        spike(m, bd, (math.sin(ang) * 4.0, 30.0, math.cos(ang) * 1.0), (math.sin(ang) * 0.5, 1, 0.1), 1.8,
              5.0 + (j % 3) * 1.6, barkf, tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                # long root-arms
        ab = m.bone(nm, bd, (sx * 6.0, 26.0, 0))
        pts = [(sx * 6.0, 26.0, 0), (sx * 10.0, 18.0, -2.0), (sx * 11.0, 8.0, -3.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 2, barkf, extend=0.5)
        for f in range(4):
            spike(m, ab, pts[-1], ((f - 1.5) * 0.4, -1, -0.3), 1.0, 5.0, barkf, tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.0, 6.0, 0))
        m.round_box(lg, sx * 3.0, 0, 2.4, 2.4, 0.0, 7.0, barkf, cut=1)
        for t in range(3):
            spike(m, lg, (sx * 3.0, 0.8, 0), ((t - 1) * 0.8, -0.1, -1), 1.0, 3.0, barkf, tip=0.8)
    return m
