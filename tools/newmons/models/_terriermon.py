"""Shared builder for Terriermon, Terriermon (X-Antibody) and Terriermon Assistant (CobbleEffort: Digital; hand-built
after the official art on wikimon.net): Lopmon's twin: a small round cream bunny-dog with a single horn, dot eyes, a
cat mouth, green feet, and two huge long ears that sweep out and up like wings, banded green and splitting into three
green fingers at the tips. X-Antibody: much longer ears striped green like a tiger, a gold ornament with a green gem,
and a shaggy golden mane. Assistant: an open white lab coat with a black tie and a wink. Shiny: pale pink and blue."""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import fabric, fur, gem, skin, solid, strands
from _route import pal, tone

BASE = {"cream": (248, 246, 222), "cream_dark": (204, 200, 160), "green": (150, 200, 100), "green_dark": (80, 140, 50),
        "eye": (24, 20, 20), "gold": (240, 200, 60), "gold_light": (255, 240, 170), "gem": (40, 170, 90),
        "gem_light": (150, 250, 180), "mane": (246, 220, 110), "mane_dark": (200, 160, 50), "coat": (250, 252, 255),
        "coat_dark": (196, 210, 230), "tie": (30, 30, 36), "mouth": (200, 70, 80)}
SHINY = {"cream": (250, 220, 230), "cream_dark": (210, 160, 180), "green": (120, 170, 230), "green_dark": (60, 100, 170)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, look="base"):
    x = look == "x"
    FUR = fur(P, "cream", "cream_dark", length=0.6)

    def earf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if x and (abs(xx) * 0.9 + y * 0.3) % 3.0 < 0.8:
            return tone(p["green"], face), None
        if not x and (abs(xx) % 5.0) < 1.4 and abs(xx) > 6.0:
            return tone(p["green"], face), None
        return FUR(xx, y, z, face, variant, box=box, **k)

    def bodyf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                if look == "assistant" and sx < 0:
                    if abs(y - 10.4) < 0.25 and abs(xx - sx * 1.4) < 0.7:
                        return tone(p["eye"], face), None
                elif math.hypot(xx - sx * 1.4, y - 10.4) < 0.6:
                    return tone(p["eye"], face), None
            if abs(y - 8.8) < 0.3 and abs(xx) < 0.8:
                return tone(p["mouth"], face), None
        return FUR(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 3, 0))
        ball(m, bd, (0, 8.0, 0), 4.6, bodyf, layers=4, squash=1.1)
        spike(m, bd, (0, 12.6, -1.0), (0, 1, -0.2), 1.2, 2.4, FUR, tip=0.8)
        L = 15.0 if not x else 24.0
        for side, nm in ((1, "wing_left"), (-1, "wing_right")):                     # huge sweeping ears
            eb = m.bone(nm, bd, (side * 2.0, 11.0, 0))
            pts = [(side * 2.0, 11.6, 0), (side * L * 0.4, 16.0, 1.0), (side * L * 0.75, 16.6, 1.0),
                   (side * L, 13.0, 0.0)]
            for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
                rod(m, eb, p0, p1, 2, earf, extend=0.6, t2=4 - j * 0.6)
            for j in range(3):                                                       # three green fingers
                spike(m, eb, pts[-1], (side * 0.6, -1 + j * 0.6, 0), 1.0, 3.4, skin(P, "green", dark="green_dark"),
                      tip=0.8)
            if x:
                m.round_box(eb, pts[1][0], 1.0, 1.6, 1.4, pts[1][1] - 1.4, pts[1][1] + 1.4, gem(P, "gold", "gold_light"),
                            cut=0)
                if side > 0:
                    m.round_box(eb, pts[1][0], 0.0, 0.9, 1.0, pts[1][1] - 0.8, pts[1][1] + 0.8, gem(P, "gem", "gem_light"),
                                cut=0)
        if x:                                                                        # shaggy golden mane
            for j in range(9):
                ang = (j - 4) * 0.4
                spike(m, bd, (math.sin(ang) * 3.0, 12.0, 1.0), (math.sin(ang) * 1.2, 0.6, 0.6), 1.4, 3.6,
                      strands(P, "mane", "mane_dark"), tip=0.8)
        if look == "assistant":                                                      # open lab coat + tie
            for sx in (-1, 1):
                m.box(bd, min(sx * 1.6, sx * 5.0), 2.0, -4.8, max(sx * 1.6, sx * 5.0), 10.0, -3.0,
                      fabric(P, "coat", "coat_dark"), rotation=(0, 0, sx * 6), pivot=(sx * 3.0, 10.0, -4.0))
            m.box(bd, -5.0, 2.0, -3.0, 5.0, 10.0, 3.6, fabric(P, "coat", "coat_dark"))
            m.box(bd, -0.5, 4.4, -4.9, 0.5, 8.2, -4.4, solid(P, "tie"))
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab = m.bone(nm, bd, (sx * 3.6, 8.0, -1.0))
            spike(m, ab, (sx * 3.6, 8.0, -1.0), (sx * 0.8, 0.2, -0.5), 1.2, 2.4, FUR, tip=0.8)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, top, (sx * 1.6, 3.0, 0))
            m.round_box(lg, sx * 1.8, -1.0, 1.2, 1.8, 0.0, 3.0, FUR, cut=0)
            m.box(lg, sx * 1.8 - 1.2, 0.0, -3.4, sx * 1.8 + 1.2, 1.2, -1.6, skin(P, "green", dark="green_dark"))
        return m

    return build
