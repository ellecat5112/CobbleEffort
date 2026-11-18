"""Shared builder for Gravimon and Gravimon Darkness Mode (CobbleEffort: Digital; hand-built after the official art
on wikimon.net). Gravimon: a gaunt skeletal white giant with a long ribbed spine for a waist, a tattered black-and-
grey shroud of hair streaming from its head, huge hanging clawed hands and long dark cables looping round it ending
in brass plugs. Darkness Mode: a lean figure in a red body suit with white armoured shoulders, great black and gold
wings crackling with orange lightning, a black flame crown, and a curtain of long cables with brass plugs hanging
from its outstretched white arms. Shiny: bone-gold and violet.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import feather_wing
from _digidetail import armour, feathers, metal, skin, solid, strands
from _route import pal, tone


def make(name, dark=False):
    base = {"white": (236, 236, 240), "white_dark": (170, 172, 186), "black": (34, 32, 38), "black_dark": (12, 12, 16),
            "grey": (140, 140, 150), "cable": (90, 30, 40), "cable_dark": (40, 10, 16), "brass": (220, 180, 70),
            "red": (200, 30, 40), "red_dark": (120, 10, 16), "gold": (220, 170, 50), "gold_dark": (140, 100, 20),
            "bolt": (255, 160, 40), "eye": (230, 40, 40)}
    shiny = {"white": (230, 210, 150), "white_dark": (170, 150, 90), "cable": (90, 50, 140), "red": (60, 50, 140)}

    def P(v):
        return pal(base, shiny, v)

    BONE = skin(P, "white", dark="white_dark")
    CABLE = metal(P, "cable", dark="cable_dark")

    def cable(m, bone, pts):
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, bone, p0, p1, 1, CABLE, extend=0.3, t2=1)
        m.round_box(bone, pts[-1][0], pts[-1][2], 0.6, 0.6, pts[-1][1] - 1.4, pts[-1][1], solid(P, "brass"), cut=0)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 30, 0))
        if not dark:
            for j in range(10):                                                      # ribbed spine waist
                m.round_box(bd, 0, 0, 1.6 + (j % 2) * 0.6, 1.4, 20.0 + j * 2.0, 21.4 + j * 2.0, BONE, cut=0)
            m.round_box(bd, 0, 0, 5.0, 3.0, 40.0, 50.0, BONE, cut=1)                  # ribcage
            for j in range(4):
                m.box(bd, -5.2, 41.0 + j * 2.2, -3.2, 5.2, 41.6 + j * 2.2, -2.8, solid(P, "black"))
        else:
            m.round_box(bd, 0, 0, 3.4, 2.6, 22.0, 44.0, skin(P, "red", dark="red_dark"), cut=1)  # red body suit
            m.round_box(bd, 0, 0, 7.0, 3.6, 42.0, 48.0, armour(P, "white", "white_dark", trim="gold"), cut=1)
        hd = m.bone("head", bd, (0, 50, 0))
        m.round_box(hd, 0, -0.4, 2.6, 2.8, 48.6, 55.0, BONE, cut=1)
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.6, sx * 1.8), 52.0, -3.3, max(sx * 0.6, sx * 1.8), 52.8, -3.1, solid(P, "eye", glow=True))
        for i in range(12):                                                          # streaming hair / black flame crown
            ang = math.radians(-120 + i * 22)
            spike(m, hd, (2.2 * math.sin(ang), 54.6, 0.4 + 1.6 * math.cos(ang) + 1.0),
                  (math.sin(ang) * (1.2 if not dark else 0.4), 0.6 if not dark else 1.0, 0.8 if not dark else 0.2),
                  1.8, 12.0 if not dark else 9.0, strands(P, "black", "grey"), tip=0.9)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab = m.bone(nm, bd, (sx * 5.0, 48.0, 0))
            if not dark:                                                              # long arms, huge hanging hands
                pts = [(sx * 5.0, 48.0, 0), (sx * 10.0, 34.0, -2.0), (sx * 12.0, 16.0, -4.0)]
                for p0, p1 in zip(pts, pts[1:]):
                    rod(m, ab, p0, p1, 2, BONE, extend=0.4)
                m.round_box(ab, sx * 12.0, -4.0, 3.6, 3.0, 8.0, 16.0, BONE, cut=1)
                for j in range(4):
                    spike(m, ab, (sx * 12.0 + (j - 1.5) * 1.6, 8.0, -4.0), (0, -1, -0.2), 1.0, 5.0, BONE, tip=0.8)
                for j in range(3):
                    cable(m, ab, [(sx * 6.0, 46.0, 1.0), (sx * (14.0 + j * 4.0), 56.0 - j * 6.0, 4.0),
                                  (sx * (20.0 + j * 4.0), 40.0 - j * 4.0, 2.0), (sx * (16.0 + j * 2.0), 30.0 - j * 4.0, -2.0)])
            else:                                                                      # outstretched arms, cable curtain
                rod(m, ab, (sx * 5.0, 48.0, 0), (sx * 20.0, 44.0, 0), 2, BONE, extend=0.4)
                m.round_box(ab, sx * 21.0, 0, 2.4, 2.4, 40.0, 46.0, BONE, cut=1)
                for j in range(6):
                    x = sx * (8.0 + j * 2.6)
                    cable(m, ab, [(x, 46.0 - j * 0.6, 0), (x + sx * 1.0, 20.0, 1.0), (x + sx * 1.6, 2.0, 0)])
        if dark:
            for side in (1, -1):                                                        # black and gold wings
                wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 4.0, 50.0, 3.0))
                feather_wing(m, wb, (side * 4.0, 50.0, 3.0), 26.0, 10.0, 3,
                             feathers(P, "black", "black_dark", tip="gold"), side=side, sweep=10, droop=-12.0)
                for j in range(3):
                    spike(m, wb, (side * (16.0 + j * 4.0), 58.0 + j * 2.0, 4.0), (side * 0.8, 0.6, 0), 1.0, 5.0,
                          solid(P, "bolt", glow=True), tip=0.8)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, top, (sx * 2.6, 22.0, 0))
            rod(m, lg, (sx * 2.6, 22.0, 0), (sx * 4.0, 2.0, -1.0), 2, BONE if not dark else solid(P, "black"), extend=0.4)
            for j in range(3):
                spike(m, lg, (sx * 4.0 + (j - 1) * 1.0, 0.6, -2.0), (0, -0.2, -1), 0.8, 4.0, BONE, tip=0.8)
        return m

    return build
