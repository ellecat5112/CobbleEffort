"""Shared builder for Renamon and Renamon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): a slender upright golden fox: a white chest ruff, a pointed snout, tall ears, sharp blue eyes, long
purple sleeve-gloves with a yin-yang mark on each shoulder, golden fur with white tips on its legs and a long bushy
white-tipped tail; a ring of glowing leaves (Koyousetsu) circles its raised paw. X-Antibody: the fur deepens to amber
with flame-like crimson markings and white swirling yin-yang sigils, the gloves turn black-violet with claws, and two
ghostly fox spirits wreathe it. Shiny: silver-white.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import humanoid
from _digidetail import fabric, fur, solid
from _route import pal, tone


def make(name, x=False):
    base = {"gold": (250, 200, 50) if not x else (240, 160, 40), "gold_dark": (200, 140, 20) if not x else (170, 90, 10),
            "white": (252, 250, 244), "white_dark": (200, 196, 186), "purple": (120, 70, 170) if not x else (50, 30, 70),
            "purple_dark": (60, 30, 100) if not x else (20, 10, 30), "eye": (60, 120, 220), "black": (30, 26, 30),
            "mark": (30, 26, 30) if not x else (210, 40, 40), "leaf": (90, 170, 70, 200), "spirit": (170, 140, 250, 150)}
    shiny = {"gold": (220, 220, 230), "gold_dark": (150, 150, 170)}

    def P(v):
        return pal(base, shiny, v)

    FUR = fur(P, "gold", "gold_dark", length=1.2)

    def furf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north" and abs(xx) < 3.0 and 38.0 < y < 50.0:
            return fur(P, "white", "white_dark", length=1.0)(xx, y, z, face, variant, box=box, **k)
        if face in ("north", "east", "west") and 44.0 < y < 50.0 and abs(abs(xx) - 6.6) < 1.4:
            d = math.hypot(abs(xx) - 6.6, y - 47.0)
            if d < 1.2 and (abs(xx) - 6.6) * (y - 47.0) > 0:
                return tone(p["mark"], face), None
        if y < 10.0:
            return fur(P, "white", "white_dark", length=1.0)(xx, y, z, face, variant, box=box, **k)
        if x and abs(math.sin(y * 0.7 + xx * 0.5)) > 0.94:
            return tone(p["mark"], face), None
        return FUR(xx, y, z, face, variant, box=box, **k)

    GLOVE = fabric(P, "purple", "purple_dark", axis="y", period=2.0)

    def tailf(xx, y, z, face, variant, box=None, **k):
        if z > 18.0:
            return fur(P, "white", "white_dark", length=1.0)(xx, y, z, face, variant, box=box, **k)
        return FUR(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        mats = {"skin": furf, "forearm": GLOVE, "hand": GLOVE, "finger": GLOVE, "talon": solid(P, "black"),
                "claw": solid(P, "white")}
        a = humanoid(m, mats, bulk=0.75, arm_bulk=0.75, leg_bulk=0.85, claws=x, talons=True, digitigrade=True,
                     name=name)
        bd = a["body"]
        m.round_box(bd, 0, -1.0, 4.4, 3.0, 46.0, 53.0, fur(P, "white", "white_dark", length=1.4), cut=1)   # ruff
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 2.4, 2.6, 54.0, 60.0, furf, cut=1)
        m.round_box(hd, 0, -3.8, 1.2, 1.4, 54.4, 57.0, fur(P, "white", "white_dark", length=0.8), cut=0)  # snout
        m.box(hd, -0.5, 56.4, -5.3, 0.5, 57.0, -5.1, solid(P, "black"))
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.8, sx * 2.0), 57.6, -2.8, max(sx * 0.8, sx * 2.0), 58.4, -2.6, solid(P, "eye"))
            spike(m, hd, (sx * 1.8, 60.0, 0), (sx * 0.3, 1, 0.1), 1.8, 7.0, FUR, tip=0.8)   # tall ears
        tl = m.bone("tail", bd, (0, 31, 3))                                              # bushy tail
        pts = [(0, 31.0, 3.0), (2.0, 24.0, 10.0), (5.0, 22.0, 17.0), (8.0, 26.0, 22.0)]
        for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, tl, p0, p1, 4 + (1 if i == 1 else 0), tailf, extend=0.8)
        spike(m, tl, pts[-1], (0.6, 0.6, 0.4), 2.6, 4.0, tailf, tip=0.8)
        h = a["arm_left"]["hand"]                                                        # ring of glowing leaves
        for i in range(6):
            ang = 2 * math.pi * i / 6
            c = (h[0] + 2.0, h[1] + 10.0 + 7.0 * math.sin(ang), h[2] + 7.0 * math.cos(ang))
            m.box(a["arm_left"]["bone"], c[0] - 0.3, c[1] - 1.4, c[2] - 1.0, c[0] + 0.3, c[1] + 1.4, c[2] + 1.0,
                  solid(P, "leaf", glow=True))
        if x:                                                                            # ghostly fox spirits
            for sx in (-1, 1):
                sb = m.bone("spirit_left" if sx > 0 else "spirit_right", bd, (sx * 12.0, 50.0, 4.0))
                m.round_box(sb, sx * 12.0, 4.0, 2.0, 3.0, 48.0, 52.0, solid(P, "spirit", glow=True), cut=1)
                spike(m, sb, (sx * 12.0, 50.0, 1.0), (0, -0.2, -1), 1.4, 3.0, solid(P, "spirit", glow=True), tip=0.8)
                for e in (-1, 1):
                    spike(m, sb, (sx * 12.0 + e * 1.2, 52.0, 4.0), (e * 0.3, 1, 0), 1.0, 2.6,
                          solid(P, "spirit", glow=True), tip=0.8)
                rod(m, sb, (sx * 12.0, 50.0, 7.0), (sx * 16.0, 44.0, 14.0), 2, solid(P, "spirit", glow=True), extend=0.4)
        return m

    return build
