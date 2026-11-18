"""Shared builder for Gabumon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): a stocky
yellow reptile wearing a striped wolf pelt over its head and back, a single ridged horn, red eyes, a toothy grin,
pelt paws with red-tipped claws and a red-and-blue emblem on its belly. Looks: "base" (white pelt, blue stripes),
"black" (dark brown pelt, cream stripes, grey hide), "x" (the X-Antibody: a big round yellow beast with a lavender
striped pelt, a long golden horn and huge white claws). Shiny = the "Black" colours (Black's shiny = the classic).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import fur, skin, solid
from _route import pal, tone

BASE = {"hide": (250, 214, 40), "hide_dark": (200, 150, 10), "pelt": (220, 226, 250), "pelt_dark": (150, 160, 210),
        "stripe": (50, 70, 170), "horn": (240, 220, 140), "horn_dark": (40, 40, 40), "eye": (200, 30, 40),
        "white": (250, 250, 250), "mouth": (150, 30, 40), "tooth": (250, 250, 246), "claw": (200, 30, 60),
        "emblem": (220, 40, 100), "emblem2": (60, 120, 200)}
BLACK = {"hide": (150, 150, 156), "hide_dark": (90, 90, 96), "pelt": (90, 70, 60), "pelt_dark": (50, 40, 34),
         "stripe": (230, 220, 200), "eye": (240, 140, 30), "claw": (70, 60, 60), "emblem": (250, 230, 150),
         "emblem2": (200, 180, 120)}
XLOOK = {"pelt": (180, 160, 230), "pelt_dark": (120, 100, 180), "stripe": (90, 70, 160), "horn": (230, 190, 90),
         "claw": (246, 246, 246), "emblem": (70, 70, 200), "emblem2": (230, 50, 70), "eye": (200, 30, 40)}


def make(name, look="base"):
    base = dict(BASE, **(BLACK if look == "black" else XLOOK if look == "x" else {}))
    shiny = dict(BASE, **(BLACK if look != "black" else {}))
    if look == "x":
        shiny = dict(base, **{"pelt": (100, 80, 70), "pelt_dark": (60, 46, 40), "stripe": (230, 220, 200)})

    def P(v):
        return pal(base, shiny, v)

    HIDE = skin(P, "hide", dark="hide_dark")
    PELT0 = fur(P, "pelt", "pelt_dark", length=1.0, density=2.2)

    def peltf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if abs(((x * 0.6 + y * 0.35 + z * 0.2) % 3.2) - 1.6) < 0.45:
            return tone(p["stripe"], face), None
        return PELT0(x, y, z, face, variant, box=box, **k)

    def bellyf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            r = math.hypot(x, y - cy)
            if r < er * 0.45:
                return tone(p["emblem2"], face), None
            if r < er:
                return tone(p["emblem"], face), None
        return HIDE(x, y, z, face, variant, box=box, **k)

    def build():
        nonlocal cy, er
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        if look == "x":                                                        # round yellow beast
            cy, er = 13.0, 4.0
            bd = m.bone("body", top, (0, 6, 0))
            ball(m, bd, (0, 13.0, 0), 9.0, bellyf, layers=6, ry=10.0)
            m.round_box(bd, 0, 4.0, 9.0, 6.0, 10.0, 24.0, peltf, cut=3)       # pelt over the back
            hd = m.bone("head", bd, (0, 20, -3))
            m.round_box(hd, 0, -6.4, 3.0, 2.4, 15.6, 19.6, HIDE, cut=1)       # muzzle
            m.box(hd, -0.8, 18.6, -9.0, 0.8, 19.6, -8.7, solid(P, "horn_dark"))
            for sx in (-1, 1):
                m.box(hd, min(sx * 1.6, sx * 3.0), 20.4, -6.2, max(sx * 1.6, sx * 3.0), 21.2, -5.9, solid(P, "eye"))
            spike(m, hd, (0, 25.0, -2.0), (0, 1, -0.15), 2.4, 10.0, solid(P, "horn"), tip=1.0)
            for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
                ab = m.bone(nm, bd, (sx * 8.0, 14.0, -1.0))
                rod(m, ab, (sx * 8.0, 14.0, -1.0), (sx * 10.0, 6.0, -3.0), 3, peltf, extend=0.6)
                for j in range(3):
                    spike(m, ab, (sx * 10.0 + (j - 1) * 1.2, 5.0, -4.0), (sx * 0.2, -0.6, -1), 1.0, 5.0,
                          solid(P, "claw"), tip=0.8)
            for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
                lg = m.bone(nm, top, (sx * 4.0, 5.0, 0))
                m.round_box(lg, sx * 4.4, -1.0, 2.6, 3.2, 0.0, 6.0, HIDE, cut=1)
                for j in range(3):
                    spike(m, lg, (sx * 4.4 + (j - 1) * 1.4, 0.6, -4.0), (0, -0.2, -1), 0.8, 2.0, solid(P, "claw"),
                          tip=0.8)
            tb = m.bone("tail", bd, (0, 10, 8))
            rod(m, tb, (0, 10.0, 8.0), (2.0, 16.0, 14.0), 3, peltf, extend=0.4, t2=4)
            return m
        cy, er = 14.0, 2.2                                                     # the classic little Gabumon
        bd = m.bone("body", top, (0, 8, 0))
        m.round_box(bd, 0, 0.4, 4.6, 3.6, 7.0, 19.0, bellyf, cut=2)
        m.round_box(bd, 0, 2.4, 5.0, 2.2, 9.0, 21.0, peltf, cut=1)             # pelt down the back
        hd = m.bone("head", bd, (0, 20, -1))
        m.round_box(hd, 0, -0.6, 4.8, 4.2, 18.0, 25.6, peltf, cut=2)           # pelt hood
        m.round_box(hd, 0, -5.8, 3.0, 2.4, 17.6, 21.6, peltf, cut=1)           # wolf snout
        m.round_box(hd, 0, -4.6, 3.4, 2.0, 15.0, 18.0, HIDE, cut=1)            # yellow jaw
        m.box(hd, -2.6, 17.6, -6.7, 2.6, 18.2, -6.3, solid(P, "mouth"))
        for j in range(6):
            x = -2.2 + j * 0.88
            spike(m, hd, (x, 17.9, -6.2), (0, -1, 0), 0.6, 1.2, solid(P, "tooth"))
        m.box(hd, -0.8, 20.8, -8.6, 0.8, 21.8, -8.2, solid(P, "horn_dark"))      # nose
        for sx in (-1, 1):
            m.round_box(hd, sx * 2.4, -4.6, 0.9, 0.4, 21.6, 23.2, solid(P, "white"), cut=0)
            m.box(hd, min(sx * 2.0, sx * 2.8), 22.0, -5.1, max(sx * 2.0, sx * 2.8), 22.8, -4.9, solid(P, "eye"))
            ear = (sx * 6.0, 25.0, 4.0)                                         # pelt ears swept back
            spike(m, hd, (sx * 3.6, 24.0, 1.0), (sx * 0.8, 0.2, 1.0), 2.0, 5.0, peltf, tip=1.0)
        spike(m, hd, (0, 25.4, -1.4), (0, 1, -0.3), 2.0, 7.0, solid(P, "horn"), tip=1.0)   # ridged horn
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab = m.bone(nm, bd, (sx * 4.4, 17.0, -1.0))
            rod(m, ab, (sx * 4.4, 17.0, -1.0), (sx * 5.6, 10.0, -3.0), 2, peltf, extend=0.4, t2=3)
            m.round_box(ab, sx * 5.8, -3.4, 1.8, 1.8, 7.4, 10.4, HIDE, cut=1)
            for j in range(3):
                spike(m, ab, (sx * 5.8 + (j - 1) * 1.0, 7.6, -4.8), (0, -0.4, -1), 0.8, 2.6, solid(P, "claw"),
                      tip=0.8)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, top, (sx * 2.6, 8.0, 0))
            rod(m, lg, (sx * 2.6, 8.0, 0), (sx * 2.8, 2.0, -0.6), 3, HIDE, extend=0.4)
            m.round_box(lg, sx * 2.8, -1.6, 2.0, 2.6, 0.0, 2.6, peltf, cut=1)
            for j in range(3):
                spike(m, lg, (sx * 2.8 + (j - 1) * 1.1, 0.4, -4.2), (0, 0, -1), 0.8, 1.4, solid(P, "white"))
        tb = m.bone("tail", bd, (0, 9, 4))
        rod(m, tb, (0, 9.0, 4.0), (0, 6.0, 11.0), 2, peltf, extend=0.4, t2=3)
        return m

    cy, er = 0.0, 0.0
    return build
