"""Shared builder for Omega Shoutmon and Omega Shoutmon (X-Antibody) (CobbleEffort: Digital; hand-built after the official
art on wikimon.net): the golden dragon-knight: a slender armoured warrior of black and gold with a great V-shaped
crest of golden horns, a red visor, spiked gold pauldrons, a long golden lance-blade on its arm and spirals of fire
coiling round it. The X-Antibody ("x"): heavier black-and-gold plate, bigger horns and wings of fire.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import humanoid
from _digidetail import armour, cutout, flame_inside, local, metal, solid
from _route import pal, tone

BASE = {"gold": (240, 200, 70), "gold_dark": (160, 120, 20), "black": (36, 34, 40), "black_dark": (12, 12, 16),
        "red": (220, 40, 40), "steel": (220, 224, 236), "fire": (255, 150, 40, 210), "fire_core": (255, 240, 150, 235)}
SHINY = {"gold": (200, 210, 230), "gold_dark": (110, 120, 140), "fire": (100, 170, 255, 210),
         "fire_core": (220, 240, 255, 235)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    GOLD = armour(P, "gold", "gold_dark", trim="black", trim_w=0.3)
    DARK = armour(P, "black", "black_dark", trim="gold", trim_w=0.3)

    def firef(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(xx, y, z, face, box)
        c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
        return c, c[:3]

    FIRE = cutout(flame_inside(4, 0.1, 7), firef)

    def build():
        m = Model(name)
        mats = {"skin": DARK, "chest": GOLD, "deltoid": GOLD, "forearm": GOLD, "knee": GOLD, "shin": GOLD,
                "foot": GOLD, "toe": GOLD}
        a = humanoid(m, mats, bulk=0.9 if not x else 1.05, arm_bulk=0.9, leg_bulk=0.95, name=name)
        bd = a["body"]
        for sx in (-1, 1):
            spike(m, bd, (sx * 7.0, 51.0, 0), (sx * 0.8, 1, 0.2), 1.6, 6.0 if not x else 9.0, GOLD, tip=0.8)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 2.4, 2.8, 54.0, 59.6, GOLD, cut=1)
        m.box(hd, -1.8, 57.0, -3.3, 1.8, 57.8, -3.1, solid(P, "red", glow=True))
        for sx in (-1, 1):                                                             # V crest of golden horns
            spike(m, hd, (sx * 1.0, 59.4, -1.0), (sx * 0.7, 1, 0.1), 1.6, 12.0 if not x else 15.0, GOLD, tip=0.8)
        ar = a["arm_right"]                                                            # golden lance-blade
        h = ar["hand"]
        rod(m, ar["bone"], (h[0], h[1] + 2.0, h[2]), (h[0] + 2.0, h[1] - 26.0, h[2] - 4.0), 1,
            metal(P, "gold", dark="gold_dark"), extend=0.2, t2=3)
        for i in range(8):                                                             # coiling spiral of fire
            ang = 2 * math.pi * i / 8
            c = (14.0 * math.cos(ang), 20.0 + i * 4.0, 6.0 * math.sin(ang))
            for rot in (0, 90):
                m.box(bd, c[0] - 2.0, c[1], c[2], c[0] + 2.0, c[1] + 5.0, c[2], FIRE, rotation=(0, rot, 0), pivot=c)
        if x:                                                                           # wings of fire
            for side in (1, -1):
                for j in range(3):
                    x0, x1 = sorted((side * 3.0, side * (20.0 - j * 3.0)))
                    m.box(bd, x0, 46.0, 4.0 + j * 0.5, x1, 52.0, 4.0 + j * 0.5, FIRE,
                          rotation=(0, 0, side * (35 - j * 20)), pivot=(side * 3.0, 49.0, 4.0))
        return m

    return build
