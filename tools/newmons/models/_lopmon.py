"""Shared builder for Lopmon and Lopmon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the brown bunny: a small round brown rabbit with a pink-cream belly, dot eyes, a tiny horn, and two
huge long ears that sweep out like wings, pink-striped and splitting into three pink fingers at the tips. X-Antibody:
much longer ears with darker brown tiger markings, gold ornaments near the tips, and fluffy cream puffs on its
shoulders. Shiny: grey-blue.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import fur, gem, skin, solid
from _route import pal, tone

BASE = {"brown": (180, 140, 120), "brown_dark": (110, 80, 66), "pink": (250, 190, 200), "pink_dark": (220, 130, 150),
        "cream": (250, 240, 210), "cream_dark": (210, 190, 150), "eye": (24, 20, 20), "gold": (240, 200, 60),
        "gold_light": (255, 240, 170), "horn": (230, 210, 200), "stripe": (120, 90, 70)}
SHINY = {"brown": (150, 160, 190), "brown_dark": (90, 100, 130)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    FUR = fur(P, "brown", "brown_dark", length=0.6)

    def earf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if x and (abs(xx) * 0.9 + y * 0.3) % 3.0 < 0.7:
            return tone(p["stripe"], face), None
        if not x and face in ("north", "up") and (abs(xx) % 4.0) < 1.2:
            return tone(p["pink"], face), None
        return FUR(xx, y, z, face, variant, box=box, **k)

    def bodyf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                if math.hypot(xx - sx * 1.4, y - 10.4) < 0.6:
                    return tone(p["eye"], face), None
            if y < 8.0 and abs(xx) < 2.4:
                return tone(p["pink"], face), None
        return FUR(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 3, 0))
        ball(m, bd, (0, 8.0, 0), 4.6, bodyf, layers=4, squash=1.1)
        spike(m, bd, (0, 12.6, -1.6), (0, 1, -0.4), 1.0, 1.6, solid(P, "horn"), tip=0.8)
        L = 14.0 if not x else 22.0
        for side, nm in ((1, "wing_left"), (-1, "wing_right")):                     # huge sweeping ears
            eb = m.bone(nm, bd, (side * 2.0, 11.0, 0))
            pts = [(side * 2.0, 11.0, 0), (side * L * 0.45, 14.0, 1.0), (side * L * 0.8, 10.0, 1.0), (side * L, 4.0, 0.0)]
            for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
                rod(m, eb, p0, p1, 2, earf, extend=0.6, t2=4 - j)
            for j in range(3):                                                       # three pink fingers
                spike(m, eb, pts[-1], (side * 0.3 + (j - 1) * 0.4, -1, 0), 1.0, 3.0, skin(P, "pink", dark="pink_dark"),
                      tip=0.8)
            if x:
                m.round_box(eb, pts[-2][0], 1.0, 1.2, 1.2, pts[-2][1] - 1.0, pts[-2][1] + 1.0, gem(P, "gold", "gold_light"),
                            cut=0)
                m.round_box(bd, side * 4.6, 0, 1.8, 1.8, 9.0, 12.6, fur(P, "cream", "cream_dark"), cut=1)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab = m.bone(nm, bd, (sx * 3.6, 8.0, -1.0))
            spike(m, ab, (sx * 3.6, 8.0, -1.0), (sx * 0.6, -0.6, -0.5), 1.0, 1.8, FUR, tip=0.8)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, top, (sx * 1.6, 3.0, 0))
            m.round_box(lg, sx * 1.8, -1.0, 1.2, 1.8, 2.0, 4.0, FUR, cut=0)
        return m

    return build
