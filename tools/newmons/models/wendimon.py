"""Wendimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a hulking hunched beast-man: a shaggy dark brown body, a red hood with two curved grey horns, a
grinning red mask-face with white fangs and a gold horn, floppy green ears, enormously long red arms ending in great
grey-clawed hands, a white bandage tied round one wrist, and short heavy legs with clawed red feet. 15 blocks.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, fur, plane, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a hulking hunched brown beast with a red hood and grey horns, a grinning red mask-face, green ears and enormous long red arms"
BASE = {"brown": (100, 70, 56), "brown_dark": (50, 30, 24), "red": (190, 30, 40), "red_dark": (110, 10, 16),
        "grey": (150, 150, 160), "grey_dark": (80, 80, 90), "green": (130, 180, 70), "white": (248, 248, 248),
        "gold": (240, 200, 70), "eye": (250, 220, 60), "mouth": (90, 10, 20)}
SHINY = {"brown": (70, 80, 110), "brown_dark": (30, 36, 60), "red": (60, 130, 170), "red_dark": (20, 70, 110)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "brown", "brown_dark", length=1.8)
RED = skin(P, "red", dark="red_dark")


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        if 29.0 < b < 31.4 and abs(a) < 2.6:
            if (a * 1.6) % 1.0 < 0.5 and abs(b - 30.2) > 0.4:
                return p["white"], None
            return p["mouth"], None
        for sx in (-1, 1):
            if math.hypot(a - sx * 1.4, b - 33.0) < 0.6:
                return p["eye"], p["eye"]
    return RED(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("wendimon")
    top = m.bone("wendimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    ball(m, bd, (0, 22.0, 2.0), 8.6, FUR, layers=5, ry=9.0)                                # hunched body
    hd = m.bone("head", bd, (0, 30, -6))
    m.round_box(hd, 0, -6.6, 3.4, 2.2, 28.0, 35.0, facef, cut=1)
    m.round_box(hd, 0, -4.4, 5.0, 4.0, 32.0, 38.0, fabric(P, "red", "red_dark"), cut=2)      # red hood
    spike(m, hd, (0, 35.0, -8.8), (0, 1, -0.4), 1.0, 2.0, solid(P, "gold"), tip=0.8)
    for sx in (-1, 1):
        pts = [(sx * 4.0, 36.0, -3.0), (sx * 8.0, 39.0, -2.0), (sx * 9.0, 43.0, -3.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 2, skin(P, "grey", dark="grey_dark"), extend=0.4)
        m.box(hd, min(sx * 3.4, sx * 6.4), 29.0, -6.0, max(sx * 3.4, sx * 6.4), 32.0, -5.0, solid(P, "green"),
              rotation=(0, 0, -sx * 25), pivot=(sx * 3.4, 31.0, -5.5))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                # enormous long arms
        ab = m.bone(nm, bd, (sx * 7.0, 26.0, -2.0))
        pts = [(sx * 7.0, 26.0, -2.0), (sx * 12.0, 18.0, -6.0), (sx * 13.0, 8.0, -9.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 3, RED, extend=0.6)
        h = (sx * 13.4, 5.0, -10.0)
        ball(m, ab, h, 3.2, RED, layers=3)
        for f in range(4):
            spike(m, ab, (h[0] + (f - 1.5) * 1.6, h[1] - 2.4, h[2] - 1.6), (0, -0.6, -1), 1.0, 4.0,
                  skin(P, "grey", dark="grey_dark"), tip=0.8)
        if sx < 0:
            m.round_box(ab, sx * 13.0, -9.0, 2.6, 2.6, 8.0, 10.0, fabric(P, "white", "grey"), cut=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 12.0, 2.0))
        rod(m, lg, (sx * 4.0, 14.0, 2.0), (sx * 5.0, 3.0, 0.0), 3, FUR, extend=0.6)
        m.round_box(lg, sx * 5.0, -1.4, 2.8, 3.4, 0.0, 3.0, RED, cut=1)
        for t in range(3):
            spike(m, lg, (sx * 5.0 + (t - 1) * 1.6, 1.0, -4.6), (0, -0.2, -1), 1.0, 2.4, skin(P, "grey", dark="grey_dark"),
                  tip=0.8)
    return m
