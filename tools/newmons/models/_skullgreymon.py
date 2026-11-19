"""Shared builder for Skull Greymon and Skull Greymon: "G" Erosion Mode (CobbleEffort: Digital; hand-built after the
official art on wikimon.net): the undead dinosaur: a hunched skeleton of bleached bones, a huge horned skull with green
eye-lights and jagged teeth, a ribcage holding a red-glowing heart, long bone arms with huge raking claws, a spine of
bone plates and a long bony tail, and a green-and-orange organic missile on its back. "G" Erosion Mode: the skeleton
overgrown with a wild mane of grey bone spines and a darker, sicker glow. Shiny: obsidian bones.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import armour, solid
from _route import pal, tone


def make(name, erosion=False):
    base = {"bone": (232, 228, 210), "bone_dark": (150, 144, 120), "eye": (80, 240, 120), "heart": (240, 70, 50),
            "missile": (90, 160, 70), "missile_tip": (240, 130, 50), "spine": (170, 170, 176), "mouth": (40, 30, 30),
            "tooth": (250, 250, 240)}
    shiny = {"bone": (60, 56, 66), "bone_dark": (24, 22, 28)}
    if erosion:
        base["eye"] = (230, 60, 240)

    def P(v):
        return pal(base, shiny, v)

    BONE = armour(P, "bone", "bone_dark")

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 22, 0))
        pts = [(0, 34.0, -8.0), (0, 30.0, 2.0), (0, 22.0, 10.0)]                          # hunched spine
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, bd, p0, p1, 2, BONE, extend=0.4)
        for j in range(6):                                                               # ribcage
            z = -6.0 + j * 2.6
            y = 32.0 - j * 1.6
            for sx in (-1, 1):
                rp = [(0, y, z), (sx * 6.0, y - 4.0, z - 1.0), (sx * 4.0, y - 10.0, z - 2.0), (0, y - 12.0, z - 2.0)]
                for p0, p1 in zip(rp, rp[1:]):
                    rod(m, bd, p0, p1, 1, BONE, extend=0.2)
        ball(m, bd, (0, 24.0, -2.0), 2.4, solid(P, "heart", glow=True), layers=2)
        rod(m, bd, (0, 38.0, 4.0), (0, 42.0, -12.0), 4, solid(P, "missile"), extend=0.4)     # organic missile
        spike(m, bd, (0, 42.4, -13.0), (0, 0.2, -1), 2.4, 4.0, solid(P, "missile_tip"), tip=0.8)
        hd = m.bone("head", bd, (0, 34, -10))
        m.round_box(hd, 0, -16.0, 4.6, 7.0, 30.0, 40.0, BONE, cut=1)                       # huge skull
        m.box(hd, -3.6, 30.0, -23.4, 3.6, 33.0, -12.0, solid(P, "mouth"))
        for j in range(6):
            for sx in (-1, 1):
                spike(m, hd, (sx * 3.4, 33.0, -22.0 + j * 1.8), (0, -1, 0), 1.0, 2.0, solid(P, "tooth"), tip=0.8)
        for sx in (-1, 1):
            m.box(hd, min(sx * 4.5, sx * 4.8), 36.0, -18.0, max(sx * 4.5, sx * 4.8), 37.4, -16.0, solid(P, "eye", glow=True))
            spike(m, hd, (sx * 3.0, 40.0, -12.0), (sx * 0.5, 1, 0.4), 1.6, 8.0, BONE, tip=0.8)
        if erosion:                                                                      # mane of bone spines
            for j in range(16):
                ang = math.radians(-80 + j * 10)
                spike(m, hd, (4.0 * math.sin(ang), 40.0, -10.0 + j * 0.4), (math.sin(ang), 0.8, 0.6), 1.2, 10.0,
                      solid(P, "spine"), tip=0.8)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # long bone arms + claws
            ab = m.bone(nm, bd, (sx * 6.0, 30.0, -6.0))
            rod(m, ab, (sx * 6.0, 30.0, -6.0), (sx * 12.0, 20.0, -10.0), 2, BONE, extend=0.4)
            rod(m, ab, (sx * 12.0, 20.0, -10.0), (sx * 12.0, 10.0, -14.0), 2, BONE, extend=0.4)
            for f in range(4):
                spike(m, ab, (sx * 12.0 + (f - 1.5) * 1.4, 10.0, -14.0), ((f - 1.5) * 0.2, -1, -0.6), 1.0, 10.0, BONE,
                      tip=0.8)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, top, (sx * 5.0, 22.0, 6.0))
            rod(m, lg, (sx * 5.0, 22.0, 6.0), (sx * 6.0, 12.0, 0.0), 3, BONE, extend=0.4)
            rod(m, lg, (sx * 6.0, 12.0, 0.0), (sx * 6.0, 2.0, 4.0), 2, BONE, extend=0.4)
            for f in range(3):
                spike(m, lg, (sx * 6.0 + (f - 1) * 1.4, 1.0, 2.0), ((f - 1) * 0.3, -0.2, -1), 1.0, 5.0, BONE, tip=0.8)
        tl = m.bone("tail", bd, (0, 22, 10))
        pts = [(0, 22.0, 10.0), (0, 16.0, 18.0), (0, 10.0, 26.0), (0, 8.0, 34.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, tl, p0, p1, 1, BONE, extend=0.2)
            m.round_box(tl, p1[0], p1[2], 1.6, 1.6, p1[1] - 0.6, p1[1] + 0.6, BONE, cut=0)
        return m

    return build
