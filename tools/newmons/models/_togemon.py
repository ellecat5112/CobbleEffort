"""Shared builder for Togemon and Togemon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): a walking green cactus with ribbed sides and little spines, three dark holes for a face, an orange tuft
on top, stubby cactus arms in big red boxing gloves, and two thick cactus legs. X-Antibody: a straw sombrero with a
zigzag band, a yellow fringed poncho with a gold clasp, an angry face and a beak-like orange flower. Shiny: blue-grey
cactus, purple gloves."""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import fabric, leather, plane, skin, solid
from _route import pal, tone

BASE = {"green": (150, 200, 60), "green_dark": (80, 130, 30), "spine": (60, 80, 30), "hole": (20, 30, 10),
        "tuft": (240, 140, 50), "red": (210, 50, 40), "red_dark": (130, 20, 14), "straw": (240, 200, 80),
        "straw_dark": (190, 140, 40), "zig": (230, 100, 40), "poncho": (240, 220, 80), "poncho_dark": (200, 160, 30),
        "gold": (220, 170, 60)}
SHINY = {"green": (130, 160, 180), "green_dark": (70, 100, 120), "red": (140, 60, 190), "red_dark": (80, 20, 120)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    def cactusf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north" and box is not None and box.size[1] > 10:
            a, b = plane(xx, y, z, face)
            for cx, cy, r in ((-1.8, 21.0, 1.0), (1.8, 21.0, 1.0), (0, 17.6, 1.2)):
                if math.hypot((a - cx) / (r * 0.8), (b - cy) / r) < 1.0:
                    return p["hole"], None
            if x and abs(b - 22.6 + abs(a) * 0.4) < 0.3 and 0.8 < abs(a) < 3.0:
                return p["hole"], None
        ang = math.atan2(xx, z)
        if (ang * 4.0) % 1.0 < 0.12:
            return tone(p["green_dark"], face), None
        if (int(y * 1.3) * 7 + int(ang * 8) * 3) % 41 == 0:
            return tone(p["spine"], face), None
        return skin(P, "green", dark="green_dark")(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 8, 0))
        m.round_box(bd, 0, 0, 5.4, 4.6, 8.0, 27.0, cactusf, cut=2)
        hd = m.bone("head", bd, (0, 27, 0))
        for j in range(5):
            spike(m, hd, ((j - 2) * 0.8, 27.0, 0), ((j - 2) * 0.4, 1, 0.1), 1.2, 3.0, solid(P, "tuft"), tip=0.8)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab = m.bone(nm, bd, (sx * 5.0, 18.0, 0))
            rod(m, ab, (sx * 5.0, 17.0, 0), (sx * 9.0, 18.0, 0), 2, cactusf, extend=0.4)
            rod(m, ab, (sx * 9.0, 18.0, 0), (sx * 9.0, 22.0, -1.0), 2, cactusf, extend=0.4)
            ball(m, ab, (sx * 9.4, 24.0, -1.6), 2.8, leather(P, "red", "red_dark"), layers=3)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, top, (sx * 2.6, 8.0, 0))
            m.round_box(lg, sx * 2.8, 0, 2.4, 2.8, 0.0, 9.0, cactusf, cut=1)
        if x:
            m.round_box(hd, 0, 0, 9.0, 9.0, 27.4, 28.4, fabric(P, "straw", "straw_dark"), cut=4)   # sombrero brim
            m.round_box(hd, 0, 0, 4.0, 4.0, 28.4, 32.4, fabric(P, "straw", "straw_dark"), cut=2)
            m.round_box(hd, 0, 0, 4.2, 4.2, 28.4, 29.6, solid(P, "zig"), cut=2)
            for sx in (-1, 1):                                                          # fringed poncho
                m.box(bd, min(sx * 0.2, sx * 6.0), 13.0, -5.2, max(sx * 0.2, sx * 6.0), 26.0, -4.4,
                      fabric(P, "poncho", "poncho_dark"), rotation=(0, 0, -sx * 12), pivot=(0, 26.0, -4.8))
            m.box(bd, -6.0, 14.0, 4.4, 6.0, 26.0, 5.2, fabric(P, "poncho", "poncho_dark"))
            ball(m, bd, (0, 24.0, -5.6), 1.2, solid(P, "gold"), layers=1)
            spike(m, bd, (0, 18.6, -4.6), (0, 0, -1), 1.6, 2.0, solid(P, "tuft"), tip=0.8)
        return m
    return build
