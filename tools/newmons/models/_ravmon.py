"""Shared builder for Ravmon and Ravmon: Burst Mode (CobbleEffort: Digital; hand-built after the official art on
wikimon.net). Ravmon: a raven-man warrior in navy-and-steel armour with a red beaked raven helm, great ragged black
feathered wings, a heavy black barrel-launcher in one arm, a curved blade at its wrist, and steel-shod talons. Burst
Mode: radiant: silver-white armour, a long dark feather-tail, and four vast wings of glowing violet light feathers.
Shiny: crimson / gold.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import feather_wing
from _digibody import humanoid
from _digidetail import armour, feathers, metal, solid
from _route import pal, tone


def make(name, burst=False):
    base = {"navy": (40, 44, 80), "navy_dark": (14, 16, 34), "steel": (200, 204, 216), "steel_dark": (100, 104, 120),
            "red": (200, 30, 40), "black": (30, 28, 34), "black_dark": (10, 10, 12), "white": (236, 236, 244),
            "white_dark": (170, 172, 190), "light": (200, 150, 250, 180), "light_dark": (150, 90, 220, 180),
            "eye": (250, 200, 40)}
    shiny = ({"navy": (150, 30, 40), "navy_dark": (70, 10, 14)} if not burst else
             {"light": (255, 220, 120, 180), "light_dark": (230, 170, 60, 180)})

    def P(v):
        return pal(base, shiny, v)

    key, dark = ("white", "white_dark") if burst else ("navy", "navy_dark")
    ARM = armour(P, key, dark, trim="steel", trim_w=0.2)
    STEEL = metal(P, "steel", dark="steel_dark")

    def build():
        m = Model(name)
        mats = {"skin": ARM, "hand": ARM, "finger": STEEL, "talon": STEEL, "foot": STEEL}
        a = humanoid(m, mats, bulk=0.9, arm_bulk=0.85, leg_bulk=0.85, talons=True, digitigrade=True, name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.6, 2.6, 3.0, 54.0, 60.0, armour(P, "black", "black_dark"), cut=1)
        spike(m, hd, (0, 57.0, -3.4), (0, -0.3, -1), 2.0, 5.0, solid(P, "red" if not burst else "steel"), tip=0.8)
        for sx in (-1, 1):
            m.box(hd, min(sx * 1.0, sx * 2.2), 58.0, -3.7, max(sx * 1.0, sx * 2.2), 58.8, -3.5, solid(P, "eye", glow=True))
            for j in range(3):
                spike(m, hd, (sx * 1.4, 60.0, 0.6 + j), (sx * 0.3, 0.6, 1), 1.0, 5.0 - j, solid(P, "black"), tip=0.8)
        if burst:                                                                        # four wings of light
            for sx in (-1, 1):
                for j, (droop, span) in enumerate(((-14.0, 30.0), (8.0, 24.0))):
                    feather_wing(m, bd, (sx * 3.0, 50.0 - j * 6.0, 3.0 + j), span, 16.0, 6,
                                 feathers(P, "light", "light_dark"), side=sx, sweep=25, droop=droop)
            tl = m.bone("tail", bd, (0, 32, 3))
            for j in range(3):
                spike(m, tl, (0, 32.0, 3.0), ((j - 1) * 0.3, -0.8, 1), 1.6, 20.0, solid(P, "black"), tip=0.8)
        else:
            for sx in (-1, 1):
                feather_wing(m, bd, (sx * 3.0, 50.0, 3.0), 26.0, 16.0, 6, feathers(P, "black", "black_dark"), side=sx,
                             sweep=30, droop=-6.0)
            w = a["arm_right"]["wrist"]                                                  # barrel launcher
            rod(m, a["arm_right"]["bone"], (w[0], w[1] + 4.0, w[2] + 2.0), (w[0] - 2.0, w[1] - 2.0, w[2] - 14.0), 4,
                metal(P, "black", dark="black_dark"), extend=0.4)
            m.round_box(a["arm_right"]["bone"], w[0] - 2.0, w[2] - 14.4, 1.4, 0.6, w[1] - 3.4, w[1] - 0.6,
                        solid(P, "red"), cut=0)
            w = a["arm_left"]["wrist"]
            spike(m, a["arm_left"]["bone"], (w[0], w[1], w[2]), (0.3, -0.6, -1), 1.4, 10.0, STEEL, tip=0.8)
        return m

    return build
