"""Shared builder for Thunderballmon and Thunderballmon (X-Antibody) (CobbleEffort: Digital; hand-built after the
official art on wikimon.net): a navy ball with a golden lightning-bolt crest, big round eyes and a wide mouth,
floating white-gloved fists with orange rivets, short legs in red-and-white boots, and a ring of crackling lime
lightning round it. X-Antibody: brighter blue with a red X scar across its face, a mechanical arm holding up a glowing
light bulb, a leather glove on the other hand, and tangled red and teal cables. Shiny: orange."""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import eye, leather, metal, plane, skin, solid
from _route import pal, tone

BASE = {"navy": (40, 50, 130), "navy_dark": (16, 20, 70), "gold": (250, 200, 50), "white": (250, 250, 250),
        "glove": (240, 240, 246), "glove_dark": (180, 180, 196), "red": (210, 40, 40), "orange": (240, 140, 40),
        "eye": (200, 40, 40), "pupil": (20, 10, 10), "mouth": (130, 20, 30), "bolt": (200, 250, 60),
        "brown": (150, 100, 60), "brown_dark": (90, 56, 30), "steel": (180, 184, 196), "steel_dark": (90, 94, 106),
        "bulb": (255, 250, 190), "teal": (60, 170, 170), "x": (220, 50, 40)}
SHINY = {"navy": (230, 120, 40), "navy_dark": (150, 60, 14)}


def make(name, x=False):
    base = dict(BASE)
    if x:
        base.update(navy=(70, 110, 200), navy_dark=(30, 50, 120))

    def P(v):
        return pal(base, SHINY, v)

    def ballf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            a, b = plane(xx, y, z, face)
            if x and (abs(a - (b - 15.0)) < 0.6 or abs(a + (b - 15.0)) < 0.6) and abs(a) < 3.4 and b < 18.4:
                return p["x"], None
            for sx in (-1, 1):
                c = eye(p, a - sx * 2.4, b - 17.6, 1.6, "eye")
                if c is not None:
                    return c, None
            if 11.4 < b < 13.6 and abs(a) < 2.4 - (b - 11.4) * 0.3:
                return p["mouth"], None
        return metal(P, "navy", dark="navy_dark")(xx, y, z, face, variant, box=box, **k)

    GLOVE = skin(P, "glove", dark="glove_dark")

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 10, 0))
        ball(m, bd, (0, 15.0, 0), 6.6, ballf, layers=6)
        hd = m.bone("head", bd, (0, 21, 0))
        for j in range(4):                                                             # lightning-bolt crest
            m.box(hd, -1.0 + (j % 2) * 1.6, 21.0 + j * 2.2, -1.0, 1.0 + (j % 2) * 1.6, 23.4 + j * 2.2, 1.0,
                  solid(P, "gold"), rotation=(0, 0, 20 if j % 2 else -20), pivot=(0, 22.0 + j * 2.2, 0))
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab = m.bone(nm, bd, (sx * 6.0, 15.0, 0))
            if x and sx > 0:                                                           # mechanical bulb arm
                pts = [(6.0, 15.0, 0), (10.0, 18.0, -1.0), (12.0, 24.0, -2.0)]
                for p0, p1 in zip(pts, pts[1:]):
                    rod(m, ab, p0, p1, 1, metal(P, "steel", dark="steel_dark"), extend=0.4)
                ball(m, ab, (12.0, 27.6, -2.0), 2.6, solid(P, "bulb", glow=True), layers=3)
                m.round_box(ab, 12.0, -2.0, 1.4, 1.4, 23.6, 25.2, metal(P, "steel"), cut=0)
            else:
                h = (sx * 10.0, 13.0, -3.0)
                ball(m, ab, h, 2.4, GLOVE if not x else leather(P, "brown", "brown_dark"), layers=3)
                for j in range(3):
                    ball(m, ab, (h[0] + sx * 0.6, h[1] + 1.2 - j * 1.2, h[2] - 2.2), 0.5, solid(P, "orange"), layers=1)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, top, (sx * 2.4, 9.0, 0))
            rod(m, lg, (sx * 2.4, 9.0, 0), (sx * 2.8, 3.0, 0), 1, solid(P, "navy_dark"), extend=0.4)
            m.round_box(lg, sx * 2.8, -0.8, 1.8, 2.6, 0.0, 3.2, solid(P, "red"), cut=1)
            m.box(lg, sx * 2.8 - 1.9, 0.0, -3.5, sx * 2.8 + 1.9, 1.0, -2.0, solid(P, "white"))
        if x:                                                                          # tangled cables
            for k, (c, pts) in enumerate((("red", [(-3, 10, 4), (-8, 6, 6), (-9, 1, 3), (-6, 0.5, 0)]),
                                          ("teal", [(3, 10, 4), (8, 8, 6), (11, 4, 3), (12, 1, 0)]))):
                for p0, p1 in zip(pts, pts[1:]):
                    rod(m, bd, p0, p1, 1, solid(P, c), extend=0.3)
        else:                                                                          # lime lightning ring
            rg = m.bone("ring", top, (0, 2, 0))
            for i in range(18):
                ang = i * 2 * math.pi / 18
                r = 11.0 + (1.0 if i % 2 else -1.0)
                m.box(rg, r * math.cos(ang) - 1.0, 1.0, r * math.sin(ang) - 1.0, r * math.cos(ang) + 1.0, 2.6,
                      r * math.sin(ang) + 1.0, solid(P, "bolt", glow=True))
        return m
    return build
