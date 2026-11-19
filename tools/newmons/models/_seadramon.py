"""Shared builder for Seadramon and Seadramon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the sea serpent: a long coiling teal body with a pale belly and red stripe markings, a golden-yellow
armoured dragon head with a swept horn and fins, blue eyes, and a red leaf-shaped tail fin. X-Antibody: a deep-blue
serpent with flowing red streaks and red-edged dorsal fins, a huge golden finned head-crest sweeping back, and a
purple-lipped toothy maw. Shiny: crimson / emerald.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digidetail import armour, scales, skin, solid
from _route import pal, tone


def make(name, x=False, colours=None, shiny_colours=None):
    base = {"teal": (40, 140, 160) if not x else (40, 80, 200), "teal_dark": (14, 80, 100) if not x else (14, 30, 120),
            "belly": (230, 236, 200) if not x else (150, 200, 240), "red": (210, 40, 40), "gold": (250, 200, 50),
            "gold_dark": (200, 120, 20), "eye": (40, 80, 200) if not x else (250, 60, 60), "mouth": (130, 50, 140),
            "tooth": (250, 250, 240)}
    shiny = {"teal": (180, 40, 60) if not x else (40, 160, 90), "teal_dark": (100, 14, 24) if not x else (14, 90, 40)}
    base.update(colours or {})
    shiny.update(shiny_colours or {})

    def P(v):
        return pal(base, shiny, v)

    def bodyf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "down":
            return skin(P, "belly", dark="teal_dark", var=0.02)(xx, y, z, face, variant, box=box, **k)
        if abs(math.sin(z * 0.5 + y * 0.4)) > (0.93 if not x else 0.85) and face in ("east", "west", "up"):
            return tone(p["red"], face), None
        return scales(P, "teal", "teal_dark", size=1.4)(xx, y, z, face, variant, box=box, **k)

    HELM = armour(P, "gold", "gold_dark")

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 10, 0))
        pts = [(0, 26.0, -8.0), (0, 18.0, -4.0), (4.0, 12.0, 2.0), (8.0, 14.0, 8.0), (6.0, 20.0, 12.0), (0, 22.0, 12.0),
               (-4.0, 18.0, 10.0), (-4.0, 12.0, 6.0), (0, 8.0, 4.0), (4.0, 6.0, 10.0)]
        for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
            b = m.bone(f"coil_{i}", bd, p0)
            rod(m, b, p0, p1, max(2, 5 - i // 3), bodyf, extend=0.8)
            if x and i < 6:
                spike(m, b, (p0[0], p0[1] + 2.0, p0[2]), (0, 1, 0.5), 1.0, 3.0, solid(P, "red"), tip=0.8)
        tl = m.bone("tail_fin", "coil_8", pts[-1])
        m.box(tl, pts[-1][0] - 0.3, pts[-1][1] - 2.0, pts[-1][2], pts[-1][0] + 0.3, pts[-1][1] + 2.0, pts[-1][2] + 6.0,
              solid(P, "red"))
        hd = m.bone("head", bd, pts[0])
        m.round_box(hd, 0, -12.0, 3.0, 4.0, 24.0, 30.0, HELM, cut=1)                    # golden head
        m.round_box(hd, 0, -17.0, 2.0, 2.0, 24.0, 27.0, HELM, cut=1)                    # snout
        m.box(hd, -1.8, 24.0, -19.0, 1.8, 25.0, -12.0, solid(P, "mouth"))
        jb = m.bone("jaw", hd, (0, 24, -10))
        m.round_box(jb, 0, -15.0, 1.8, 3.0, 22.4, 24.0, skin(P, "belly", dark="teal_dark"), cut=0)
        for j in range(4):
            for sx in (-1, 1):
                spike(m, hd, (sx * 1.6, 24.0, -18.0 + j * 1.6), (0, -1, 0), 0.8, 1.2, solid(P, "tooth"), tip=0.8)
        for sx in (-1, 1):
            m.box(hd, min(sx * 2.9, sx * 3.2), 27.6, -13.0, max(sx * 2.9, sx * 3.2), 28.6, -11.6, solid(P, "eye"))
            spike(m, hd, (sx * 2.8, 28.0, -9.0), (sx * 0.6, 0.2, 1), 1.4, 5.0 if not x else 9.0, HELM, tip=0.8)   # fins
        spike(m, hd, (0, 30.0, -10.0), (0, 0.6, 1), 1.6, 6.0 if not x else 12.0, HELM, tip=0.8)  # swept horn
        if not x:
            m.box(hd, -0.3, 30.0, -12.0, 0.3, 36.0, -8.0, solid(P, "red"), rotation=(-20, 0, 0), pivot=(0, 30.0, -10.0))
        return m

    return build
