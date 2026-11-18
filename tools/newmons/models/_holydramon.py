"""Shared builder for Holydramon and Holydramon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art
on wikimon.net): the holy dragon, one of the Four Great Dragons: a long pink serpentine dragon covered in soft white
fur ruffs, a fierce dragon head with a pale mane and long black horns banded magenta, two small clawed arms, a slender
coiling tail ending in a tuft, and great pink wings (X-Antibody: magenta wings with a white belly). Shiny: gold.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import bat_wing
from _digidetail import fur, metal, skin, solid, strands
from _route import pal, tone


def make(name, x=False):
    base = {"pink": (240, 180, 210) if not x else (190, 70, 140), "pink_dark": (190, 110, 160) if not x else (120, 30, 80),
            "white": (246, 244, 250), "white_dark": (190, 186, 200), "black": (34, 30, 38), "magenta": (200, 40, 130),
            "eye": (60, 200, 110), "mouth": (180, 30, 60), "tooth": (250, 250, 240), "claw": (40, 36, 44)}
    shiny = {"pink": (250, 220, 130), "pink_dark": (200, 160, 60)}

    def P(v):
        return pal(base, shiny, v)

    HIDE = skin(P, "pink", dark="pink_dark")
    FUR = fur(P, "white", "white_dark", length=1.2)

    def hornf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if (y + z) % 3.0 < 0.8:
            return tone(p["magenta"], face), None
        return tone(p["black"], face), None

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 20, 0))
        pts = [(0, 34.0, -4.0), (2.0, 28.0, 0.0), (-2.0, 22.0, 3.0), (-4.0, 14.0, 0.0), (0.0, 8.0, -3.0), (5.0, 4.0, 0.0),
               (7.0, 2.0, 6.0), (4.0, 3.0, 11.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, bd, p0, p1, max(2, 7 - j), HIDE if j > 1 or not x else FUR, extend=0.6)
            if j < 4:
                m.round_box(bd, p0[0], p0[2], 4.0 - j * 0.6, 4.0 - j * 0.6, p0[1] - 1.0, p0[1] + 1.0, FUR, cut=1)
        for j in range(3):
            spike(m, bd, pts[-1], ((j - 1) * 0.5, -0.4, 1), 1.0, 4.0, strands(P, "white", "white_dark"), tip=0.8)
        hd = m.bone("head", bd, (0, 36, -5))
        m.round_box(hd, 0, -6.0, 3.0, 5.0, 34.0, 40.0, HIDE, cut=1)
        m.box(hd, -2.2, 34.4, -11.2, 2.2, 36.0, -10.9, solid(P, "mouth"))
        for j in range(4):
            spike(m, hd, (-1.6 + j * 1.1, 36.0, -11.0), (0, -1, 0), 0.6, 1.2, solid(P, "tooth"))
        for sx in (-1, 1):
            m.box(hd, min(sx * 3.0, sx * 3.2), 38.0, -8.0, max(sx * 3.0, sx * 3.2), 39.0, -7.0, solid(P, "eye", glow=True))
            pts2 = [(sx * 2.0, 40.0, -4.0), (sx * 4.0, 46.0, 0.0), (sx * 4.0, 50.0, 6.0)]
            for p0, p1 in zip(pts2, pts2[1:]):
                rod(m, hd, p0, p1, 1, hornf, extend=0.3, t2=2)
        for i in range(10):                                                              # pale mane
            ang = math.radians(-120 + i * 24)
            spike(m, hd, (3.0 * math.sin(ang), 38.0, -2.0 + 2.0 * math.cos(ang)), (math.sin(ang), 0.2, 0.8), 2.0, 6.0,
                  FUR, tip=0.9)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab = m.bone(nm, bd, (sx * 3.0, 30.0, -2.0))
            rod(m, ab, (sx * 3.0, 30.0, -2.0), (sx * 7.0, 26.0, -6.0), 2, HIDE, extend=0.4)
            for j in range(3):
                spike(m, ab, (sx * 7.0 + (j - 1) * 0.9, 25.6, -6.6), (0, -0.6, -1), 0.8, 2.0, solid(P, "claw"), tip=0.8)
        for side in (1, -1):
            wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 30.0, 2.0))
            bat_wing(m, wb, (side * 3.0, 30.0, 2.0), 22.0, 14.0, 4, metal(P, "pink_dark"), HIDE, side=side, sweep=20)
        return m

    return build
