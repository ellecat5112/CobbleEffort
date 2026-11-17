"""Bio Coatlmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a feathered serpent of the Bio Hybrid line. A long white armoured serpent body ringed with red and
gold bands, a red feathered head-mask with gold marks and blue eyes, a crest of green and white plumes with a
crystal spike, great white wings, and a tail ending in a gold flame-shaped torch. 15 blocks tall.

Front is -z, y is up. 50 units tall; Adult stage (Armor).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, eye, feathers, gem, metal, plane, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(15, HEIGHT, 2.4)
KIND = "floater"
K = 3
LOOK = ("a feathered serpent: a long white armoured body ringed in red and gold, a red feathered head-mask with blue "
        "eyes, a crest of green and white plumes, great white wings and a gold flame-torch tail")
BASE = {"white": (246, 246, 250), "white_dark": (180, 184, 198), "red": (200, 30, 40), "red_dark": (120, 10, 20),
        "gold": (236, 196, 60), "gold_dark": (160, 120, 30), "green": (40, 140, 90), "green_dark": (16, 80, 50),
        "crystal": (90, 210, 170), "crystal_light": (210, 255, 240), "eye": (60, 140, 230), "pupil": (16, 20, 30),
        "grey": (120, 124, 136)}
SHINY = {"white": (60, 60, 74), "white_dark": (26, 26, 34), "red": (60, 140, 220), "red_dark": (20, 70, 140),
         "green": (190, 90, 160), "green_dark": (110, 40, 90)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = armour(P, "white", "white_dark")


def ringf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = (box.lo[2] + box.size[2] - z) if box else 0
    band = t % 6.0
    if band < 0.9:
        return tone(p["red"], face), None
    if band < 1.4:
        return tone(p["gold"], face), None
    return WHITE(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 7.0, y - 42.0, 1.0, "eye")
        if c is not None:
            return c, None
        if abs(y - 40.0) < 0.3 or abs(z + 8.0) < 0.3:
            return tone(p["gold"], face), None
    return armour(P, "red", "red_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("biocoatlmon")
    top = m.bone("biocoatlmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 26, 0))
    pts = []
    for i in range(14):                                          # the serpent body: an S from head down to a coil
        t = i / 13
        pts.append((6.0 * math.sin(t * 5.0), 40.0 - 34.0 * t, -6.0 + 10.0 * math.sin(t * 3.0)))
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, bd, p0, p1, max(2, round(5.4 - i * 0.2)), ringf, extend=0.8)
    hd = m.bone("head", bd, pts[0])
    m.round_box(hd, pts[0][0], -8.0, 3.0, 4.0, 38.0, 45.0, headf, cut=1)
    m.box(hd, pts[0][0] - 2.0, 38.0, -13.0, pts[0][0] + 2.0, 41.4, -11.0, armour(P, "red", "red_dark"))
    F = feathers(P, "green", "green_dark", size=(1.4, 3.0), flow=(0, 1), tip="white")
    for j in range(7):                                           # plume crest
        ang = math.radians(-50 + j * 16)
        rod(m, hd, (pts[0][0], 45.0, -6.0), (pts[0][0] + 6.0 * math.sin(ang), 52.0, -2.0 + 6.0 * math.cos(ang) * 0.5),
            2, F, extend=0.2, t2=1)
    spike(m, hd, (pts[0][0], 45.0, -4.0), (0, 1, 0.6), 1.8, 6.0, gem(P, "crystal", "crystal_light"), tip=0.8)
    W = feathers(P, "white", "white_dark", size=(1.6, 3.0), flow=(0, -1))
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):        # great white wings
        wb = m.bone(nm, bd, (sx * 3.0, 34.0, -2.0))
        for i in range(9):
            t = i / 8
            base = (sx * (3.0 + 16.0 * t), 34.0 + 10.0 * t, -2.0 + 3.0 * t)
            ln = 8.0 + 12.0 * t
            m.box(wb, base[0] - 1.8, base[1] - ln, base[2], base[0] + 1.8, base[1], base[2], W,
                  rotation=(-10, 0, -sx * (50 - 30 * t)), pivot=base)
    tl = m.bone("tail", bd, pts[-1])                             # gold flame torch
    e = pts[-1]
    for j in range(4):
        ang = math.radians(-40 + j * 27)
        spike(m, tl, e, (math.sin(ang), -0.4, math.cos(ang) * 0.3 + 0.6), 1.2, 3.6, metal(P, "gold", dark="gold_dark"),
              tip=0.4)
    return m
