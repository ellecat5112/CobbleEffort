"""Shared builder for Metal Mamemon and Metal Mamemon (X-Antibody) (CobbleEffort: Digital; hand-built after the official
art on wikimon.net): the little cyborg super-soldier: a round silver ball of a body dotted with bolt holes, big red
eyes, a red mechanical claw hand, a huge steel arm cannon firing an orange energy ball, and stubby steel legs with
riveted boots. The X-Antibody ("x"): a sleeker blue-grey armoured shell with an orange face plate, a glass dome of
crackling energy on its cannon arm, coloured cables and a pair of trailing orange fins.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import armour, gem, metal, riveted, solid
from _route import pal, tone

BASE = {"silver": (196, 200, 212), "silver_dark": (100, 104, 120), "red": (210, 40, 40), "red_dark": (120, 14, 18),
        "black": (40, 38, 44), "eye": (220, 30, 40), "white": (250, 250, 250), "orange": (250, 120, 40),
        "orange_light": (255, 210, 110), "blue": (90, 120, 190), "blue_dark": (40, 56, 110), "glass": (160, 220, 250),
        "cable_r": (220, 60, 40), "cable_g": (70, 190, 90), "cable_y": (240, 200, 60)}
SHINY = {"silver": (230, 200, 110), "silver_dark": (160, 120, 40), "blue": (170, 90, 190), "blue_dark": (90, 30, 110),
         "red": (60, 170, 80), "red_dark": (20, 90, 30)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    SHELL = riveted(P, "silver", "silver_dark", spacing=1.8) if not x else armour(P, "blue", "blue_dark",
                                                                                   trim="silver", trim_w=0.3)
    STEEL = metal(P, "silver", dark="silver_dark")

    def holesf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if not x and face != "down" and ((round(xx / 2.4) + round(y / 2.4) + round(z / 2.4)) % 3 == 0) and \
                math.hypot(xx - round(xx / 2.4) * 2.4, y - round(y / 2.4) * 2.4) < 0.5:
            return tone(p["black"], face), None
        return SHELL(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 8, 0))
        ball(m, bd, (0, 10.0, 0), 7.0, holesf, layers=6)                                  # round body
        hd = m.bone("head", bd, (0, 12, -6))
        if x:
            m.round_box(hd, 0, -6.4, 4.0, 1.2, 8.0, 14.0, armour(P, "orange", "red_dark"), cut=1)    # face plate
        for sx in (-1, 1):
            ball(m, hd, (sx * 2.4, 11.6, -6.8), 1.4, solid(P, "white"), layers=2)
            m.box(hd, sx * 2.4 - 0.6, 11.0, -8.25, sx * 2.4 + 0.6, 12.2, -8.1, solid(P, "eye", glow=True))
        for j in range(3):                                                                # head bolts / antennae
            spike(m, hd, ((j - 1) * 2.6, 16.6, -1.0), (0, 1, 0), 1.2, 2.0, STEEL, tip=0.8)
        al = m.bone("arm_left", bd, (6.4, 10.0, 0))                                       # red claw hand
        rod(m, al, (6.4, 10.0, 0), (10.0, 13.0, -2.0), 2, STEEL, extend=0.4)
        m.round_box(al, 11.0, -2.6, 2.0, 2.0, 12.0, 16.0, armour(P, "red", "red_dark"), cut=1)
        for j in range(3):
            spike(m, al, (11.0 + (j - 1) * 1.2, 16.0, -3.0), (0, 1, -0.6), 1.0, 3.6, STEEL, tip=0.8)
        ar = m.bone("arm_right", bd, (-6.4, 9.0, 0))                                      # huge arm cannon
        rod(m, ar, (-6.4, 9.0, 0), (-10.0, 8.0, -4.0), 3, STEEL, extend=0.4)
        rod(m, ar, (-10.0, 8.0, -4.0), (-11.0, 7.0, -14.0), 5, SHELL, extend=0.6)
        if not x:
            ball(m, ar, (-11.0, 7.0, -17.0), 3.2, gem(P, "orange", "orange_light"), layers=4)   # energy ball
        else:
            ball(m, ar, (-11.0, 9.0, -8.0), 4.6, gem(P, "glass", "white"), layers=4)            # energy dome
            for i, key in enumerate(("cable_r", "cable_g", "cable_y")):
                rod(m, bd, (-3.0 + i, 15.0, 4.0), (-9.0, 13.0 + i, -6.0), 1, solid(P, key), extend=0.2)
            for sx in (-1, 1):
                rod(m, bd, (sx * 2.0, 4.0, 4.0), (sx * 3.0, -1.0, 9.0), 1, solid(P, "orange"), extend=0.2, t2=3)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, top, (sx * 3.0, 4.0, 0))
            rod(m, lg, (sx * 3.0, 5.0, 0), (sx * 3.4, 2.0, 0), 2, STEEL, extend=0.3)
            m.round_box(lg, sx * 3.4, -0.8, 2.0, 2.8, 0.0, 2.4, SHELL, cut=1)
        return m

    return build
