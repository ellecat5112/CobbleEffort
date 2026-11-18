"""Mikemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a calico cat of white, orange and dark brown patches leaping with one enormous paw stretched out, its
long white arm ending in curved claws, a pink paw pad on its other paw, huge pink-lined pointed ears, amber eyes and a
long striped tail with a tufted fork. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a calico cat of white, orange and brown patches with one enormous long white clawed arm, huge pink-lined "
        "ears, amber eyes and a long striped tail")
BASE = {"white": (248, 246, 240), "white_dark": (196, 192, 184), "orange": (230, 140, 60), "orange_dark": (160, 80, 24),
        "brown": (110, 60, 40), "pink": (240, 160, 170), "eye": (240, 170, 40), "pupil": (30, 20, 10),
        "claw": (230, 226, 216), "nose": (200, 80, 90)}
SHINY = {"orange": (120, 120, 130), "orange_dark": (60, 60, 70), "brown": (40, 40, 48)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = fur(P, "white", "white_dark", length=1.2)


def calicof(x, y, z, face, variant, box=None, **k):
    """White fur with orange and brown patches."""
    p = P(variant)
    a = math.sin(x * 0.45 + 1.0) * math.sin(y * 0.38) + 0.6 * math.sin(z * 0.5 - y * 0.2)
    if a > 0.65:
        return tone(p["orange"], face), None
    if a < -0.75:
        return tone(p["brown"], face), None
    return WHITE(x, y, z, face, variant, box=box, **k)


def tailf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs((z % 2.6) - 1.3) < 0.5:
        return tone(p["brown"], face), None
    return tone(p["orange"], face), None


def build():
    m = Model("mikemon")
    top = m.bone("mikemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    ball(m, bd, (0, 14.0, 1.0), 4.4, calicof, layers=4, ry=5.4)                             # body
    hd = m.bone("head", bd, (0, 20, 0))
    ball(m, hd, (0, 24.0, -0.4), 5.4, calicof, layers=5, ry=4.6, squash=0.85)               # head
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 3.0), 24.6, -4.65, max(sx * 1.0, sx * 3.0), 26.6, -4.5, solid(P, "eye"))
        m.box(hd, min(sx * 1.8, sx * 2.4), 24.8, -4.7, max(sx * 1.8, sx * 2.4), 26.4, -4.65, solid(P, "pupil"))
        eb = m.bone("ear_left" if sx > 0 else "ear_right", hd, (sx * 3.0, 27.0, 0))         # huge pointed ears
        spike(m, eb, (sx * 3.4, 27.0, 0), (sx * 0.8, 1, 0.1), 5.0, 9.0, WHITE, tip=0.8)
        spike(m, eb, (sx * 3.6, 27.4, -0.8), (sx * 0.8, 1, 0.1), 3.6, 7.0, solid(P, "pink"), tip=0.8)
    m.box(hd, -0.6, 23.0, -4.75, 0.6, 23.6, -4.55, solid(P, "nose"))
    al = m.bone("arm_left", bd, (4.0, 17.0, -1.0))                                          # small left paw
    rod(m, al, (4.0, 17.0, -1.0), (7.0, 20.0, -3.0), 2, calicof, extend=0.3)
    ball(m, al, (7.6, 21.0, -3.4), 1.8, WHITE, layers=2)
    m.box(al, 6.8, 20.0, -5.3, 8.4, 21.8, -5.1, solid(P, "pink"))
    ar = m.bone("arm_right", bd, (-4.0, 16.0, -1.0))                                        # enormous long arm
    rod(m, ar, (-4.0, 16.0, -1.0), (-10.0, 11.0, -8.0), 3, WHITE, extend=0.4)
    rod(m, ar, (-10.0, 11.0, -8.0), (-16.0, 6.0, -15.0), 4, WHITE, extend=0.4)
    ball(m, ar, (-17.0, 5.0, -16.0), 3.0, WHITE, layers=3)
    for f in range(4):
        pts = [(-17.0 + (f - 1.5) * 1.4, 3.0, -18.0), (-17.0 + (f - 1.5) * 1.8, 1.0, -21.0),
               (-17.0 + (f - 1.5) * 1.8, 2.0, -23.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ar, p0, p1, 1, solid(P, "claw"), extend=0.2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.4, 10.0, 1.0))
        rod(m, lg, (sx * 2.4, 11.0, 1.0), (sx * 3.0, 6.0, 3.0), 2, calicof, extend=0.3)
        rod(m, lg, (sx * 3.0, 6.0, 3.0), (sx * 3.0, 1.0, 1.0), 2, calicof, extend=0.3)
        m.round_box(lg, sx * 3.0, 0.0, 1.4, 2.2, 0.0, 1.6, WHITE, cut=0)
    tb = m.bone("tail", bd, (0, 11, 5))                                                     # long striped tail
    pts = [(0, 11.0, 5.0), (2.0, 13.0, 10.0), (5.0, 18.0, 13.0), (7.0, 24.0, 14.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 2, tailf, extend=0.3)
    for s in (-1, 1):
        spike(m, tb, pts[-1], (s * 0.6, 1, 0.2), 1.2, 3.0, solid(P, "brown"), tip=0.8)
    return m
