"""Shared builder for Pucchiemon and Pucchiemon (Green) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the Armor Digimon of kindness: a little fairy imp with a white body, a red scarf, a round button on its
chest, a red-hooded head with a pale face and black eyes, two long antennae bent at the elbow and ending in big heart
arrowheads, small cupped red wings, big red gloves and chunky red boots; one hand glows with a soft pink orb. Green:
the same in lime green. Shiny: the other colour's wings, blue.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone


def make(name, green=False):
    col = (130, 200, 60) if green else (220, 50, 40)
    dark = (60, 130, 20) if green else (130, 16, 14)
    base = {"col": col, "col_dark": dark, "white": (250, 250, 252), "white_dark": (200, 200, 214),
            "face": (252, 240, 236), "black": (20, 20, 24), "button": (60, 160, 70) if not green else (220, 60, 60),
            "orb": (250, 180, 200, 200), "blush": (250, 170, 180)}
    shiny = {"col": (60, 110, 220), "col_dark": (20, 50, 140)}

    def P(v):
        return pal(base, shiny, v)

    COL = skin(P, "col", dark="col_dark", var=0.03)

    def headf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north" and abs(x) < 2.4 and 19.0 < y < 22.4:
            for sx in (-1, 1):
                if math.hypot(x - sx * 0.9, (y - 21.0) * 0.7) < 0.5:
                    return tone(p["black"], face), None
            return tone(p["face"], face), None
        return COL(x, y, z, face, variant, box=box, **k)

    def bodyf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north" and math.hypot(x, y - 14.0) < 0.6:
            return tone(p["button"], face), None
        return skin(P, "white", dark="white_dark", var=0.02)(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 6, 0))
        m.round_box(bd, 0, 0, 2.6, 2.2, 7.0, 16.6, bodyf, cut=1)
        m.round_box(bd, 0, 0, 3.0, 2.6, 16.0, 17.6, COL, cut=1)                           # scarf
        rod(m, bd, (1.6, 17.0, -2.4), (3.0, 14.0, -3.0), 1, COL, extend=0.2, t2=2)
        hd = m.bone("head", bd, (0, 17, 0))
        ball(m, hd, (0, 21.0, -0.2), 3.4, headf, layers=3, ry=3.6)
        for sx in (-1, 1):                                                               # pointed ears
            spike(m, hd, (sx * 3.0, 22.0, 0), (sx * 1, 0.6, 0), 1.6, 3.0, COL, tip=0.8)
            pts = [(sx * 1.0, 24.0, 0), (sx * 4.0, 31.0, 1.0), (sx * 11.0, 30.0, 1.0), (sx * 13.0, 16.0, 1.0)]
            for p0, p1 in zip(pts, pts[1:]):                                              # bent antennae
                rod(m, hd, p0, p1, 1, COL, extend=0.3, t2=2)
            m.box(hd, sx * 13.0 - 2.6, 13.0, 0.6, sx * 13.0 + 2.6, 17.0, 1.4, COL)          # heart arrowheads
            spike(m, hd, (sx * 13.0, 13.4, 1.0), (0, -1, 0), 2.0, 2.4, COL, tip=0.8)
        for sx in (-1, 1):                                                               # small cupped wings
            m.box(bd, min(sx * 2.0, sx * 6.0), 14.0, 2.4, max(sx * 2.0, sx * 6.0), 18.0, 2.4, COL,
                  rotation=(0, -sx * 30, 0), pivot=(sx * 2.0, 16.0, 2.4))
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab = m.bone(nm, bd, (sx * 2.6, 15.0, 0))
            rod(m, ab, (sx * 2.6, 15.0, 0), (sx * 5.0, 12.0, -1.0), 1, bodyf, extend=0.2, t2=2)
            ball(m, ab, (sx * 5.6, 11.4, -1.4), 1.8, COL, layers=2)
        ball(m, "arm_left", (7.4, 14.0, -3.0), 1.8, solid(P, "orb", glow=True), layers=2)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, top, (sx * 1.4, 7.0, 0))
            m.round_box(lg, sx * 1.4, 0, 1.0, 1.0, 3.0, 7.4, bodyf, cut=0)
            m.round_box(lg, sx * 1.6, -0.8, 2.0, 2.8, 0.0, 4.0, COL, cut=1)                # chunky boots
        return m

    return build
