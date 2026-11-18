"""Shared builder for Guardromon and Guardromon (Gold) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the walking boiler robot: a round riveted copper hull with a small slit visor and one blue-green eye,
pipes and vents, big bolted arms with clamp hands, a little periscope arm with a pointing glove, stubby piston legs and
hydraulic feet. Gold: the same robot in polished gold. Shiny: gunmetal.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import metal, riveted, skin, solid
from _route import pal, tone


def make(name, gold=False):
    base = {"hull": (180, 110, 80) if not gold else (240, 200, 50), "hull_dark": (110, 60, 40) if not gold else
            (170, 120, 10), "hull_light": (230, 170, 140) if not gold else (255, 240, 150), "steel": (150, 150, 160),
            "steel_dark": (70, 70, 80), "eye": (90, 220, 200), "glove": (246, 246, 246), "glove_dark": (190, 190, 200),
            "red": (220, 40, 40)}
    shiny = {"hull": (90, 94, 106), "hull_dark": (40, 44, 56), "hull_light": (150, 154, 166)}

    def P(v):
        return pal(base, shiny, v)

    HULL = riveted(P, "hull", "hull_dark", light="hull_light")
    PIPE = metal(P, "steel", dark="steel_dark")

    def visorf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north" and abs(x) < 0.8 and abs(y - 25.0) < 0.6:
            return p["eye"], p["eye"]
        return HULL(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 14, 0))
        ball(m, bd, (0, 22.0, 0), 9.0, HULL, layers=6)
        hd = m.bone("head", bd, (0, 28, -6))
        m.round_box(hd, 0, -7.0, 4.0, 2.4, 22.6, 27.4, visorf, cut=1)
        m.box(hd, -3.0, 24.4, -9.6, 3.0, 25.6, -9.3, solid(P, "steel_dark"))
        for sx in (-1, 1):                                                                   # pipes and vents
            rod(m, bd, (sx * 6.0, 28.0, 4.0), (sx * 6.0, 34.0, 4.0), 2, PIPE, extend=0)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab = m.bone(nm, bd, (sx * 9.0, 24.0, 0))
            rod(m, ab, (sx * 9.0, 24.0, 0), (sx * 13.0, 18.0, -4.0), 3, PIPE, extend=0.4)
            m.round_box(ab, sx * 13.0, -6.0, 3.0, 4.0, 12.0, 19.0, HULL, cut=1)               # bolted forearm
            for sy in (-1, 1):
                spike(m, ab, (sx * 13.0, 15.4 + sy * 1.6, -10.0), (0, sy * 0.3, -1), 1.6, 3.0, PIPE, tip=0.8)  # clamp
        pa = m.bone("periscope", bd, (5.0, 30.0, -2.0))                                        # pointing glove arm
        rod(m, pa, (5.0, 30.0, -2.0), (9.0, 36.0, -6.0), 1, PIPE, extend=0, t2=1)
        m.round_box(pa, 9.6, -6.6, 1.2, 1.2, 36.0, 38.0, skin(P, "glove", dark="glove_dark"), cut=0)
        m.round_box(pa, 9.0, -6.0, 0.6, 0.6, 38.0, 39.0, solid(P, "red"), cut=0)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, top, (sx * 4.6, 14.0, 0))
            rod(m, lg, (sx * 4.6, 15.0, 0), (sx * 5.4, 6.0, 0), 3, PIPE, extend=0.4)
            m.round_box(lg, sx * 5.4, -0.6, 3.2, 3.2, 4.0, 10.0, HULL, cut=1)
            m.round_box(lg, sx * 5.4, -2.0, 3.6, 4.6, 0.0, 4.0, HULL, cut=1)
        return m

    return build
