"""Shared builder for Sparrowmon and Sparrowmon AB (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the jet-bird: a sleek yellow jet fighter with a beaked bird-head cockpit and a green eye, swept wings
and tail fins, little drill-tipped engine pods, and two clawed landing talons. AB (from the manga): heavier armour
plates in red and blue over the yellow, and a pair of big drill-cannons slung under its wings. Shiny: blue.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import slab_z
from _digidetail import armour, metal, solid
from _route import pal, tone


def make(name, ab=False):
    base = {"yellow": (250, 220, 50), "yellow_dark": (200, 150, 20), "steel": (200, 204, 216), "steel_dark": (100, 104, 120),
            "green": (90, 240, 120), "red": (210, 40, 40), "red_dark": (120, 14, 14), "blue": (50, 70, 190),
            "blue_dark": (18, 28, 110), "black": (30, 28, 32)}
    shiny = {"yellow": (90, 150, 240), "yellow_dark": (30, 80, 170)}

    def P(v):
        return pal(base, shiny, v)

    HULL = armour(P, "yellow", "yellow_dark", trim="steel", trim_w=0.2)
    STEEL = metal(P, "steel", dark="steel_dark")

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 10, 0))
        for i in range(6):                                                               # fuselage
            t = (i + 0.5) / 6
            r = 3.0 * math.sin(math.pi * (0.2 + 0.7 * t)) + 0.8
            slab_z(m, bd, 0, 12.0, -10.0 + i * 3.4, -10.0 + (i + 1) * 3.4 + 0.2, r * 1.2, r * 0.9, HULL)
        hd = m.bone("head", bd, (0, 12, -10))
        m.round_box(hd, 0, -12.0, 2.0, 2.0, 10.6, 14.0, HULL, cut=0)
        spike(m, hd, (0, 12.0, -14.0), (0, -0.2, -1), 1.4, 4.0, STEEL, tip=0.8)              # beak
        m.box(hd, 1.0, 13.0, -13.6, 2.2, 14.0, -13.2, solid(P, "green", glow=True))
        for sx in (-1, 1):                                                               # swept wings + fins
            x0, x1 = sorted((sx * 3.0, sx * 16.0))
            m.box(bd, x0, 11.4, -4.0, x1, 12.6, 4.0, HULL, rotation=(0, sx * 25, 0), pivot=(sx * 3.0, 12.0, 0))
            spike(m, bd, (sx * 2.0, 14.0, 8.0), (sx * 0.4, 1, 0.6), 1.4, 5.0, HULL, tip=0.8)
            rod(m, bd, (sx * 5.0, 10.0, 2.0), (sx * 5.0, 10.0, -6.0), 2, STEEL, extend=0.2)
            spike(m, bd, (sx * 5.0, 10.0, -6.0), (0, 0, -1), 1.4, 2.6, metal(P, "black"), tip=0.8)  # drill pods
            lg = m.bone("leg_left" if sx > 0 else "leg_right", bd, (sx * 2.0, 9.0, 0))
            rod(m, lg, (sx * 2.0, 9.0, 0), (sx * 2.4, 3.0, -1.0), 1, STEEL, extend=0.2, t2=2)
            for f in range(3):
                spike(m, lg, (sx * 2.4 + (f - 1) * 0.8, 2.6, -1.4), ((f - 1) * 0.3, -0.6, -1), 0.8, 2.4, STEEL, tip=0.8)
        if ab:                                                                           # heavier plates + cannons
            for sx in (-1, 1):
                m.box(bd, min(sx * 2.0, sx * 4.0), 10.0, -6.0, max(sx * 2.0, sx * 4.0), 15.0, 4.0,
                      armour(P, "red" if sx > 0 else "blue", "red_dark" if sx > 0 else "blue_dark"))
                rod(m, bd, (sx * 10.0, 9.0, 4.0), (sx * 10.0, 9.0, -10.0), 3, STEEL, extend=0.4)
                spike(m, bd, (sx * 10.0, 9.0, -10.0), (0, 0, -1), 2.0, 4.0, metal(P, "black"), tip=0.8)
        return m

    return build
