"""Shared builder for Plotmon and Plotmon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): a cream puppy with a round head, long floppy ears, big green eyes, blushing cheeks, an open little
mouth, stubby legs with round feet, and a golden collar. X-Antibody: a warmer peach coat and its collar grown into a
great golden ring round its body engraved with dark runes. Shiny: pale lilac.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import fur, metal, solid
from _route import pal, tone

BASE = {"cream": (250, 244, 214), "cream_dark": (210, 196, 160), "peach": (250, 226, 170), "eye": (40, 150, 110),
        "pupil": (20, 30, 30), "white": (255, 255, 255), "blush": (250, 170, 180), "mouth": (220, 80, 100),
        "gold": (220, 170, 60), "gold_dark": (120, 80, 20), "rune": (60, 40, 20)}
SHINY = {"cream": (230, 220, 250), "cream_dark": (180, 170, 220), "peach": (236, 214, 250)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    key = "peach" if x else "cream"
    FUR = fur(P, key, "cream_dark", length=1.2, density=1.6)

    def headf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                d = math.hypot((xx - sx * 1.8) * 0.9, y - 15.4)
                if d < 0.55:
                    return tone(p["pupil"], face), None
                if d < 0.75 and xx * sx > 1.9:
                    return tone(p["white"], face), None
                if d < 1.3:
                    return tone(p["eye"], face), None
                if math.hypot(xx - sx * 3.0, y - 13.6) < 0.8:
                    return tone(p["blush"], face), None
            if 12.6 < y < 13.8 and abs(xx) < 0.9:
                return tone(p["mouth"], face), None
        return FUR(xx, y, z, face, variant, box=box, **k)

    def runef(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face not in ("up", "down") and abs(math.sin(math.atan2(z, xx) * 7)) > 0.85 and 6.4 < y < 8.6:
            return tone(p["rune"], face), None
        return metal(P, "gold", dark="gold_dark")(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 3, 0))
        ball(m, bd, (0, 6.6, 0.6), 3.0, FUR, layers=3, ry=3.4)
        hd = m.bone("head", bd, (0, 10, 0))
        ball(m, hd, (0, 14.6, -0.4), 4.4, headf, layers=4, ry=4.0)
        for sx in (-1, 1):                                                              # long floppy ears
            ex = m.bone("ear_left" if sx > 0 else "ear_right", hd, (sx * 3.6, 17.0, 0))
            if x:
                x0, x1 = sorted((sx * 3.6, sx * 10.0))
                m.box(ex, x0, 16.0, -1.4, x1, 18.0, 1.4, FUR, rotation=(0, 0, sx * 10), pivot=(sx * 3.6, 17.0, 0))
            else:
                m.round_box(ex, sx * 4.6, 0.4, 1.0, 1.6, 9.0, 17.0, FUR, cut=0)
        if x:                                                                            # the great golden ring
            for i in range(14):
                ang = 2 * math.pi * i / 14
                cx, cz = 4.6 * math.cos(ang), 0.6 + 4.6 * math.sin(ang)
                m.box(bd, cx - 1.4, 6.0, cz - 1.4, cx + 1.4, 9.0, cz + 1.4, runef)
        else:
            m.round_box(bd, 0, 0.4, 2.8, 2.8, 9.0, 10.0, metal(P, "gold", dark="gold_dark"), cut=1)
        for sx, nm in ((1, "leg_front_left"), (-1, "leg_front_right"), (1, "leg_back_left"), (-1, "leg_back_right")):
            zz = -1.6 if "front" in nm else 2.6
            lg = m.bone(nm, top, (sx * 1.8, 4.0, zz))
            m.round_box(lg, sx * 1.8, zz, 1.2, 1.2, 0.8, 5.0, FUR, cut=0)
            m.round_box(lg, sx * 1.8, zz - 0.4, 1.6, 1.8, 0.0, 1.4, FUR, cut=0)
        rod(m, bd, (0, 6.0, 3.4), (0, 8.0, 5.4), 1, FUR, extend=0.2, t2=1)
        return m

    return build
