"""Shared builder for Grademon and Grademon (Vice) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the swordsman knight: a lean armoured warrior with a long-horned helm, ridged shoulder pauldrons,
segmented armour, long clawed feet, a great tattered cape and two long thin swords. Grademon: gold armour with red
details and a deep blue cape, a green scabbard. Vice: navy-violet armour with red details, a dark blue-black cape and
one long curved blade. Shiny: silver and crimson.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import cape, humanoid
from _digidetail import armour, fabric, metal, solid
from _route import pal, tone


def make(name, vice=False):
    base = {"gold": (240, 190, 60) if not vice else (50, 50, 90), "gold_dark": (160, 110, 20) if not vice else (20, 20, 46),
            "gold_light": (255, 236, 150) if not vice else (110, 110, 160), "red": (210, 40, 40),
            "cape": (40, 70, 170) if not vice else (24, 30, 70), "cape_dark": (16, 30, 90) if not vice else (8, 10, 30),
            "steel": (220, 224, 234), "steel_dark": (110, 114, 126), "green": (60, 140, 70), "eye": (250, 60, 40)}
    shiny = {"gold": (210, 214, 226), "gold_dark": (120, 124, 138), "gold_light": (255, 255, 255),
             "cape": (170, 30, 40), "cape_dark": (90, 10, 16)}

    def P(v):
        return pal(base, shiny, v)

    ARM = armour(P, "gold", "gold_dark", light="gold_light", trim="red", trim_w=0.3)
    STEEL = metal(P, "steel", dark="steel_dark")

    def build():
        m = Model(name)
        mats = {"skin": ARM, "claw": STEEL, "talon": metal(P, "gold", dark="gold_dark")}
        a = humanoid(m, mats, bulk=0.85, arm_bulk=0.9, leg_bulk=0.95, claws=True, talons=True, digitigrade=True,
                     name=name)
        bd = a["body"]
        for sx in (-1, 1):                                                          # ridged pauldrons
            m.round_box(bd, sx * 7.4, 0.4, 3.2, 3.6, 47.0, 52.0, ARM, cut=1)
            m.round_box(bd, sx * 7.4, -3.4, 2.0, 0.6, 48.0, 51.0, solid(P, "red"), cut=0)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.6, 2.4, 3.0, 53.6, 59.6, ARM, cut=1)
        m.box(hd, -1.8, 57.2, -3.7, 1.8, 57.8, -3.5, solid(P, "eye", glow=True))
        for sx in (-1, 1):                                                          # long helm horns
            pts = [(sx * 1.6, 59.4, 0), (sx * 3.0, 68.0, 1.0), (sx * 2.6, 76.0, 2.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, hd, p0, p1, 1, ARM, extend=0.4, t2=2)
        spike(m, hd, (0, 59.6, -2.4), (0, 1, -0.4), 1.4, 5.0, ARM, tip=0.8)
        cape(m, bd, 52.0, 18.0, 46.0, fabric(P, "cape", "cape_dark"), z=5.0, flare=1.3)
        for nm, sx in (("arm_right", -1), ("arm_left", 1)):                         # long thin swords
            if vice and nm == "arm_left":
                continue
            h = a[nm]["hand"]
            if vice:
                pts = [(h[0], h[1], h[2] - 1.0), (h[0] + sx * 10.0, h[1] - 6.0, h[2] - 10.0),
                       (h[0] + sx * 24.0, h[1] - 8.0, h[2] - 12.0)]
            else:
                pts = [(h[0], h[1], h[2] - 1.0), (h[0] + sx * 14.0, h[1] + 6.0 * (1 if sx > 0 else -1), h[2] - 14.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, a[nm]["bone"], p0, p1, 1, STEEL, extend=0.3, t2=1)
        if not vice:
            rod(m, bd, (-6.0, 30.0, 3.0), (8.0, 36.0, 4.0), 1, solid(P, "green"), extend=0, t2=2)    # green scabbard
        return m

    return build
