"""Shared builder for the Gaogamon line (CobbleEffort: Digital; hand-built after the official art on wikimon.net):
Gaogamon (Adult) and Mach Gaogamon (Perfect), in their usual colours or as the Black versions.

Gaogamon: a hunched wolf-beast with a great golden mane, red fighting gloves, black-and-steel fur and a jointed metal
tail. Mach Gaogamon: an armoured wolf-man with a jetpack of twin boosters, a steel gauntlet and the golden mane.
Black versions are charcoal and steel; shiny = the classic blue.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, quadruped
from _digibody import dome, humanoid, shell
from _digidetail import armour, fur, leather, metal, solid, strands
from _route import pal, tone

BLUE = {"fur": (60, 110, 200), "fur_dark": (24, 50, 120), "fur_light": (140, 180, 240)}
BLACK = {"fur": (54, 52, 60), "fur_dark": (20, 18, 24), "fur_light": (120, 118, 132)}
COMMON = {"mane": (240, 200, 80), "mane_dark": (180, 130, 30), "red": (210, 40, 40), "red_dark": (120, 14, 20),
          "steel": (200, 204, 216), "steel_dark": (90, 94, 106), "claw": (240, 240, 244), "eye": (255, 220, 60),
          "mouth": (110, 20, 30), "tooth": (250, 250, 246), "black": (30, 30, 36), "glow": (120, 200, 255)}


def make(name, stage, black=True):
    base = dict(COMMON, **(BLACK if black else BLUE))
    shiny = dict(COMMON, **(BLUE if black else BLACK))

    def P(v):
        return pal(base, shiny, v)

    FUR = fur(P, "fur", "fur_dark", tip="fur_light", length=1.4)
    MANE = strands(P, "mane", "mane_dark")
    STEEL = metal(P, "steel", dark="steel_dark")
    GLOVE = leather(P, "red", "red_dark", stitch="steel")

    def build():
        m = Model(name)
        if stage == "adult":
            mats = {"skin": FUR, "belly": FUR, "neck": FUR, "head": FUR, "snout": FUR, "jaw": FUR,
                    "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": FUR, "leg_lower": GLOVE,
                    "paw": GLOVE, "claw": solid(P, "claw"), "tail": STEEL}
            a = quadruped(m, mats, name, length=22.0, body_y=16.0, body_rx=6.4, body_ry=6.4, chest_bulk=1.3,
                          neck=((0, 20, -12), (0, 22, -15)), head_len=9.0, head_w=4.2, head_h=4.4, snout=0.4,
                          mouth_open=10, teeth=4, leg_bulk=1.6, toes=3,
                          tail=((0, 26, 14), (0, 34, 16), (0, 38, 10), (0, 36, 4)), tail_r=(1.6, 1.4, 1.2, 1.0))
            hd = a["head"]
            mane = m.bone("mane", hd, (0, 22, -14))
            for i in range(18):                                  # the great golden mane
                ang = math.radians(i * 20)
                base_p = (4.4 * math.cos(ang), 22.0 + 4.4 * math.sin(ang), -12.0)
                tip = (base_p[0] * 2.0, base_p[1] + 3.0 * math.sin(ang), -6.0)
                rod(m, mane, base_p, tip, 3, MANE, extend=0.3, t2=2)
            for sx in (-1, 1):
                m.box(hd, sx * 2.0 - 0.6, 23.4, -19.4, sx * 2.0 + 0.6, 24.2, -19.2, solid(P, "eye", glow=True))
            tl = a["tail"]
            e = a["tail_pts"][-1]
            for d in ((0.6, -0.4, -1), (-0.6, -0.4, -1), (0, -1, -0.6)):
                spike(m, tl, e, d, 1.4, 4.0, STEEL)              # tail pincer
            return m
        mats = {"skin": FUR, "chest": armour(P, "steel", "steel_dark"), "abs": FUR, "pelvis": FUR, "neck": FUR,
                "deltoid": armour(P, "steel", "steel_dark"), "upper_arm": FUR, "forearm": GLOVE, "hand": GLOVE,
                "finger": GLOVE, "claw": solid(P, "claw"), "thigh": FUR, "knee": STEEL, "shin": armour(P, "steel",
                "steel_dark"), "calf": FUR, "foot": STEEL, "talon": solid(P, "claw")}
        a = humanoid(m, mats, bulk=1.15, arm_bulk=1.3, leg_bulk=1.2, digitigrade=True, claws=True, talons=True,
                     name=name, hand_pose="fist")
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.6, 2.8, 3.0, 54.4, 61.0, FUR, cut=1)
        m.box(hd, -1.8, 54.6, -6.4, 1.8, 57.4, -3.0, FUR)
        m.box(hd, -2.0, 57.8, -3.7, 2.0, 58.6, -3.5, solid(P, "eye", glow=True))
        for sx in (-1, 1):
            spike(m, hd, (sx * 2.0, 60.4, 0), (sx * 0.3, 1, 0.2), 1.4, 3.6, FUR)
        mane = m.bone("mane", hd, (0, 58, 1))
        for i in range(14):
            ang = math.radians(-100 + i * 15)
            rod(m, mane, (3.0 * math.sin(ang), 57.0, 1.0), (6.0 * math.sin(ang), 50.0 + 4.0 * math.cos(ang), 5.0), 3,
                MANE, extend=0.3, t2=2)
        for sx in (-1, 1):                                       # jetpack boosters
            m.round_box(bd, sx * 3.4, 6.0, 2.4, 2.4, 38.0, 52.0, STEEL, cut=1)
            m.box(bd, sx * 3.4 - 1.6, 36.0, 4.4, sx * 3.4 + 1.6, 37.0, 7.6, solid(P, "glow", glow=True))
        al = a["arm_left"]                                       # steel gauntlet
        h = al["hand"]
        m.round_box(al["bone"], h[0], h[2], 3.2, 3.2, h[1] - 3.4, h[1] + 3.0, STEEL, cut=1)
        return m
    return build
