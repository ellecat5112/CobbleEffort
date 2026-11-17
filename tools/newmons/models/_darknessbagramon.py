"""Shared builder for Darkness Bagramon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): the
dark emperor. A tall gaunt figure in black armour with gold trim and a horned gold crown, a skeletal pale right arm
with long red claws, great ragged black feathered wings, and an enormous deep-blue cape that billows into tattered
darkness. make(dk=True): Dark Knightmon (Bagramon), its form fused with Dark Knightmon's armour: a hulking body with a
massive bone-white skeletal arm, black plate banded in steel, gold horns and a tattered black cape. Shiny: crimson.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import feather_wing
from _digibody import cape, humanoid
from _digidetail import armour, fabric, feathers, metal, skin, solid
from _route import pal, tone

BASE = {"black": (36, 36, 46), "black_dark": (12, 12, 18), "black_light": (100, 100, 120), "gold": (236, 190, 60),
        "gold_dark": (160, 110, 20), "bone": (230, 220, 190), "bone_dark": (170, 156, 120), "red": (200, 40, 40),
        "blue": (30, 40, 110), "blue_dark": (10, 14, 50), "steel": (200, 204, 216), "steel_dark": (100, 104, 116),
        "feather": (40, 40, 50), "feather_dark": (14, 14, 18), "eye": (250, 60, 60)}
SHINY = {"blue": (130, 20, 30), "blue_dark": (60, 6, 12), "black": (60, 40, 50)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "black", "black_dark", light="black_light", trim="gold", trim_w=0.35)
GOLD = metal(P, "gold", dark="gold_dark")
BONE = skin(P, "bone", dark="bone_dark", var=0.05)


def make(name, dk=False):
    def build():
        m = Model(name)
        mats = {"skin": solid(P, "black_dark"), "chest": PLATE, "abs": PLATE, "pelvis": PLATE, "deltoid": PLATE,
                "upper_arm": PLATE, "forearm": PLATE, "hand": PLATE, "finger": GOLD, "claw": solid(P, "red"),
                "thigh": PLATE, "knee": GOLD, "shin": PLATE, "calf": PLATE, "foot": PLATE, "talon": GOLD}
        a = humanoid(m, mats, bulk=1.3 if dk else 0.95, arm_bulk=1.1, leg_bulk=1.1, digitigrade=True, claws=True,
                     talons=True, name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 2.6, 3.0, 54.0, 61.0, PLATE, cut=1)
        m.box(hd, -1.8, 54.4, -5.6, 1.8, 57.0, -3.0, GOLD)                              # gold muzzle-guard
        m.box(hd, -2.0, 57.6, -3.4, 2.0, 58.2, -3.1, solid(P, "eye", glow=True))
        for sx in (-1, 1):                                                              # horned crown
            spike(m, hd, (sx * 2.4, 60.0, 0), (sx * 0.4, 1, 0.1), 1.8, 7.0, GOLD, tip=0.3)
        ar = a["arm_right"]                                                             # the skeletal arm
        sh, el, h = ar["shoulder"], ar["elbow"], ar["hand"]
        s = 2.0 if dk else 1.0
        rod(m, ar["bone"], sh, el, round(4 * s), BONE, extend=0.6)
        rod(m, ar["bone"], el, h, round(3 * s), BONE, extend=0.6)
        m.round_box(ar["bone"], h[0], h[2], 2.4 * s, 2.4 * s, h[1] - 2.0 * s, h[1] + 2.0, BONE, cut=1)
        for f in range(4):
            spike(m, ar["bone"], (h[0] + (f - 1.5) * 1.2 * s, h[1] - 2.0 * s, h[2] - 1.0), (0, -1, -0.4), 1.0 * s,
                  6.0 * s, solid(P, "red"), tip=0.3)
        if dk:
            for j in range(3):                                                          # steel bands
                y = 30.0 + j * 6.0
                m.round_box(bd, 0, 0.4, 6.6, 5.0, y - 0.6, y + 0.6, metal(P, "steel", dark="steel_dark"), cut=2)
        else:
            for side in (1, -1):                                                        # ragged black wings
                feather_wing(m, bd, (side * 3.0, 50.0, 3.6), 22.0, 12.0, 3,
                             feathers(P, "feather", "feather_dark", size=(1.6, 3.4)), side=side, sweep=30, droop=0.2)
        cb = m.bone("cap", bd, (0, 52, 3))                                              # the enormous cape
        cape(m, cb, 52.0, 30.0 if not dk else 22.0, 50.0,
             fabric(P, "blue" if not dk else "black", "blue_dark" if not dk else "black_dark", axis="y"),
             z=4.6, flare=1.6, panels=10, sweep=(8, 10), seed=17)
        return m
    return build
