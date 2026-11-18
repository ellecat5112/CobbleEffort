"""Shared builder for Nezhamon and Nezhamon: Crimson Mode (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the cyborg child-god of the Four Holy Beasts' realm: a youthful armoured warrior in gold-and-black
plate with a round revolver-cylinder faceplate, a long red sash streaming like flame, a fire-tipped spear held across
its back, flames bursting from its shoulders, and its legs set into two great black-and-gold wheels (Wind-Fire
Wheels). Crimson Mode ("crimson"): red armour, a flaming blade in each hand, the wheels turned into a blazing
motorcycle beneath it and a trailing beaded rope.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, cutout, fabric, flame_inside, local, metal, solid
from _route import pal, tone

BASE = {"gold": (236, 190, 70), "gold_dark": (150, 110, 24), "black": (36, 34, 40), "black_dark": (12, 12, 16),
        "red": (210, 40, 40), "red_dark": (120, 14, 14), "orange": (240, 140, 40), "steel": (210, 214, 226),
        "steel_dark": (100, 104, 116), "eye": (60, 230, 220), "fire": (255, 140, 40, 215),
        "fire_core": (255, 240, 160, 235), "white": (240, 240, 236)}
SHINY = {"gold": (200, 210, 230), "gold_dark": (110, 120, 140), "red": (60, 90, 210), "red_dark": (20, 40, 130),
         "fire": (90, 170, 255, 215), "fire_core": (220, 240, 255, 235)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, crimson=False):
    PLATE = armour(P, "red" if crimson else "gold", "red_dark" if crimson else "gold_dark", trim="black", trim_w=0.3)
    DARK = armour(P, "black", "black_dark", trim="gold", trim_w=0.3)
    SASH = fabric(P, "red", "red_dark")

    def firef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        c = p["fire_core"] if v / max(H, 1e-6) < 0.35 else p["fire"]
        return c, c[:3]

    FIRE = cutout(flame_inside(4, 0.1, 6), firef)

    def flame(m, bone, c, w, h, ang=0.0):
        for a in (0, 90):
            m.box(bone, c[0] - w / 2, c[1], c[2], c[0] + w / 2, c[1] + h, c[2], FIRE, rotation=(0, a + ang, 0), pivot=c)

    def wheel(m, bone, c, r, axis_x=True):
        cx, cy, cz = c
        for i in range(12):
            ang = 2 * math.pi * i / 12
            if axis_x:
                m.box(bone, cx - 1.6, cy + r * math.sin(ang) - 1.4, cz + r * math.cos(ang) - 1.4, cx + 1.6,
                      cy + r * math.sin(ang) + 1.4, cz + r * math.cos(ang) + 1.4, DARK)
        m.round_box(bone, cx, cz, 1.0, r * 0.5, cy - r * 0.5, cy + r * 0.5, PLATE, cut=1)

    def build():
        m = Model(name)
        mats = {"skin": PLATE, "chest": PLATE, "abs": DARK, "pelvis": DARK, "neck": DARK, "deltoid": PLATE,
                "upper_arm": DARK, "forearm": PLATE, "hand": DARK, "finger": DARK, "thigh": fabric(P, "orange", "red_dark"),
                "knee": PLATE, "shin": PLATE, "calf": PLATE, "foot": DARK, "toe": DARK}
        a = humanoid(m, mats, bulk=0.9, arm_bulk=0.9, leg_bulk=0.95, hand_pose="fist", name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 2.6, 2.8, 54.0, 60.0, PLATE, cut=1)
        for i in range(6):                                                             # revolver-cylinder faceplate
            ang = 2 * math.pi * i / 6
            m.box(hd, 1.2 * math.cos(ang) - 0.5, 57.0 + 1.2 * math.sin(ang) - 0.5, -3.4, 1.2 * math.cos(ang) + 0.5,
                  57.0 + 1.2 * math.sin(ang) + 0.5, -3.2, solid(P, "steel"))
        m.box(hd, -2.0, 58.8, -3.3, 2.0, 59.4, -3.1, solid(P, "eye", glow=True))
        for i in range(7):                                                             # crown of gold spikes
            ang = math.radians(-60 + i * 20)
            spike(m, hd, (2.6 * math.sin(ang), 60.0, -0.6 * math.cos(ang)), (math.sin(ang) * 0.6, 1, 0.2), 1.2, 4.0,
                  metal(P, "gold"), tip=0.8)
        for sx in (-1, 1):                                                             # shoulder flames
            flame(m, bd, (sx * 7.0, 51.0, 0.4), 3.6, 7.0)
        for j in range(5):                                                             # streaming red sash
            m.box(bd, -10.0 + j * 4.0, 40.0 + j * 2.0, 4.0, -6.0 + j * 4.0, 42.0 + j * 2.0, 4.2, SASH,
                  rotation=(0, 0, -20 + j * 10), pivot=(-8.0 + j * 4.0, 41.0 + j * 2.0, 4.1))
        if not crimson:
            rod(m, bd, (-14.0, 34.0, 5.0), (16.0, 58.0, 5.0), 1, solid(P, "black"), extend=0.2)   # spear
            spike(m, bd, (16.0, 58.0, 5.0), (0.8, 0.6, 0), 1.4, 5.0, metal(P, "steel"), tip=0.8)
            flame(m, bd, (15.0, 56.0, 5.0), 3.0, 6.0)
            for nm in ("leg_left", "leg_right"):                                       # Wind-Fire Wheels
                ank = a[nm]["ankle"]
                wheel(m, a[nm]["bone"], (ank[0], 5.0, ank[2]), 5.0)
        else:
            for nm in ("arm_left", "arm_right"):                                       # flaming blades
                h = a[nm]["hand"]
                rod(m, a[nm]["bone"], (h[0], h[1], h[2] - 1.0), (h[0], h[1] + 14.0, h[2] - 4.0), 1,
                    metal(P, "steel", dark="steel_dark"), extend=0.2, t2=2)
                flame(m, a[nm]["bone"], (h[0], h[1] + 8.0, h[2] - 3.0), 3.0, 9.0)
            mb = m.bone("bike", a["top"], (0, 8, 0))                                    # blazing motorcycle
            m.round_box(mb, 0, 0, 3.0, 12.0, 6.0, 12.0, PLATE, cut=1)
            wheel(m, mb, (0, 6.0, -12.0), 6.0)
            wheel(m, mb, (0, 6.0, 12.0), 6.0)
            for ang in (0, 90):
                m.box(mb, -3.0, 2.0, 18.0, 3.0, 12.0, 30.0, FIRE, rotation=(0, 0, ang), pivot=(0, 7.0, 18.0))
            for i in range(10):                                                         # trailing beaded rope
                ball(m, bd, (8.0 + i * 0.6, 30.0 - i * 2.4, -2.0), 0.7, solid(P, "white"), layers=1)
        return m

    return build
