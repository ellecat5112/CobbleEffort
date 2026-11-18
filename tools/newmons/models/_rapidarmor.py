"""Shared builder for Rapidmon Armor and Rapidmon (X-Antibody) (CobbleEffort: Digital; hand-built after the official
art on wikimon.net): the golden Rapidmon. Armor (the Armor Digimon of miracles): a round golden robot rabbit, long
golden rocket-ears tipped red, a domed head with a red visor, ball-jointed golden limbs, red-spiked ball cannons for
hands and pointed golden boots. X-Antibody: a sleek golden holy knight, its ears grown into long swept blades, armour
edged in cyan crystal, long bladed gauntlets and pointed greaves. Shiny: silver and blue.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, metal, solid
from _route import pal, tone

BASE = {"gold": (240, 200, 70), "gold_dark": (160, 110, 20), "red": (210, 40, 40), "red_dark": (120, 14, 14),
        "steel": (210, 214, 226), "steel_dark": (110, 114, 126), "visor": (200, 40, 50), "crystal": (90, 230, 240),
        "black": (30, 30, 36), "cream": (250, 236, 200)}
SHINY = {"gold": (210, 214, 226), "gold_dark": (110, 114, 126), "red": (60, 110, 220), "red_dark": (20, 50, 140)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark", trim="red", trim_w=0.2)
STEEL = metal(P, "steel", dark="steel_dark")


def make(name, x=False):
    def build():
        m = Model(name)
        if not x:
            top = m.bone(name, None, (0, 0, 0))
            bd = m.bone("body", top, (0, 14, 0))
            ball(m, bd, (0, 22.0, 0), 6.0, GOLD, layers=5)                              # round golden body
            ball(m, bd, (0, 14.0, 0.4), 4.0, GOLD, layers=3)
            hd = m.bone("head", bd, (0, 28, 0))
            ball(m, hd, (0, 32.0, -0.4), 4.0, GOLD, layers=4)
            m.box(hd, -2.4, 31.6, -4.5, 2.4, 32.8, -4.2, solid(P, "visor", glow=True))
            spike(m, hd, (0, 35.0, -2.0), (0, 1, -0.6), 1.4, 3.0, GOLD, tip=0.8)
            for sx in (-1, 1):                                                           # rocket ears
                for j in range(2):
                    p0 = (sx * 2.0, 35.0, 1.0 + j * 1.2)
                    d = (sx * (0.6 + 0.2 * j), 1, 0.2)
                    rod(m, hd, p0, (p0[0] + d[0] * 12, p0[1] + 12, p0[2] + 2.4), 2, GOLD, extend=0.4)
                    spike(m, hd, (p0[0] + d[0] * 12, p0[1] + 12, p0[2] + 2.4), d, 1.6, 3.0, solid(P, "red"), tip=0.8)
            for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                          # ball cannon hands
                ab = m.bone(nm, bd, (sx * 6.0, 24.0, 0))
                rod(m, ab, (sx * 6.0, 24.0, 0), (sx * 11.0, 20.0, -1.0), 1, STEEL, extend=0.3, t2=2)
                ball(m, ab, (sx * 13.0, 19.0, -1.4), 3.0, armour(P, "red", "red_dark"), layers=3)
                m.round_box(ab, sx * 13.0, -4.4, 1.2, 0.6, 18.0, 20.0, solid(P, "black"), cut=0)
                for j in range(4):
                    ang = 2 * math.pi * j / 4 + 0.4
                    spike(m, ab, (sx * 13.0 + 2.6 * math.cos(ang), 19.0 + 2.6 * math.sin(ang), -1.4),
                          (math.cos(ang), math.sin(ang), 0), 0.8, 1.6, GOLD, tip=0.8)
            for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
                lg = m.bone(nm, top, (sx * 3.0, 12.0, 0))
                rod(m, lg, (sx * 3.0, 12.0, 0), (sx * 3.6, 6.0, 0), 1, STEEL, extend=0.3, t2=2)
                m.round_box(lg, sx * 3.6, -1.0, 2.2, 3.6, 0.0, 6.0, GOLD, cut=1)
                spike(m, lg, (sx * 3.6, 2.0, -4.4), (0, 0.3, -1), 1.6, 3.0, GOLD, tip=0.8)
            return m
        mats = {"skin": GOLD, "neck": STEEL, "knee": GOLD, "talon": GOLD, "claw": GOLD}
        a = humanoid(m, mats, bulk=0.85, arm_bulk=0.8, leg_bulk=0.8, talons=True, digitigrade=True, name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.6, 2.4, 3.0, 54.0, 60.0, GOLD, cut=1)
        m.box(hd, -1.8, 57.0, -3.7, 1.8, 57.8, -3.5, solid(P, "crystal", glow=True))
        for sx in (-1, 1):                                                               # blade ears
            for j in range(3):
                spike(m, hd, (sx * 1.6, 60.0, 0.4 + j), (sx * (0.4 + j * 0.25), 1, 0.4 + j * 0.2), 1.4,
                      18.0 - j * 3.0, GOLD, tip=0.8)
            m.round_box(bd, sx * 7.6, 0, 3.0, 3.4, 46.0, 51.0, GOLD, cut=1)
            spike(m, bd, (sx * 9.0, 50.0, 0), (sx * 1, 0.6, 0.2), 1.6, 8.0, solid(P, "crystal", glow=True), tip=0.8)
            lg = a["leg_left" if sx > 0 else "leg_right"]
            spike(m, lg["bone"], (lg["knee"][0], lg["knee"][1], lg["knee"][2] - 1.0), (0, 0.4, -1), 1.4, 6.0, GOLD,
                  tip=0.8)
        for side in ("arm_left", "arm_right"):                                           # bladed gauntlets
            w = a[side]["wrist"]
            sx = 1 if side == "arm_left" else -1
            spike(m, a[side]["bone"], (w[0], w[1], w[2]), (sx * 0.3, -0.4, -1), 1.6, 14.0, STEEL, tip=0.8)
        return m

    return build
