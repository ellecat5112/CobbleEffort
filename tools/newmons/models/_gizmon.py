"""Shared builder for Gizmon: AT and Gizmon: XT (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the Gizumon war machines. AT: a black sphere with a glowing yellow-red eye, its body a bundle of
striped purple-and-green blade fins hanging like a jellyfish, wires trailing from under it. XT: the sphere set on a
violet torso with a white ringed waist, great purple-and-green swept blade wings, a small head pod with a red eye,
thin cabled legs ending in white pod feet. Shiny: red and grey.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import local, metal, solid
from _route import pal, tone


def make(name, xt=False):
    base = {"black": (36, 30, 44), "black_dark": (12, 10, 16), "violet": (110, 60, 170), "violet_dark": (50, 20, 90),
            "green": (60, 190, 70), "green_dark": (20, 110, 30), "eye": (250, 200, 40), "eye_core": (220, 40, 30),
            "white": (240, 240, 246), "white_dark": (170, 172, 190), "wire": (80, 90, 80)}
    shiny = {"violet": (190, 40, 50), "violet_dark": (100, 14, 20), "green": (170, 174, 186), "green_dark": (90, 94, 106)}

    def P(v):
        return pal(base, shiny, v)

    def bladef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        return tone(p["green"] if (u + v) % 4.0 < 1.4 else p["violet"], face), None

    def spheref(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            d = math.hypot(x, y - cy)
            if d < 0.8:
                return p["eye_core"], p["eye_core"]
            if d < 1.6:
                return p["eye"], p["eye"]
        return metal(P, "black" if not xt else "violet", dark="black_dark" if not xt else "violet_dark")(
            x, y, z, face, variant, box=box, **k)

    cy = 30.0 if not xt else 30.0

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 20, 0))
        ball(m, bd, (0, cy, 0), 6.0, spheref, layers=5)
        if not xt:                                                                      # hanging blade fins
            for i in range(8):
                ang = 2 * math.pi * i / 8
                c = (4.0 * math.cos(ang), 24.0, 4.0 * math.sin(ang))
                m.box(bd, c[0] - 1.8, 6.0 + (i % 2) * 3.0, c[2] - 0.3, c[0] + 1.8, 24.0, c[2] + 0.3, bladef,
                      rotation=(0, -math.degrees(ang) + 90, 8 * math.cos(ang)), pivot=c)
            for j in range(5):
                rod(m, bd, ((j - 2) * 1.2, 24.0, -1.0), ((j - 2) * 2.0, 12.0, -4.0), 1, solid(P, "wire"), extend=0, t2=1)
            hd = m.bone("head", bd, (0, 34, 0))
            spike(m, hd, (0, 35.4, 0), (0, 1, 0.6), 2.4, 5.0, bladef, tip=1.0)
            return m
        m.round_box(bd, 0, 0, 4.0, 3.0, 18.0, 25.0, metal(P, "violet", dark="violet_dark"), cut=1)   # torso
        m.round_box(bd, 0, 0, 3.0, 2.6, 14.0, 18.6, metal(P, "white", dark="white_dark"), cut=1)      # ringed waist
        hd = m.bone("head", bd, (0, 36, 0))
        m.round_box(hd, 0, -1.0, 1.6, 1.6, 36.0, 40.0, metal(P, "white", dark="white_dark"), cut=1)
        m.box(hd, -0.6, 37.6, -2.8, 0.6, 38.6, -2.6, solid(P, "eye_core", glow=True))
        for side in (1, -1):                                                              # swept blade wings
            for j in range(3):
                x0, x1 = sorted((side * 5.0, side * (22.0 - j * 4.0)))
                m.box(bd, x0, 30.0 - j * 4.0, 1.0 + j, x1, 33.0 - j * 4.0, 1.6 + j, bladef,
                      rotation=(0, side * 15, side * (30 - j * 18)), pivot=(side * 5.0, 31.0 - j * 4.0, 1.0))
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, top, (sx * 2.0, 14.0, 0))
            pts = [(sx * 2.0, 14.0, 0), (sx * 4.0, 8.0, -1.0), (sx * 3.0, 2.0, 1.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, lg, p0, p1, 1, solid(P, "green"), extend=0.3, t2=1)
            m.round_box(lg, sx * 3.0, 0.0, 1.6, 2.2, 0.0, 2.6, metal(P, "white", dark="white_dark"), cut=1)
        return m

    return build
