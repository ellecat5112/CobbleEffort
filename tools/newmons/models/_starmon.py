"""Shared builder for Starmon and Starmon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): a living star of a sheriff: its whole head-body a big metal five-pointed star with a black face and a
red gem, blue boxing gloves studded with spikes and stars on segmented arms, chunky red-and-blue boots, and a long
golden chain-scarf streaming behind. X-Antibody: a pale-lilac star with layered points, red-and-blue star-spangled
gloves and boots, and a long yellow ribbon scarf. Shiny: gold / dark.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import armour, leather, metal, solid
from _route import pal, tone


def make(name, x=False):
    base = {"star": (210, 214, 226) if not x else (190, 180, 240), "star_dark": (110, 114, 130) if not x else (120, 110, 190),
            "black": (24, 22, 28), "red": (210, 40, 40), "red_dark": (120, 14, 14), "blue": (40, 60, 170),
            "blue_dark": (16, 24, 100), "gold": (250, 210, 60), "eye": (90, 160, 250), "steel": (190, 194, 206)}
    shiny = {"star": (250, 220, 90), "star_dark": (180, 140, 30)}

    def P(v):
        return pal(base, shiny, v)

    STAR = metal(P, "star", dark="star_dark")

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 10, 0))
        ball(m, bd, (0, 22.0, 0), 5.0, STAR, layers=4, squash=0.6)                       # star head-body
        for j in range(5):
            ang = math.radians(90 + j * 72)
            spike(m, bd, (0, 22.0, 0), (math.cos(ang), math.sin(ang), 0), 4.4, 9.0, STAR, tip=0.8)
            if x:
                ang2 = ang + math.radians(36)
                spike(m, bd, (0, 22.0, 1.0), (math.cos(ang2), math.sin(ang2), 0), 3.0, 6.0, STAR, tip=0.8)
        m.round_box(bd, 0, -2.6, 2.8, 0.6, 19.0, 24.0, solid(P, "black"), cut=0)            # black face
        for sx in (-1, 1):
            m.box(bd, sx * 1.2 - 0.6, 21.6, -3.3, sx * 1.2 + 0.6, 22.8, -3.1, solid(P, "eye", glow=True))
        m.box(bd, -0.6, 26.0, -3.0, 0.6, 27.4, -2.6, solid(P, "red"))
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # segmented arms + gloves
            ab = m.bone(nm, bd, (sx * 4.0, 19.0, 0))
            rod(m, ab, (sx * 4.0, 19.0, 0), (sx * 9.0, 14.0, -1.0), 1, metal(P, "steel"), extend=0.2, t2=2)
            ball(m, ab, (sx * 10.4, 13.0, -1.4), 2.6, leather(P, "blue" if not x else "red", "blue_dark"), layers=3)
            for j in range(3):
                spike(m, ab, (sx * 10.4 + (j - 1) * 1.4, 15.4, -1.4), (0, 1, 0), 0.8, 1.4, metal(P, "steel"), tip=0.8)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, top, (sx * 2.2, 10.0, 0))
            rod(m, lg, (sx * 2.2, 13.0, 0), (sx * 2.6, 5.0, 0), 1, metal(P, "steel"), extend=0.2, t2=2)
            m.round_box(lg, sx * 2.6, -0.8, 2.2, 3.0, 0.0, 5.0, armour(P, "red" if sx > 0 else "blue",
                        "red_dark" if sx > 0 else "blue_dark"), cut=1)
        pts = [(2.0, 26.0, 2.0), (8.0, 24.0, 6.0), (12.0, 18.0, 8.0), (14.0, 12.0, 6.0)]   # scarf / chain
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, bd, p0, p1, 1 if not x else 2, solid(P, "gold"), extend=0.2, t2=2 if not x else 1)
        return m

    return build
