"""Shared builder for Pteranomon and Pteranomon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art
on wikimon.net): the Armor Digimon of sincerity: a mechanical pteranodon of blue-steel plates: a long beaked head with
a swept crest and a toothy jaw, yellow eyes, great straight jet wings marked with red, missile racks under each wing,
jointed legs with red talons. X-Antibody: a dark navy stealth jet of angular plates with teal running lights, swept
delta wings, a twin-boom tail and two blue jet thrusters burning under it. Shiny: gunmetal and orange.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, slab_z
from _digidetail import armour, metal, solid
from _route import pal, tone

BASE = {"plate": (110, 120, 170), "plate_dark": (50, 56, 100), "red": (210, 40, 40), "steel": (200, 204, 216),
        "steel_dark": (100, 104, 120), "eye": (250, 210, 40), "mouth": (180, 60, 80), "tooth": (250, 250, 240),
        "talon": (210, 40, 40), "navy": (50, 54, 90), "navy_dark": (18, 20, 40), "teal": (90, 230, 230),
        "jet": (130, 210, 255, 200)}
SHINY = {"plate": (120, 124, 132), "plate_dark": (56, 58, 66), "red": (240, 140, 30), "navy": (90, 90, 100),
         "navy_dark": (40, 40, 48), "teal": (250, 160, 40)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    key, dark = ("navy", "navy_dark") if x else ("plate", "plate_dark")
    PLATE = armour(P, key, dark, trim="teal" if x else None, trim_w=0.2)

    def wingf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if not x and abs(xx) > 22 and face in ("up", "down"):
            return tone(p["red"], face), None
        if x and face in ("up", "down") and abs(z - (abs(xx) * 0.4 - 4)) < 0.3:
            return tone(p["teal"], face), p["teal"]
        return PLATE(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 16, 0))
        for i in range(6):                                                               # fuselage
            t = (i + 0.5) / 6
            r = 4.6 * math.sin(math.pi * (0.2 + 0.7 * t)) + 1.0
            slab_z(m, bd, 0, 18.0, -10.0 + i * 3.6, -10.0 + (i + 1) * 3.6 + 0.2, r, r * 0.9, PLATE)
        wb = m.bone("wings", bd, (0, 20, -2))
        for sx in (-1, 1):
            if x:                                                                        # swept delta wings
                for j in range(4):
                    x0, x1 = sorted((sx * 4.0, sx * (28.0 - j * 5.0)))
                    m.box(wb, x0, 19.4, -4.0 + j * 4.0, x1, 20.6, 0.0 + j * 4.0, wingf,
                          rotation=(0, sx * 25, 0), pivot=(sx * 4.0, 20.0, -2.0 + j * 4.0))
            else:                                                                        # long straight jet wings
                x0, x1 = sorted((sx * 4.0, sx * 30.0))
                m.box(wb, x0, 19.4, -3.0, x1, 20.6, 3.0, wingf, rotation=(0, sx * 8, sx * 6), pivot=(sx * 4.0, 20.0, 0))
            for j in range(3 if not x else 0):                                           # missile racks
                c = (sx * (10.0 + j * 2.4), 18.0, -2.0)
                rod(m, wb, (c[0], c[1], c[2] + 5.0), c, 1, metal(P, "steel", dark="steel_dark"), extend=0.2, t2=2)
                spike(m, wb, c, (0, 0, -1), 1.0, 1.6, solid(P, "red"), tip=0.8)
        nk = m.bone("neck", bd, (0, 20, -10))
        rod(m, nk, (0, 20.0, -10.0), (0, 25.0, -14.0), 3, PLATE, extend=0.4)
        hd = m.bone("head", nk, (0, 25, -14))
        m.round_box(hd, 0, -15.0, 2.2, 2.6, 23.6, 27.4, PLATE, cut=1)
        spike(m, hd, (0, 25.6, -17.0), (0, -0.1, -1), 2.4, 14.0, PLATE, tip=0.8)          # long beak
        jb = m.bone("jaw", hd, (0, 24, -16))
        spike(m, jb, (0, 23.6, -17.0), (0, -0.25, -1), 1.6, 10.0, PLATE, tip=0.8)
        for j in range(4):
            spike(m, hd, (0, 24.6, -19.0 - j * 2.0), (0, -1, 0), 0.8, 1.0, solid(P, "tooth"), tip=0.8)
        spike(m, hd, (0, 26.6, -13.0), (0, 0.3, 1), 1.6, 10.0, PLATE, tip=0.8)              # swept crest
        for sx in (-1, 1):
            m.box(hd, min(sx * 2.1, sx * 2.3), 25.6, -17.0, max(sx * 2.1, sx * 2.3), 26.6, -15.6,
                  solid(P, "eye", glow=True))
        if x:                                                                            # twin booms + jets
            for sx in (-1, 1):
                rod(m, bd, (sx * 3.0, 18.0, 8.0), (sx * 4.0, 22.0, 20.0), 2, PLATE, extend=0.3)
                m.box(bd, sx * 4.0 - 0.4, 20.0, 18.0, sx * 4.0 + 0.4, 27.0, 22.0, PLATE)
                rod(m, bd, (sx * 3.0, 15.0, 2.0), (sx * 3.0, 15.0, 10.0), 3, metal(P, "steel_dark"), extend=0.3)
                spike(m, bd, (sx * 3.0, 14.0, 4.0), (0, -1, 0.3), 2.4, 7.0, solid(P, "jet", glow=True), tip=0.8)
        else:
            rod(m, bd, (0, 18.0, 10.0), (0, 18.0, 18.0), 2, PLATE, extend=0.3)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, bd, (sx * 3.0, 14.0, 2.0))
            rod(m, lg, (sx * 3.0, 14.0, 2.0), (sx * 3.4, 8.0, -1.0), 2, metal(P, "steel", dark="steel_dark"), extend=0.3)
            rod(m, lg, (sx * 3.4, 8.0, -1.0), (sx * 3.4, 3.0, 1.0), 1, metal(P, "steel", dark="steel_dark"), extend=0.3)
            for f in range(3):
                spike(m, lg, (sx * 3.4 + (f - 1) * 1.0, 2.6, 0.6), ((f - 1) * 0.3, -1, -0.6), 0.8, 2.6,
                      solid(P, "talon"), tip=0.8)
        return m

    return build
