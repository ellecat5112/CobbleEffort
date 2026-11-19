"""Shared builder for Skull Mammon and Skull Mammon (X-Antibody) (CobbleEffort: Digital; hand-built after the official
art on wikimon.net): the undead mammoth: a great skeleton of silver-grey bones on columnar legs with clawed feet, a
red-glowing core in its ribcage, a skull crowned with dark violet crystal spikes, and a long golden mechanical trunk
ending in a claw. X-Antibody: bigger, its trunk a heavy golden spiked chain-arm, great curved silver tusks sweeping up
and back, and a long dark mane. Shiny: bronze bones.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import armour, metal, solid, strands
from _route import pal, tone


def make(name, x=False):
    base = {"bone": (200, 204, 214), "bone_dark": (110, 114, 126), "gold": (236, 196, 70), "gold_dark": (150, 110, 20),
            "violet": (80, 50, 120), "core": (240, 60, 50), "eye": (240, 60, 60), "mane": (50, 46, 56), "mane_dark": (20, 18, 24)}
    shiny = {"bone": (190, 140, 90), "bone_dark": (110, 70, 40)}

    def P(v):
        return pal(base, shiny, v)

    BONE = armour(P, "bone", "bone_dark")
    GOLD = metal(P, "gold", dark="gold_dark")

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 22, 0))
        rod(m, bd, (0, 34.0, -10.0), (0, 32.0, 12.0), 2, BONE, extend=0.4)
        for j in range(7):                                                               # ribcage
            z = -8.0 + j * 3.0
            for sx in (-1, 1):
                rp = [(0, 34.0, z), (sx * 8.0, 30.0, z), (sx * 7.0, 20.0, z), (0, 18.0, z)]
                for p0, p1 in zip(rp, rp[1:]):
                    rod(m, bd, p0, p1, 1, BONE, extend=0.2)
            spike(m, bd, (0, 35.0, z), (0, 1, 0.3), 1.6, 4.0 + (x * 3.0), BONE, tip=0.8)
        ball(m, bd, (0, 26.0, 0), 3.4, solid(P, "core", glow=True), layers=3)
        hd = m.bone("head", bd, (0, 32, -12))
        m.round_box(hd, 0, -16.0, 6.0, 5.0, 26.0, 38.0, BONE, cut=2)                      # skull
        for sx in (-1, 1):
            m.box(hd, min(sx * 5.9, sx * 6.2), 32.0, -19.0, max(sx * 5.9, sx * 6.2), 33.4, -17.0, solid(P, "eye", glow=True))
        for j in range(4 if not x else 6):                                               # crystal spikes / tusks
            if not x:
                spike(m, hd, ((j - 1.5) * 2.4, 38.0, -14.0 + j), ((j - 1.5) * 0.3, 1, 0.3), 1.6, 8.0, solid(P, "violet"),
                      tip=0.8)
            else:
                sx = 1 if j % 2 else -1
                pts = [(sx * 4.0, 28.0, -20.0), (sx * (8.0 + j), 24.0, -26.0), (sx * (10.0 + j), 36.0 + j * 2, -24.0),
                       (sx * (8.0 + j), 44.0 + j * 2, -14.0)]
                for p0, p1 in zip(pts, pts[1:]):
                    rod(m, hd, p0, p1, 2, metal(P, "bone", dark="bone_dark"), extend=0.4)
        tk = m.bone("trunk", hd, (0, 28, -21))                                           # golden trunk
        pts = [(0, 28.0, -21.0), (0, 20.0, -24.0), (0, 12.0, -22.0), (0, 6.0, -26.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, tk, p0, p1, 3 if not x else 4, GOLD, extend=0.4)
            if x:
                spike(m, tk, p1, (0, 0, -1), 1.0, 2.6, metal(P, "bone"), tip=0.8)
        for f in (-1, 1):
            spike(m, tk, (f * 1.4, 6.0, -26.0), (f * 0.6, -0.4, -1), 1.2, 4.0, GOLD, tip=0.8)
        if x:
            for j in range(6):
                rod(m, hd, (0, 38.0, -8.0 + j), ((j - 2.5) * 2.0, 20.0, 4.0 + j * 2.0), 2, strands(P, "mane", "mane_dark"),
                    extend=0.4)
        for sx, nm in ((1, "leg_front_left"), (-1, "leg_front_right"), (1, "leg_back_left"), (-1, "leg_back_right")):
            zz = -6.0 if "front" in nm else 10.0
            lg = m.bone(nm, top, (sx * 6.0, 22.0, zz))
            rod(m, lg, (sx * 6.0, 22.0, zz), (sx * 7.0, 2.0, zz), 4, BONE, extend=0.4)
            m.round_box(lg, sx * 7.0, zz - 0.6, 3.4, 3.6, 0.0, 2.4, BONE, cut=1)
            for f in range(3):
                spike(m, lg, (sx * 7.0 + (f - 1) * 1.8, 1.0, zz - 4.0), (0, -0.2, -1), 1.2, 2.4, BONE, tip=0.8)
        return m

    return build
