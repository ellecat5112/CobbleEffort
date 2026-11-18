"""Shared builder for Mamemon and Mamemon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the tiny powerhouse: a small round silver ball head with big round eyes and a cheeky open grin, a red
ball body and two huge red mechanical boxing fists on jointed steel arms, and stubby legs. X-Antibody: flame-painted
black-and-red armour, spiked fists on long blue straps like flails, and spiked knee pads. Shiny: green.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import armour, leather, metal, skin, solid
from _route import pal, tone

BASE = {"silver": (210, 214, 226), "silver_dark": (100, 104, 120), "red": (210, 40, 40), "red_dark": (120, 14, 18),
        "black": (40, 38, 44), "black_dark": (12, 12, 14), "orange": (240, 120, 40), "blue": (60, 120, 210),
        "blue_dark": (20, 60, 140), "eye": (24, 20, 20), "white": (250, 250, 250), "mouth": (200, 60, 80),
        "gold": (230, 180, 60)}
SHINY = {"red": (60, 170, 80), "red_dark": (20, 90, 30)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    def headf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                d = math.hypot(xx - sx * 1.6, y - 13.6)
                if d < 0.5:
                    return tone(p["eye"], face), None
                if d < 1.1:
                    return tone(p["white"], face), None
            if 11.0 < y < 12.4 and abs(xx) < 1.6 - (12.4 - y) * 0.6:
                return tone(p["mouth"], face), None
        if x and face in ("east", "west", "up") and abs(math.sin(xx * 2.0 + y * 1.4)) > 0.9:
            return tone(p["black"], face), None
        return metal(P, "silver", dark="silver_dark")(xx, y, z, face, variant, box=box, **k)

    def flamef(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if abs(math.sin(xx * 1.6 + y * 1.2)) > 0.8:
            return tone(p["orange"], face), None
        return armour(P, "black", "black_dark")(xx, y, z, face, variant, box=box, **k)

    BODY = flamef if x else armour(P, "red", "red_dark")

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 3, 0))
        ball(m, bd, (0, 6.0, 0), 3.4, BODY, layers=3)
        hd = m.bone("head", bd, (0, 9, 0))
        ball(m, hd, (0, 13.0, -0.4), 4.0, headf, layers=4)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                        # huge fists
            ab = m.bone(nm, bd, (sx * 3.0, 8.0, 0))
            if not x:
                rod(m, ab, (sx * 3.0, 8.0, 0), (sx * 6.0, 12.0, -1.0), 1, metal(P, "silver", dark="silver_dark"), extend=0.3, t2=1)
                ball(m, ab, (sx * 7.4, 15.0, -2.0), 3.0, armour(P, "red", "red_dark"), layers=3)
            else:
                pts = [(sx * 3.0, 8.0, 0), (sx * 8.0, 12.0, 2.0), (sx * 10.0, 18.0, 0.0)]
                for p0, p1 in zip(pts, pts[1:]):
                    rod(m, ab, p0, p1, 1, leather(P, "blue", "blue_dark"), extend=0.2, t2=2)
                ball(m, ab, (sx * 10.0, 20.0, 0.0), 2.6, flamef, layers=3)
                for j in range(6):
                    ang = 2 * math.pi * j / 6
                    spike(m, ab, (sx * 10.0 + 2.4 * math.cos(ang), 20.0 + 2.4 * math.sin(ang), 0), (math.cos(ang), math.sin(ang), 0),
                          0.8, 2.0, metal(P, "gold", dark="black"), tip=0.8)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, top, (sx * 1.6, 3.0, 0))
            m.round_box(lg, sx * 1.8, -0.6, 1.4, 2.0, 0.0, 3.0, BODY, cut=0)
            if x:
                spike(m, lg, (sx * 1.8, 2.6, -2.0), (0, 0.4, -1), 0.8, 2.0, metal(P, "silver", dark="silver_dark"), tip=0.8)
        return m

    return build
