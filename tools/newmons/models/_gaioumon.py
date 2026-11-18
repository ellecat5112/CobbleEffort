"""Shared builder for Gaioumon and Gaioumon: Itto Mode (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): a towering dragon-man samurai in black-and-crimson lacquered armour, a horned dragon helm with a mane of
long white hair, glowing teal eyes, clawed gauntlets and talons. Base: two great curved blades (one each hand) and a
tattered black cape. Itto Mode: crimson armour trimmed in gold, a red ribbon sash, sweeping horns and one huge serrated
halberd-sword crackling with red lightning. Shiny: white-and-gold armour.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import cape, humanoid
from _digidetail import armour, fabric, metal, skin, solid, strands
from _route import pal, tone


def make(name, itto=False):
    base = {"black": (40, 36, 44), "black_dark": (14, 12, 18), "black_light": (100, 96, 110), "red": (190, 30, 30),
            "red_dark": (100, 10, 14), "gold": (230, 190, 70), "gold_dark": (150, 110, 20), "steel": (220, 224, 234),
            "steel_dark": (110, 114, 126), "hair": (240, 240, 246), "hair_dark": (180, 180, 196), "eye": (80, 240, 220),
            "claw": (240, 236, 220), "bolt": (255, 60, 60), "sash": (220, 30, 40), "sash_dark": (130, 10, 16)}
    if itto:
        base.update({"black": (180, 30, 30), "black_dark": (100, 10, 14), "black_light": (240, 110, 100),
                     "red": (40, 36, 44), "red_dark": (14, 12, 18)})
    shiny = {"black": (236, 236, 242), "black_dark": (160, 160, 176), "black_light": (255, 255, 255),
             "red": (230, 190, 70), "red_dark": (150, 110, 20)}

    def P(v):
        return pal(base, shiny, v)

    ARM = armour(P, "black", "black_dark", light="black_light", trim="red", trim_w=0.35)
    TRIM = armour(P, "red", "red_dark", trim="gold", trim_w=0.25)
    STEEL = metal(P, "steel", dark="steel_dark")
    HAIR = strands(P, "hair", "hair_dark")

    def build():
        m = Model(name)
        mats = {"skin": ARM, "chest": ARM, "abs": TRIM, "pelvis": TRIM, "neck": ARM, "deltoid": TRIM,
                "upper_arm": ARM, "forearm": TRIM, "hand": ARM, "finger": ARM, "claw": solid(P, "claw"),
                "thigh": ARM, "knee": TRIM, "shin": ARM, "calf": ARM, "foot": ARM, "talon": solid(P, "claw")}
        a = humanoid(m, mats, bulk=1.2, arm_bulk=1.2, leg_bulk=1.15, claws=True, talons=True, digitigrade=True,
                     name=name)
        bd = a["body"]
        for sx in (-1, 1):                                                        # great shoulder plates
            m.round_box(bd, sx * 8.6, 0.4, 3.6, 4.4, 47.0, 53.0, TRIM, cut=1)
            for j in range(3):
                spike(m, bd, (sx * 10.0, 52.0, -1.0 + j * 1.6), (sx * 0.6, 1, 0.2), 1.0, 4.0 - j, STEEL, tip=0.8)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.8, 3.0, 3.4, 53.4, 60.4, ARM, cut=1)                 # dragon helm
        m.round_box(hd, 0, -4.4, 2.0, 1.6, 53.6, 57.0, ARM, cut=1)                 # snout guard
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.8, sx * 2.2), 57.6, -4.3, max(sx * 0.8, sx * 2.2), 58.4, -4.1, solid(P, "eye", glow=True))
            d = (sx * 1.0, 0.7 if itto else 1.0, 0.6)                               # horns
            spike(m, hd, (sx * 2.4, 59.6, -1.0), d, 1.6, 10.0 if itto else 7.0, solid(P, "claw"), tip=0.8)
        for i in range(12):                                                         # long white mane
            ang = math.radians(-110 + i * 20)
            spike(m, hd, (3.0 * math.sin(ang), 60.0, 1.0 + 2.0 * math.cos(ang) + 1.0),
                  (math.sin(ang) * 0.7, 0.2, 1.0), 1.6, 12.0 + (i % 3) * 2.0, HAIR, tip=0.8)
        ar, al = a["arm_right"], a["arm_left"]
        if itto:                                                                     # one huge halberd-sword
            h = ar["hand"]
            rod(m, ar["bone"], (h[0], 6.0, h[2] - 2.0), (h[0], 54.0, h[2] - 2.0), 1, solid(P, "black_dark"), extend=0)
            m.box(ar["bone"], h[0] - 0.5, 44.0, h[2] - 7.0, h[0] + 0.5, 74.0, h[2] - 2.0, STEEL)
            for j in range(6):
                spike(m, ar["bone"], (h[0], 46.0 + j * 4.6, h[2] - 7.0), (0, 0.4, -1), 1.0, 2.6, STEEL, tip=0.8)
                m.box(ar["bone"], h[0] - 0.6, 46.0 + j * 4.6, h[2] - 4.2, h[0] + 0.6, 47.6 + j * 4.6, h[2] - 3.4,
                      solid(P, "bolt", glow=True))
            m.round_box(bd, 0, -0.2, 6.6, 4.4, 33.0, 35.6, fabric(P, "sash", "sash_dark"), cut=1)   # red ribbon sash
            for sx in (-1, 1):
                rod(m, bd, (sx * 2.0, 34.0, -4.0), (sx * 4.0, 24.0, -5.0), 2, fabric(P, "sash", "sash_dark"),
                    extend=0.3, t2=1)
        else:                                                                        # two curved blades
            for arm, sx in ((ar, -1), (al, 1)):
                h = arm["hand"]
                pts = [(h[0], h[1], h[2] - 2.0), (h[0] + sx * 4.0, h[1] + 8.0, h[2] - 10.0),
                       (h[0] + sx * 10.0, h[1] + 14.0, h[2] - 14.0)]
                for p0, p1 in zip(pts, pts[1:]):
                    rod(m, arm["bone"], p0, p1, 1, STEEL, extend=0.4, t2=3)
            cape(m, bd, 52.0, 18.0, 40.0, fabric(P, "black", "black_dark"), z=5.0, flare=0.8)
        return m

    return build
