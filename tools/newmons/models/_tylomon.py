"""Shared builder for Tylomon and Tylomon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the Armor Digimon of reliability: a sleek sea-reptile like a shark: a navy-and-white armoured snout with
a toothy jaw, swept blade fins on its back and sides, a pale-blue scaled body and a long whip of a neck-tail curling
up behind. X-Antibody: heavier armour plates in steel blue with gold trim, a serrated spine of blades, glowing cyan
seams and a crested tail fin. Shiny: green."""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, slab_z
from _digidetail import armour, eye, metal, scales, solid
from _route import pal, tone

BASE = {"navy": (40, 60, 150), "navy_dark": (16, 24, 80), "white": (236, 240, 250), "pale": (170, 210, 240),
        "pale_dark": (90, 140, 190), "blade": (210, 220, 240), "blade_dark": (110, 120, 150), "mouth": (160, 20, 40),
        "tooth": (250, 250, 244), "eye": (250, 220, 60), "pupil": (20, 10, 10), "gold": (230, 186, 60),
        "cyan": (100, 240, 250), "steel": (90, 120, 170), "steel_dark": (30, 44, 90)}
SHINY = {"navy": (40, 130, 80), "navy_dark": (14, 70, 40), "pale": (180, 230, 190), "pale_dark": (100, 170, 120),
         "steel": (60, 140, 100), "steel_dark": (20, 80, 50)}


def make(name, x=False):
    def P(v):
        return pal(BASE, SHINY, v)

    ARM = armour(P, "steel" if x else "navy", "steel_dark" if x else "navy_dark", trim="gold" if x else "white",
                 panel=(3.0, 3.0), glow_key="cyan" if x else None)
    BODY = scales(P, "pale", "pale_dark", size=1.2)
    BLADE = metal(P, "blade", dark="blade_dark")

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 8, 0))
        for i in range(8):
            z0 = -12.0 + i * 3.4
            r = max(1.8, 4.6 * math.sin(min(1.0, 0.3 + i / 7 * 0.8) * math.pi))
            slab_z(m, bd, 0, 8.0, z0, z0 + 3.6, r, r * 0.8, ARM if i < 3 else BODY)
        hd = m.bone("head", bd, (0, 8, -12))
        spike(m, hd, (0, 8.6, -12.0), (0, -0.05, -1), 4.4, 8.0, ARM, tip=0.8)
        m.box(hd, -2.4, 6.0, -19.0, 2.4, 7.4, -12.0, solid(P, "mouth"))
        for j in range(6):
            for sx in (-1, 1):
                spike(m, hd, (sx * 2.0, 7.4, -18.0 + j * 1.0), (0, -1, 0), 0.8, 1.0, solid(P, "tooth"), tip=0.8)
        for sx in (-1, 1):
            m.box(hd, min(sx * 2.0, sx * 3.4), 9.6, -14.6, max(sx * 2.0, sx * 3.4), 10.4, -13.4, solid(P, "eye", glow=True))
            spike(m, bd, (sx * 4.0, 6.0, -4.0), (sx, -0.3, 0.8), 1.4, 12.0, BLADE, tip=0.8)   # side blade fins
            spike(m, bd, (sx * 3.0, 6.0, 8.0), (sx, -0.2, 0.8), 1.2, 7.0, BLADE, tip=0.8)
        for j in range(3 if not x else 6):                                             # back blades
            spike(m, bd, (0, 11.0, -6.0 + j * (4.0 if not x else 2.4)), (0, 1, 0.8), 1.6, 8.0 - j * (1.0 if not x else 0.6),
                  BLADE, tip=0.8)
        tl = m.bone("tail", bd, (0, 8, 14))                                            # long curling neck-tail
        pts = [(0, 8.0, 14.0), (0, 10.0, 20.0), (0, 15.0, 24.0), (0, 21.0, 24.0), (0, 25.0, 20.0), (0, 26.0, 16.0)]
        for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, tl, p0, p1, max(1, 3 - i // 2), BODY, extend=0.5)
        if x:
            spike(m, tl, pts[-1], (0, 0.4, -1), 1.6, 5.0, BLADE, tip=0.8)
        return m
    return build
