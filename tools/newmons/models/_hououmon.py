"""Shared builder for Hououmon and Hououmon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the phoenix, one of the Four Great Dragons' peers among the holy beasts: a great golden bird with a
hooked beak, a crest of red-and-gold flame feathers, vast golden wings, a fan of long tail plumes tipped with red
diamond eyes, grey talons with gold rings. X-Antibody: a radiant white-gold phoenix with brighter wings, long silver
tail ribbons and crackling red lightning. Shiny: blue fire.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import feather_wing
from _digidetail import feathers, metal, solid, strands
from _route import pal, tone


def make(name, x=False):
    base = {"gold": (250, 210, 80) if not x else (255, 240, 170), "gold_dark": (200, 150, 30) if not x else (220, 190, 90),
            "red": (220, 60, 40), "beak": (240, 220, 160), "grey": (110, 100, 100), "eye": (230, 40, 40),
            "plume": (250, 180, 60), "plume_dark": (200, 90, 20), "silver": (230, 230, 240), "bolt": (240, 40, 80)}
    shiny = {"gold": (130, 200, 255), "gold_dark": (60, 120, 220), "plume": (120, 160, 255), "red": (60, 90, 230)}

    def P(v):
        return pal(base, shiny, v)

    FEATH = feathers(P, "gold", "gold_dark", size=(1.6, 2.6), tip="red")

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 20, 0))
        m.round_box(bd, 0, 0, 6.0, 7.0, 18.0, 34.0, FEATH, cut=2)
        hd = m.bone("head", bd, (0, 34, -6))
        m.round_box(hd, 0, -6.0, 3.0, 3.6, 33.0, 40.0, FEATH, cut=1)
        spike(m, hd, (0, 36.0, -9.4), (0, -0.6, -1), 2.4, 5.0, solid(P, "beak"), tip=0.9)
        for sx in (-1, 1):
            m.box(hd, min(sx * 3.0, sx * 3.2), 37.6, -8.0, max(sx * 3.0, sx * 3.2), 38.4, -7.0, solid(P, "eye", glow=True))
        for j in range(7):                                                            # flame crest
            spike(m, hd, (0, 39.6, -5.0 + j * 1.2), (0.3 * (j % 2 - 0.5), 1, 0.6), 1.2, 7.0 - abs(j - 3) * 0.6,
                  strands(P, "red", "gold"), tip=0.8)
        for side in (1, -1):
            wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 5.0, 30.0, 2.0))
            feather_wing(m, wb, (side * 5.0, 30.0, 2.0), 32.0, 14.0, 3, FEATH, side=side, sweep=10, droop=-12.0)
        tb = m.bone("tail", bd, (0, 20, 6))                                             # fan of tail plumes
        for i in range(9):
            ang = math.radians(-60 + i * 15)
            end = (14.0 * math.sin(ang), 20.0 - 12.0 * math.cos(ang) * 0.6, 6.0 + 16.0 * math.cos(ang))
            rod(m, tb, (0, 20.0, 6.0), end, 1, strands(P, "plume" if not x else "silver", "plume_dark"), extend=0.3,
                t2=2)
            m.round_box(tb, end[0], end[2], 1.0, 1.0, end[1] - 1.4, end[1] + 1.4, solid(P, "red"), cut=0)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, bd, (sx * 3.0, 18.0, 0))
            rod(m, lg, (sx * 3.0, 18.0, 0), (sx * 3.4, 8.0, -3.0), 2, solid(P, "grey"), extend=0.4)
            m.round_box(lg, sx * 3.4, -3.0, 1.6, 1.6, 9.0, 10.4, metal(P, "gold", dark="gold_dark"), cut=0)
            for j in range(3):
                spike(m, lg, (sx * 3.4 + (j - 1) * 1.0, 8.0, -3.0), ((j - 1) * 0.4, -0.6, -1), 0.9, 4.0, solid(P, "grey"),
                      tip=0.8)
        if x:
            for j in range(5):
                ang = 2 * math.pi * j / 5
                rod(m, bd, (8.0 * math.cos(ang), 26.0, 8.0 * math.sin(ang)), (12.0 * math.cos(ang + 0.6), 20.0,
                    12.0 * math.sin(ang + 0.6)), 1, solid(P, "bolt", glow=True), extend=0, t2=1)
        return m

    return build
