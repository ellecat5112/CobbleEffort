"""Sunken Valor (Ghost/Psychic), the ancient paradox Azelf, built from boxes after @Alex_LR04's art (the art's own
name).

An Azelf whose blue head has grown into a long hood that rises and curls over to one side, with a red gem on its
brow and yellow eyes with red pupils. Teal fins spotted with darker teal spread from its shoulders, and its two very
long pale tails trail far below it, each ending in three lobes set with red gems.

Shiny: a mint-green hood and violet fins.

Front is -z, y is up. 38 units tall (tails to hood); about 1.0 block.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _lake import body, brow_gem, fins, skin, solid, tail
from _pgen1 import smooth_path
from _regi import ellipsoid, lit
from _route import mix, pal, tone

HEIGHT = 38
SCALE = round(1.0 * 16 / HEIGHT, 3)
HITBOX = [0.7, HEIGHT / 16]
KIND = "floater"
K = 4
LOOK = ("an Azelf whose blue head is a long hood curling over to one side, with a red brow gem, yellow eyes, teal "
        "spotted shoulder fins and two very long trailing tails ending in red-gemmed lobes")

BASE = {"skin": (228, 238, 255), "skin_dark": (190, 204, 236), "blue": (112, 192, 228), "blue_dark": (70, 140, 196),
        "blue_light": (176, 226, 248), "red": (220, 40, 52), "red_light": (255, 128, 116), "teal": (84, 170, 178),
        "teal_dark": (34, 100, 118), "teal_light": (150, 214, 220), "line": (130, 140, 176), "eye": (255, 214, 60),
        "pupil": (190, 30, 40), "lid": (40, 60, 90)}
SHINY = {"blue": (120, 220, 170), "blue_dark": (70, 170, 130), "blue_light": (190, 246, 216), "teal": (130, 96, 186),
         "teal_dark": (80, 50, 130), "teal_light": (190, 160, 230)}
CY = 22.0
HY = 29.4


def P(v):
    return pal(BASE, SHINY, v)


def headf(x, y, z, face, variant, **k):
    """Blue head; yellow eyes with red pupils under dark brows on its front, the face below them pale."""
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = (x - sx * 1.35) * sx, y - (HY - 0.4)
            if dx * dx / 0.9 + dy * dy / 0.7 < 1.0:
                if abs(dx + 0.1) < 0.3 and abs(dy) < 0.6:
                    return p["pupil"], None
                return p["eye"], None
            if -1.0 < dx < 1.1 and 0.7 < dy - 0.4 * dx < 1.0:
                return p["lid"], None
        if y < HY - 1.4:
            return lit(p["skin"], face, y, HY, 3), None
    return lit(p["blue"], face, y, HY, 3.2), None


def hoodf(x, y, z, face, variant, box=None, **k):
    """The hood: blue, lighter along its top."""
    p = P(variant)
    if face == "up":
        return p["blue_light"], None
    return tone(p["blue"] if face != "down" else p["blue_dark"], face), None


def build() -> Model:
    m = Model("sunkenvalor")
    top = m.bone("sunkenvalor", None, (0, 0, 0))
    bd = m.bone("body", top, (0, CY, 0))
    body(m, bd, CY, P)
    m.round_box(bd, 0, 0.2, 3.0, 2.6, CY + 3.0, CY + 4.4, solid(P, "teal"), cut=1)  # collar
    fins(m, bd, [(2.4, 26.4), (5.4, 27.2), (9.6, 26.6), (8.2, 25.4), (9.2, 24.0), (6.8, 24.2), (7.0, 22.6),
                 (4.8, 23.4), (2.4, 24.4)], 0.6, P)
    hd = m.bone("head", bd, (0, CY + 4.8, 0))
    ellipsoid(m, hd, 0, HY, -0.4, 3.4, 3.0, 3.2, headf, step=1)                    # head
    brow_gem(m, hd, (0, HY + 1.4, -3.0), (0, 1, -0.6), P, w=1.4, h=2.6)
    for sx in (-1, 1):                                                           # the hood's side lobes
        ellipsoid(m, hd, sx * 3.0, HY + 0.8, 0.4, 1.4, 2.2, 1.8, hoodf, step=1)
    cap = m.bone("cap", hd, (0, HY + 2.4, 0.2))                                    # the long curling hood
    pts = smooth_path([(0, HY + 2.0, 0.2), (0.6, HY + 4.6, 0.4), (2.6, HY + 7.0, 0.6), (5.6, HY + 7.6, 0.6),
                       (8.0, HY + 6.0, 0.4), (8.8, HY + 3.6, 0.2)], 12)
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        w = 5.2 - 4.4 * i / (len(pts) - 2)
        rod(m, cap, a, b, max(1.0, round(w * 0.8 * 2) / 2), hoodf, extend=0.8, t2=max(1.0, round(w * 2) / 2))
    tail(m, m.bone("tail_left", bd, (0.6, CY - 2.4, 1.6)),
         [(0.6, CY - 2.4, 1.6), (2.8, 15.0, 2.2), (3.4, 10.0, 1.2), (2.2, 6.0, 0.2)], 1.8, 1.0, P, lobe=4.4)
    tail(m, m.bone("tail_right", bd, (-0.6, CY - 2.4, 1.6)),
         [(-0.6, CY - 2.4, 1.6), (-3.6, 15.4, 2.4), (-5.8, 11.0, 1.6), (-6.6, 6.6, 0.4)], 1.8, 1.0, P, lobe=4.4)
    return m
