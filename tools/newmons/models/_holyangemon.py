"""Shared builder for Holy Angemon and Holy Angemon: Priest Mode (CobbleEffort: Digital; hand-built after the official
art on wikimon.net). Holy Angemon: a tall angel warrior in grey plate under a white tabard, a violet-visored helm,
eight great white wings, a long violet sash, golden arm guards with an Excalibur beam blade and grey greaves. Priest
Mode: the same angel in long flowing white priest's robes with a high collar and long blond hair under the helm, eight
white wings held round it, and a long sword planted before it. Shiny: black wings and gold.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import feather_wing
from _digibody import cape, humanoid
from _digidetail import armour, fabric, feathers, metal, solid, strands
from _route import pal, tone


def make(name, priest=False):
    base = {"white": (246, 246, 250), "white_dark": (190, 192, 206), "grey": (160, 164, 176), "grey_dark": (80, 84, 96),
            "gold": (230, 190, 70), "gold_dark": (150, 110, 20), "violet": (130, 80, 190), "violet_dark": (70, 30, 120),
            "hair": (240, 220, 140), "hair_dark": (190, 160, 70), "beam": (210, 140, 255), "steel": (220, 224, 234),
            "steel_dark": (110, 114, 126)}
    shiny = {"white": (50, 48, 56), "white_dark": (20, 18, 24)}

    def P(v):
        return pal(base, shiny, v)

    ARM = armour(P, "grey", "grey_dark", trim="gold", trim_w=0.3)
    ROBE = fabric(P, "white", "white_dark", axis="y")
    WING = feathers(P, "white", "white_dark", size=(1.6, 2.8))

    def build():
        m = Model(name)
        if priest:
            mats = {"skin": ROBE, "hand": ARM, "finger": ARM, "foot": ROBE}
        else:
            mats = {"skin": ARM, "chest": ROBE, "abs": ROBE, "forearm": metal(P, "gold", dark="gold_dark")}
        a = humanoid(m, mats, bulk=0.95, arm_bulk=0.95, leg_bulk=1.0, name=name)
        bd = a["body"]
        if priest:                                                                 # long flowing robes
            m.round_box(bd, 0, 0.4, 7.0, 6.0, 0.0, 34.0, ROBE, cut=3)
            m.round_box(bd, 0, 0, 5.6, 4.6, 48.0, 54.0, ROBE, cut=2)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 2.6, 3.0, 53.6, 60.4, ARM, cut=1)
        m.box(hd, -2.0, 56.6, -3.5, 2.0, 57.6, -3.3, solid(P, "violet"))
        spike(m, hd, (0, 60.0, -0.4), (0, 1, 0.2), 1.6, 4.0, ARM, tip=0.8)
        if priest:
            for i in range(8):
                ang = math.radians(-100 + i * 28)
                rod(m, hd, (2.4 * math.sin(ang), 58.0, 1.0 + math.cos(ang)), (3.4 * math.sin(ang), 44.0, 4.0), 1,
                    strands(P, "hair", "hair_dark"), extend=0.3, t2=2)
        else:
            rod(m, bd, (2.0, 50.0, -3.0), (6.0, 30.0, -4.0), 1, fabric(P, "violet", "violet_dark"), extend=0.3, t2=4)
        for side in (1, -1):                                                        # eight great wings
            for j in range(4):
                wb = m.bone(("wing_left" if side > 0 else "wing_right") + str(j), bd, (side * 3.0, 50.0 - j * 2.0, 4.0))
                feather_wing(m, wb, (side * 3.0, 50.0 - j * 2.0, 4.0), 22.0 - j * 2.0, 8.0, 2, WING, side=side,
                             sweep=-10 + j * 18, droop=(20.0 if priest else -4.0) + j * 6.0)
        ar, h = a["arm_right"]["bone"], a["arm_right"]["hand"]
        if priest:                                                                   # sword planted before it
            rod(m, ar, (h[0], h[1] + 3.0, h[2] - 3.0), (h[0], 0.4, h[2] - 3.0), 1, metal(P, "steel", dark="steel_dark"),
                extend=0, t2=2)
            m.box(ar, h[0] - 2.4, h[1] + 0.4, h[2] - 3.4, h[0] + 2.4, h[1] + 1.2, h[2] - 2.6, metal(P, "gold", dark="gold_dark"))
        else:                                                                         # Excalibur beam blade
            rod(m, ar, (h[0], h[1] + 2.0, h[2] - 2.0), (h[0] - 4.0, h[1] - 16.0, h[2] - 14.0), 1, solid(P, "beam", glow=True),
                extend=0, t2=2)
        return m

    return build
