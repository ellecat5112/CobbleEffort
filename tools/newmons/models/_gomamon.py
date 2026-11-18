"""Shared builder for Gomamon and Gomamon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): a cheerful white seal-pup with violet stripe markings, big green eyes, a spiky orange mohawk (red and
shaggy on the X-Antibody, which also has a shaggy red chest ruff), little fangs, flippered forepaws with black claws
and a striped tail fin. Shiny: golden fur.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digidetail import fur, solid, strands
from _route import pal, tone


def make(name, x=False):
    base = {"white": (246, 246, 252), "white_dark": (190, 194, 214), "violet": (170, 130, 220), "mohawk": (240, 110, 40)
            if not x else (220, 40, 30), "mohawk_dark": (170, 50, 14) if not x else (140, 14, 10), "eye": (70, 180, 80),
            "pupil": (16, 20, 16), "claw": (30, 28, 32), "tooth": (250, 250, 240), "ruff": (230, 50, 30),
            "ruff_dark": (150, 20, 10)}
    shiny = {"white": (250, 230, 170), "white_dark": (210, 180, 110)}

    def P(v):
        return pal(base, shiny, v)

    FUR0 = fur(P, "white", "white_dark", length=0.8, density=2.2)

    def furf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face in ("east", "west", "up") and abs((z * 0.6) % 3.0 - 1.5) < 0.25:
            return tone(p["violet"], face), None
        return FUR0(xx, y, z, face, variant, box=box, **k)

    def headf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                d = math.hypot(xx - sx * 1.8, y - 11.6)
                if d < 0.6:
                    return tone(p["pupil"], face), None
                if d < 1.3:
                    return tone(p["eye"], face), None
                if abs(xx - sx * 3.0) < 0.3 and 10.0 < y < 11.0:
                    return tone(p["violet"], face), None
        return FUR0(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 5, 0))
        m.round_box(bd, 0, 2.0, 4.0, 7.0, 2.0, 9.0, furf, cut=2)                          # seal body lying low
        if x:
            m.round_box(bd, 0, -4.0, 3.6, 2.0, 3.0, 9.0, strands(P, "ruff", "ruff_dark"), cut=1)
        hd = m.bone("head", bd, (0, 9, -4))
        m.round_box(hd, 0, -5.0, 4.0, 3.6, 7.0, 15.0, headf, cut=2)
        for sx in (-1, 1):
            spike(m, hd, (sx * 1.0, 8.4, -8.4), (0, -1, -0.2), 0.6, 1.2, solid(P, "tooth"))
            spike(m, hd, (sx * 3.6, 13.4, -4.0), (sx * 0.8, 0.4, 0.4), 1.6, 3.0 if not x else 5.0, furf, tip=0.8)
        for j in range(6 if not x else 9):                                                  # mohawk
            spike(m, hd, ((j % 3 - 1) * 0.8 if x else 0, 14.6, -6.0 + j * (1.0 if not x else 0.8)), (0, 1, 0.4),
                  1.2, 3.0 + (j % 2), strands(P, "mohawk", "mohawk_dark"), tip=0.8)
        for sx, nm in ((1, "leg_front_left"), (-1, "leg_front_right")):
            lg = m.bone(nm, bd, (sx * 3.6, 5.0, -3.0))
            rod(m, lg, (sx * 3.6, 6.0, -3.0), (sx * 6.6, 1.0, -6.0), 2, furf, extend=0.4)
            for j in range(3):
                spike(m, lg, (sx * 6.6 + (j - 1) * 0.9, 0.6, -6.6), (0, -0.2, -1), 0.8, 2.6, solid(P, "claw"), tip=0.8)
        for sx, nm in ((1, "leg_back_left"), (-1, "leg_back_right")):
            m.bone(nm, bd, (sx * 3.0, 4.0, 6.0))
        tb = m.bone("tail", bd, (0, 4, 9))
        rod(m, tb, (0, 4.0, 9.0), (0, 2.0, 14.0), 2, furf, extend=0.4, t2=2)
        for sx in (-1, 1):
            spike(m, tb, (0, 2.0, 14.0), (sx * 0.8, 0.2, 1), 1.2, 3.0, furf, tip=0.8)
        return m

    return build
