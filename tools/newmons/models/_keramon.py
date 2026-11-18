"""Shared builder for Keramon and Keramon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the bug that eats data: a pale lavender round head with green ringed eyes and a wide stitched grin, a
spiky yellow collar, long wavy antennae, a skirt of dangling tendrils for a body and two long thin arms ending in big
clawed hands with an eye on each palm. X-Antibody: a bigger dark-veined head covered in red-ringed eyes, a mouth
stretched open, a crown of feathered spikes and longer tangled tendrils. Shiny: mint green.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import skin, solid, strands
from _route import pal, tone

BASE = {"lav": (190, 180, 230), "lav_dark": (120, 110, 170), "lav_light": (230, 226, 250), "yellow": (250, 210, 50),
        "eye": (60, 190, 90), "eye_ring": (30, 30, 40), "mouth": (40, 30, 50), "vein": (150, 30, 60), "red": (220, 40, 60),
        "tooth": (250, 250, 250)}
SHINY = {"lav": (160, 230, 190), "lav_dark": (80, 160, 120), "lav_light": (220, 255, 235)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    def headf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        hy = 20.0 if not x else 22.0
        if face == "north":
            spots = [(-1.8, hy + 1.0), (1.8, hy + 1.0)] if not x else [(-2.6, hy + 2.0), (2.6, hy + 2.0), (0, hy + 3.4),
                                                                       (-3.6, hy - 0.6), (3.6, hy - 0.6)]
            for (ex, ey) in spots:
                d = math.hypot(xx - ex, y - ey)
                if d < 0.5:
                    return tone(p["eye_ring"], face), None
                if d < 1.0:
                    return tone(p["eye"] if not x else p["red"], face), (p["red"] if x else None)
            if abs(y - (hy - 2.0) + 0.15 * xx * xx * (0.3 if not x else 0.15)) < (0.3 if not x else 1.0) and abs(xx) < 3.6:
                if (xx + 5.0) % 0.8 < 0.2:
                    return tone(p["tooth"], face), None
                return tone(p["mouth"], face), None
        if x and (int(xx * 1.7 + y * 0.9) % 5 == 0):
            return tone(p["vein"], face), None
        return skin(P, "lav", dark="lav_dark", light="lav_light")(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 8, 0))
        n = 10 if not x else 14                                                      # dangling tendril skirt
        for i in range(n):
            ang = 2 * math.pi * i / n
            pts = [(1.6 * math.cos(ang), 15.0, 1.6 * math.sin(ang)), (2.6 * math.cos(ang), 8.0, 2.6 * math.sin(ang)),
                   (3.0 * math.cos(ang + 0.4), 2.0 if not x else 0.4, 3.0 * math.sin(ang + 0.4))]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, bd, p0, p1, 1, strands(P, "lav", "lav_dark" if not x else "vein"), extend=0.2, t2=1)
        hd = m.bone("head", bd, (0, 16, 0))
        r = 4.6 if not x else 6.2
        ball(m, hd, (0, 20.0 if not x else 22.0, 0), r, headf, layers=5)
        for i in range(10):                                                            # spiky collar
            ang = 2 * math.pi * i / 10
            spike(m, hd, (2.4 * math.cos(ang), 15.6, 2.4 * math.sin(ang)), (math.cos(ang), -0.2, math.sin(ang)), 1.2,
                  2.4, solid(P, "yellow" if not x else "red"), tip=0.8)
        for sx in (-1, 1):                                                             # wavy antennae
            pts = [(sx * 1.6, 23.6 + (2 if x else 0), 0), (sx * 3.6, 29.0 + (2 if x else 0), 1.0),
                   (sx * 7.0, 30.0 + (2 if x else 0), 0.0), (sx * 8.0, 26.0 + (2 if x else 0), -1.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, hd, p0, p1, 1, solid(P, "lav_dark" if not x else "vein"), extend=0.2, t2=1)
        if x:
            for i in range(9):                                                         # crown of feathered spikes
                ang = math.radians(-80 + i * 20)
                spike(m, hd, (5.6 * math.sin(ang), 24.0 + 3.0 * math.cos(ang), 2.0), (math.sin(ang), math.cos(ang), 0.4), 1.4,
                      4.0, solid(P, "yellow"), tip=0.8)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                           # long thin arms, big hands
            ab = m.bone(nm, bd, (sx * 2.0, 14.0, 0))
            pts = [(sx * 2.0, 14.0, 0), (sx * 8.0, 10.0, -1.0), (sx * 10.0, 3.0, -2.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, ab, p0, p1, 1, skin(P, "lav", dark="lav_dark"), extend=0.3, t2=1)
            m.round_box(ab, sx * 10.0, -2.0, 2.0, 2.0, 0.0, 3.4, skin(P, "lav", dark="lav_dark"), cut=1)
            m.round_box(ab, sx * 10.0, -4.1, 0.8, 0.2, 1.2, 2.4, solid(P, "eye" if not x else "red"), cut=0)
            for j in range(4):
                spike(m, ab, (sx * 10.0 + (j - 1.5) * 1.0, 0.4, -2.6), ((j - 1.5) * 0.3, -0.6, -1), 0.8, 2.6,
                      skin(P, "lav", dark="lav_dark"), tip=0.8)
        return m

    return build
