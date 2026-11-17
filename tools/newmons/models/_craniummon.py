"""Shared builder for Craniummon, the Royal Knight (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): a knight in deep violet plate with a skull motif on its chest, a red-and-blue glowing tabard, a tall
crested helm, a great round violet shield (Avalon) and a double-ended spear (Clanbeena) with long silver blades,
clawed gauntlets and taloned sabatons. make(x=True): the X-Antibody form, magenta-and-violet armour bristling with
spikes, teal glowing seams, red ribbons and a single long cyan-edged lance. Shiny: gold.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import cape, dome, humanoid
from _digidetail import armour, fabric, local, metal, solid
from _route import pal, tone

BASE = {"violet": (90, 70, 150), "violet_dark": (36, 26, 76), "violet_light": (160, 140, 220), "red": (190, 30, 40),
        "red_dark": (100, 10, 16), "blue": (60, 160, 230), "silver": (210, 214, 226), "silver_dark": (110, 114, 128),
        "skull": (236, 230, 210), "eye": (250, 60, 60), "teal": (60, 230, 210), "magenta": (170, 50, 120),
        "under": (30, 26, 40)}
SHINY = {"violet": (220, 180, 70), "violet_dark": (150, 110, 20), "violet_light": (255, 236, 160),
         "magenta": (240, 200, 90)}


def P(v):
    return pal(BASE, SHINY, v)


SILVER = metal(P, "silver", dark="silver_dark")


def make(name, x=False):
    PLATE = armour(P, "magenta" if x else "violet", "violet_dark", light="violet_light", trim="silver" if not x else "teal",
                   trim_w=0.3, glow_key="teal" if x else None)

    def chestf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            if math.hypot(xx, y - 47.0) < 1.8 and not (abs(xx) < 0.4 and y < 46.4):
                return tone(p["skull"], face), None                     # the skull motif
            if abs(xx) < 2.0 and 30.0 < y < 44.0:
                c = p["blue"] if abs(xx) < 0.7 else p["red"]
                return (c, c) if abs(xx) < 0.7 else (tone(c, face), None)  # glowing tabard stripe
        return PLATE(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        mats = {"skin": solid(P, "under"), "chest": chestf, "abs": chestf, "pelvis": PLATE, "deltoid": PLATE,
                "upper_arm": PLATE, "forearm": PLATE, "hand": PLATE, "finger": SILVER, "claw": SILVER, "thigh": PLATE,
                "knee": PLATE, "shin": PLATE, "calf": PLATE, "foot": PLATE, "talon": SILVER}
        a = humanoid(m, mats, bulk=1.15, arm_bulk=1.1, leg_bulk=1.1, digitigrade=True, claws=True, talons=True,
                     name=name, hand_pose="fist")
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.2, 2.8, 3.0, 54.0, 61.0, PLATE, cut=1)
        m.box(hd, -2.0, 57.2, -3.3, 2.0, 57.8, -3.1, solid(P, "eye", glow=True))
        for i in range(5):                                                     # tall crest
            spike(m, hd, (0, 60.6, -2.0 + i * 1.2), (0, 1, 0.3 + 0.15 * i), 1.4, 5.0 - abs(i - 2) * 0.8, SILVER,
                  tip=0.3)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            dome(m, a[nm]["bone"], (a[nm]["shoulder"][0] + sx * 1.8, 49.4, 0.3), 4.4, 4.2, PLATE, layers=4)
            if x:
                for j in range(3):
                    spike(m, a[nm]["bone"], (a[nm]["shoulder"][0] + sx * 3.0, 50.0 + j, -1.0 + j * 1.4),
                          (sx, 0.6, 0.2), 1.4, 5.0, SILVER, tip=0.3)
        if x:                                                                  # spikes and red ribbons
            for j in range(6):
                spike(m, bd, ((j - 2.5) * 2.0, 30.0, -4.0), ((j - 2.5) * 0.2, -1, -0.4), 1.4, 5.0, SILVER, tip=0.3)
            for sx in (-1, 1):
                pts = [(sx * 5.0, 50.0, 3.0), (sx * 9.0, 42.0, 8.0), (sx * 12.0, 30.0, 10.0)]
                for p0, p1 in zip(pts, pts[1:]):
                    rod(m, bd, p0, p1, 1, fabric(P, "red", "red_dark"), extend=0.3, t2=3)
        else:
            al = a["arm_left"]                                                 # Avalon: the great round shield
            h = al["hand"]
            sb = m.bone("shield", al["bone"], h)
            cx, cy, cz = h[0] + 2.0, h[1] + 6.0, h[2] - 3.0
            for fy, fx in ((1.0, 0.42), (0.92, 0.72), (0.72, 0.92), (0.42, 1.0)):
                m.box(sb, cx - 9.0 * fx, cy - 10.0 * fy, cz - 1.6, cx + 9.0 * fx, cy + 10.0 * fy, cz, PLATE)
        ar = a["arm_right"]                                                    # Clanbeena / the X lance
        h = ar["hand"]
        lb = m.bone("spear", ar["bone"], h)
        top, bot = (h[0], h[1] + 26.0, h[2] - 2.0), (h[0], h[1] - 22.0, h[2] + 2.0)
        if x:
            top, bot = (h[0] + 6.0, h[1] + 30.0, h[2] - 14.0), (h[0] - 3.0, h[1] - 10.0, h[2] + 6.0)
        rod(m, lb, bot, top, 1, solid(P, "under"), extend=0)
        for end, d in ((top, 1), (bot, -1)) if not x else ((top, 1),):
            n = math.dist(top, bot)
            u = tuple((t - b) / n * d for t, b in zip(top, bot))
            spike(m, lb, end, u, 3.0, 10.0 if not x else 18.0, SILVER, tip=0.6)
            m.box(lb, end[0] - 2.4, end[1] - 0.8, end[2] - 0.8, end[0] + 2.4, end[1] + 0.8, end[2] + 0.8, PLATE)
        return m
    return build
