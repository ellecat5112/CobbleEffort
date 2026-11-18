"""Shared builder for Gazimon and Gazimon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net). Gazimon: a crouching lavender-grey beast with huge swept-back ears tipped dark, a sly smile, long white
sabre fangs, orange eyes with dark marks, a tail ending in a fan of fur bound with rings, and black claws. X-Antibody:
an upright pale-blue gremlin with long jagged ears, a gaping red maw, long black claws and black straps. Shiny: sandy
gold fur.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digidetail import fur, metal, solid
from _route import pal, tone


def make(name, x=False):
    base = {"fur": (200, 196, 240) if not x else (150, 180, 230), "fur_dark": (130, 120, 190) if not x else
            (80, 110, 170), "black": (30, 28, 34), "tooth": (250, 250, 246), "eye": (240, 120, 40) if not x else
            (230, 30, 40), "mouth": (180, 30, 40), "ring": (60, 60, 70), "ring_dark": (20, 20, 26)}
    shiny = {"fur": (230, 200, 130), "fur_dark": (170, 140, 70)}

    def P(v):
        return pal(base, shiny, v)

    FUR = fur(P, "fur", "fur_dark", length=1.0, density=2.2)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        if x:                                                                  # upright gremlin
            bd = m.bone("body", top, (0, 10, 0))
            m.round_box(bd, 0, 0.6, 3.4, 3.0, 10.0, 20.0, FUR, cut=1)
            m.round_box(bd, 0, 0.4, 3.6, 3.2, 12.0, 13.0, solid(P, "black"), cut=1)
            hd = m.bone("head", bd, (0, 20, -1))
            m.round_box(hd, 0, -1.4, 3.4, 3.4, 19.6, 26.0, FUR, cut=2)
            m.round_box(hd, 0, -4.9, 2.0, 0.3, 20.0, 23.6, solid(P, "mouth"), cut=0)
            for sx in (-1, 1):
                spike(m, hd, (sx * 1.0, 23.4, -5.0), (0, -1, 0), 0.6, 2.0, solid(P, "tooth"))
                m.box(hd, min(sx * 1.0, sx * 2.2), 24.4, -5.0, max(sx * 1.0, sx * 2.2), 25.0, -4.8, solid(P, "eye"))
                for j in range(3):                                             # long jagged ears
                    spike(m, hd, (sx * 2.6, 25.4 - j * 0.6, 0.6 + j * 0.8), (sx * 0.8, 0.9 - j * 0.2, 0.6), 1.6,
                          10.0 - j * 2.0, FUR, tip=0.8)
            for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
                ab = m.bone(nm, bd, (sx * 3.4, 18.0, -1.0))
                rod(m, ab, (sx * 3.4, 18.0, -1.0), (sx * 7.0, 14.0, -4.0), 2, FUR, extend=0.4)
                m.round_box(ab, sx * 6.0, -3.0, 1.6, 1.6, 15.0, 16.2, solid(P, "black"), cut=0)
                for j in range(3):
                    spike(m, ab, (sx * 7.0 + (j - 1) * 0.8, 13.4, -4.6), (sx * 0.3, -0.6, -1), 0.8, 6.0,
                          solid(P, "black"), tip=0.8)
            for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
                lg = m.bone(nm, top, (sx * 2.0, 10.0, 0))
                rod(m, lg, (sx * 2.0, 10.0, 0), (sx * 3.0, 5.0, 1.4), 2, FUR, extend=0.4)
                rod(m, lg, (sx * 3.0, 5.0, 1.4), (sx * 3.0, 1.0, 0.0), 2, FUR, extend=0.4)
                m.round_box(lg, sx * 3.0, 0.4, 1.6, 1.6, 2.4, 3.4, solid(P, "black"), cut=0)
                for j in range(3):
                    spike(m, lg, (sx * 3.0 + (j - 1) * 0.9, 0.5, -1.4), (0, -0.1, -1), 0.8, 2.4, solid(P, "black"),
                          tip=0.8)
            return m
        bd = m.bone("body", top, (0, 7, 0))                                     # crouching Gazimon
        m.round_box(bd, 0, 1.0, 4.0, 5.6, 4.0, 12.0, FUR, cut=2)
        hd = m.bone("head", bd, (0, 12, -4))
        m.round_box(hd, 0, -5.0, 3.6, 3.4, 9.4, 16.6, FUR, cut=2)
        for sx in (-1, 1):
            m.box(hd, min(sx * 1.0, sx * 2.6), 14.0, -8.5, max(sx * 1.0, sx * 2.6), 14.8, -8.3, solid(P, "eye"))
            m.box(hd, min(sx * 2.6, sx * 3.0), 13.0, -8.5, max(sx * 2.6, sx * 3.0), 15.6, -8.3, solid(P, "black"))
            spike(m, hd, (sx * 1.2, 11.0, -8.0), (0, -1, -0.2), 1.0, 5.0, solid(P, "tooth"), tip=0.8)   # sabre fangs
            for j in range(3):                                                  # huge swept-back ears
                spike(m, hd, (sx * 3.0, 16.0, -4.0 + j * 1.2), (sx * 1.0, 0.5, 0.6 + j * 0.2), 1.8 - j * 0.3,
                      11.0 - j * 2.0, FUR, tip=0.9)
        for sx, nm in ((1, "leg_front_left"), (-1, "leg_front_right"), (1, "leg_back_left"), (-1, "leg_back_right")):
            z = -4.0 if "front" in nm else 5.0
            lg = m.bone(nm, top, (sx * 3.4, 6.0, z))
            rod(m, lg, (sx * 3.4, 7.0, z), (sx * 4.0, 1.0, z - 1.0), 2, FUR, extend=0.4, t2=3)
            for j in range(3):
                spike(m, lg, (sx * 4.0 + (j - 1) * 0.9, 0.5, z - 2.4), (0, -0.2, -1), 0.8, 2.0, solid(P, "black"),
                      tip=0.8)
        tb = m.bone("tail", bd, (0, 8, 6))
        rod(m, tb, (0, 8.0, 6.0), (0, 12.0, 13.0), 1, FUR, extend=0.4, t2=1)
        for j in range(3):
            m.round_box(tb, 0, 9.6 + j * 0.9, 1.0, 0.4, 9.0 + j * 0.6, 10.4 + j * 0.6,
                        metal(P, "ring", dark="ring_dark"), cut=0)
        for j in range(4):
            spike(m, tb, (0, 12.0, 13.0), ((j - 1.5) * 0.5, 0.6, 1), 1.2, 4.0, FUR, tip=0.8)
        return m

    return build
