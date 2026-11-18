"""Shared builder for Garudamon and Garudamon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art
on wikimon.net): the great bird-man: a muscular red-feathered giant with a hawk's head under a red helm, a white
feather beard, great red wings striped gold and yellow at the tips, red trousers with white bands and huge yellow
talons. The X-Antibody form is a burlier orange-red flyer with a white-crested crimson mask, a lance in its arm and
broad brown wings. Shiny: deep blue feathers.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import feather_wing
from _digibody import humanoid
from _digidetail import fabric, feathers, metal, skin, solid
from _route import pal, tone


def make(name, x=False):
    base = {"red": (200, 40, 30), "red_dark": (120, 14, 10), "red_light": (250, 120, 90), "gold": (250, 200, 50),
            "yellow": (250, 220, 60), "yellow_dark": (200, 160, 20), "white": (246, 244, 236),
            "white_dark": (190, 186, 170), "beak": (240, 200, 60), "eye": (40, 40, 40), "claw": (40, 36, 34),
            "brown": (150, 80, 40), "brown_dark": (90, 46, 20), "steel": (210, 214, 224), "steel_dark": (110, 114, 126)}
    if x:
        base.update({"red": (230, 100, 40), "red_dark": (150, 50, 14), "red_light": (255, 170, 110)})
    shiny = {"red": (50, 80, 190), "red_dark": (20, 34, 110), "red_light": (130, 160, 240), "brown": (60, 80, 150)}

    def P(v):
        return pal(base, shiny, v)

    FEATHER = feathers(P, "red", "red_dark", size=(1.4, 2.2))
    SKIN = skin(P, "red", dark="red_dark", light="red_light")
    PANTS = fabric(P, "red", "red_dark", axis="y")

    def pantsf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if abs((y * 0.5) % 3.0 - 1.5) < 0.3:
            return tone(p["white"], face), None
        return PANTS(xx, y, z, face, variant, box=box, **k)

    def wingf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        t = abs(xx) / 30.0
        if x:
            return feathers(P, "brown", "brown_dark", size=(1.6, 2.6))(xx, y, z, face, variant, box=box, **k)
        if t > 0.75:
            return tone(p["yellow"], face), None
        if t > 0.55 and (y % 2.4) < 0.8:
            return tone(p["gold"], face), None
        return FEATHER(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        mats = {"skin": SKIN, "chest": FEATHER, "pelvis": pantsf, "thigh": pantsf, "knee": pantsf, "shin": pantsf,
                "calf": pantsf, "foot": skin(P, "yellow", dark="yellow_dark"), "talon": solid(P, "claw"),
                "claw": solid(P, "claw")}
        a = humanoid(m, mats, bulk=1.25 if x else 1.15, arm_bulk=1.25, leg_bulk=1.1, claws=True, talons=True,
                     digitigrade=True, name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.6, 3.0, 3.4, 53.4, 60.6, FEATHER, cut=1)
        spike(m, hd, (0, 57.0, -4.0), (0, -0.6, -1), 2.4, 5.0, solid(P, "beak"), tip=0.9)       # hooked beak
        for sx in (-1, 1):
            m.box(hd, min(sx * 1.0, sx * 2.4), 58.0, -3.9, max(sx * 1.0, sx * 2.4), 58.8, -3.7, solid(P, "eye"))
        if x:
            m.round_box(hd, 0, -1.0, 3.2, 3.6, 56.6, 59.4, solid(P, "red_dark"), cut=1)         # crimson mask
            for i in range(9):
                spike(m, hd, ((i - 4) * 0.7, 60.0, 0.6), ((i - 4) * 0.2, 1, 0.6), 1.2, 6.0, solid(P, "white"),
                      tip=0.8)
        else:
            m.round_box(hd, 0, 0.0, 3.2, 3.6, 59.0, 62.0, metal(P, "red", dark="red_dark"), cut=1)  # red helm
            spike(m, hd, (0, 61.6, -2.0), (0, 0.5, -1), 1.6, 4.0, solid(P, "gold"), tip=0.8)
        for j in range(6):                                                                    # feather beard
            spike(m, hd, ((j - 2.5) * 0.9, 55.0, -2.6), (0, -1, -0.2), 1.2, 5.0, solid(P, "white"), tip=0.8)
        for side in (1, -1):
            wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 4.0, 48.0, 3.0))
            feather_wing(m, wb, (side * 4.0, 48.0, 3.0), 30.0, 12.0, 3, wingf, side=side, sweep=20, droop=-6.0)
        if x:                                                                                  # lance
            ar, h = a["arm_right"]["bone"], a["arm_right"]["hand"]
            rod(m, ar, (h[0], h[1] + 10.0, h[2] + 6.0), (h[0], h[1] - 8.0, h[2] - 22.0), 2,
                metal(P, "brown", dark="brown_dark"), extend=0)
            spike(m, ar, (h[0], h[1] - 8.0, h[2] - 22.0), (0, -0.6, -1), 2.4, 6.0, metal(P, "steel", dark="steel_dark"),
                  tip=0.9)
        return m

    return build
