"""Shared builder for Ginkakumon and Ginkakumon Promote (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the silver horn oni of the Saiyu Warriors: a hulking armoured demon in silver plate over black chain
mail, two great horns, a snarling oni mask with red eyes, a glass gourd set in its chest, spiked knees and shoulders,
big clawed gauntlets and a black cape. Promote: the same armour turned gleaming gold and wreathed in golden light.
Shiny: gunmetal with blue eyes.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import cape, humanoid
from _digidetail import armour, fabric, gem, metal, riveted, solid
from _route import pal, tone


def make(name, promote=False):
    base = {"silver": (210, 214, 224) if not promote else (250, 210, 80), "silver_dark": (100, 104, 118) if not promote
            else (170, 120, 20), "silver_light": (255, 255, 255) if not promote else (255, 245, 180),
            "black": (36, 34, 40), "black_dark": (12, 12, 16), "eye": (220, 30, 40), "glass": (180, 220, 240),
            "glass_light": (240, 250, 255), "tooth": (250, 250, 240), "aura": (255, 230, 100, 110)}
    shiny = {"silver": (90, 96, 110), "silver_dark": (40, 44, 56), "silver_light": (160, 166, 180), "eye": (60, 160, 250)}

    def P(v):
        return pal(base, shiny, v)

    ARM = armour(P, "silver", "silver_dark", light="silver_light", trim="black", trim_w=0.3)
    MAIL = riveted(P, "black", "black_dark")

    def build():
        m = Model(name)
        mats = {"skin": MAIL, "chest": ARM, "deltoid": ARM, "forearm": ARM, "hand": ARM, "finger": ARM,
                "claw": metal(P, "silver", dark="silver_dark"), "knee": ARM, "shin": ARM, "calf": ARM, "foot": ARM,
                "talon": metal(P, "silver", dark="silver_dark")}
        a = humanoid(m, mats, bulk=1.25, arm_bulk=1.3, leg_bulk=1.15, claws=True, talons=True, digitigrade=True,
                     name=name)
        bd = a["body"]
        m.round_box(bd, 0, -4.4, 2.6, 1.0, 42.0, 48.0, gem(P, "glass", "glass_light", glow=False), cut=1)   # gourd
        m.round_box(bd, 0, -4.8, 1.6, 0.6, 47.6, 50.0, gem(P, "glass", "glass_light", glow=False), cut=0)
        for sx in (-1, 1):
            m.round_box(bd, sx * 9.0, 0.4, 3.6, 4.4, 46.0, 53.0, ARM, cut=1)
            for j in range(3):
                spike(m, bd, (sx * 10.6, 52.0, -1.0 + j * 1.6), (sx * 0.6, 1, 0.1), 1.2, 4.0 - j * 0.6, ARM, tip=0.8)
            kn = a["leg_left" if sx > 0 else "leg_right"]["knee"]
            spike(m, a["leg_left" if sx > 0 else "leg_right"]["bone"], (kn[0], kn[1], kn[2] - 2.0), (0, 0.2, -1), 1.6,
                  4.0, ARM, tip=0.8)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.6, 3.2, 3.4, 53.4, 61.0, ARM, cut=1)                          # oni mask
        m.box(hd, -2.4, 54.6, -4.2, 2.4, 55.6, -3.9, solid(P, "black"))
        for j in range(5):
            spike(m, hd, (-2.0 + j, 55.6, -4.1), (0, -1, 0), 0.6, 1.0, solid(P, "tooth"))
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.8, sx * 2.4), 58.0, -4.1, max(sx * 0.8, sx * 2.4), 58.8, -3.9, solid(P, "eye", glow=True))
            pts = [(sx * 2.6, 60.4, -1.0), (sx * 5.0, 66.0, 0.0), (sx * 4.0, 72.0, 1.0)]              # great horns
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, hd, p0, p1, 2, metal(P, "black", dark="black_dark"), extend=0.4)
        cape(m, bd, 52.0, 18.0, 42.0, fabric(P, "black", "black_dark"), z=5.0, flare=1.0)
        if promote:                                                                             # golden light
            def auraf(xx, y, z, face, variant, box=None, **k):
                c = P(variant)["aura"]
                return c, c[:3]
            for j, (px, py) in enumerate(((-12.0, 20.0), (12.0, 24.0), (-14.0, 44.0), (14.0, 48.0), (0.0, 68.0))):
                spike(m, bd, (px, py, 2.0), (0, 1, 0), 2.4, 10.0, auraf, tip=1.0)
        return m

    return build
