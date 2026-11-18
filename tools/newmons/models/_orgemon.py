"""Shared builder for Orgemon and Orgemon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the green ogre: a hunched muscular green brute with warty skin, a shock of wild white hair, curved horns,
a fanged roaring red mouth, studded black leather bands and wristguards, a red sash, a bone club and long clawed
fingers. The X-Antibody ("x"): darker green skin scarred with glowing red seams, black studded armour wraps, a red-
and-white mane, and a great bloodied guitar-axe instead of the club.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digibody import humanoid
from _digidetail import leather, metal, skin, solid, strands
from _route import pal, tone

BASE = {"green": (90, 170, 60), "green_dark": (40, 100, 24), "wart": (60, 130, 40), "hair": (236, 236, 244),
        "hair_dark": (170, 170, 190), "black": (34, 32, 38), "red": (200, 40, 40), "red_dark": (110, 14, 14),
        "bone": (240, 236, 220), "horn": (60, 56, 64), "mouth": (180, 30, 40), "tooth": (250, 250, 240),
        "eye": (250, 220, 60), "steel": (200, 204, 216), "seam": (255, 70, 70)}
SHINY = {"green": (90, 140, 210), "green_dark": (40, 80, 150), "wart": (60, 100, 180)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    SKIN0 = skin(P, "green", dark="green_dark")
    BAND = leather(P, "black", "black", stitch="steel")

    def skinf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if x and face in ("north", "east", "west") and abs(math.sin(xx * 0.9 + y * 0.5)) < 0.06:
            return p["seam"], p["seam"]
        if face != "down" and math.sin(xx * 1.7) * math.sin(y * 1.9 + z * 1.3) > 0.82:
            return tone(p["wart"], face), None
        return SKIN0(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        mats = {"skin": skinf, "pelvis": BAND, "forearm": BAND if x else skinf, "shin": BAND if x else skinf,
                "claw": solid(P, "red" if x else "black"), "talon": solid(P, "black")}
        a = humanoid(m, mats, bulk=1.15, arm_bulk=1.2, leg_bulk=1.05, claws=True, talons=True, digitigrade=True,
                     name=name)
        bd = a["body"]
        m.box(bd, -5.6, 30.0, -4.4, 5.6, 33.0, -3.6, leather(P, "red", "red_dark"))        # red sash
        hd = m.bone("head", bd, (0, 54, -1))
        m.round_box(hd, 0, -1.4, 2.8, 3.2, 52.0, 58.6, skinf, cut=1)
        m.box(hd, -2.0, 52.4, -4.8, 2.0, 54.6, -4.4, solid(P, "mouth"))                   # roaring mouth
        for sx in (-1, 1):
            spike(m, hd, (sx * 1.6, 52.6, -4.6), (0, 1, 0), 0.9, 2.0, solid(P, "tooth"), tip=0.8)
            m.box(hd, min(sx * 0.6, sx * 1.8), 56.0, -4.7, max(sx * 0.6, sx * 1.8), 56.8, -4.5, solid(P, "eye"))
            pts = [(sx * 2.6, 57.6, -1.0), (sx * 5.0, 60.0, -1.0), (sx * 5.6, 63.0, 0)]
            for j, (p0, p1) in enumerate(zip(pts, pts[1:])):                              # curved horns
                rod(m, hd, p0, p1, 2 - j, solid(P, "horn"), extend=0.3)
        for i in range(10):                                                            # wild mane
            ang = math.radians(-80 + i * 18)
            key = ("red" if i % 3 == 0 else "hair") if x else "hair"
            spike(m, hd, (2.6 * math.sin(ang), 58.0, 0.6 + math.cos(ang)), (math.sin(ang) * 0.7, 0.8, 0.6), 1.6, 6.0,
                  strands(P, key, "hair_dark"), tip=0.8)
        ar = a["arm_right"]
        h = ar["hand"]
        if not x:                                                                       # bone club
            rod(m, ar["bone"], (h[0], h[1], h[2] - 1.0), (h[0] - 2.0, h[1] - 14.0, h[2] - 6.0), 2, solid(P, "bone"),
                extend=0.3)
            ball(m, ar["bone"], (h[0] - 2.0, h[1] - 15.0, h[2] - 6.4), 2.2, solid(P, "bone"), layers=2)
            for j in range(3):
                spike(m, ar["bone"], (h[0] - 2.0, h[1] - 15.0, h[2] - 6.4), ((j - 1) * 0.8, -0.4, -1), 0.9, 2.4,
                      solid(P, "bone"), tip=0.8)
        else:                                                                           # guitar-axe
            rod(m, ar["bone"], (h[0], h[1] + 4.0, h[2] - 1.0), (h[0], h[1] - 24.0, h[2] - 3.0), 1, solid(P, "black"),
                extend=0.2, t2=2)
            m.box(ar["bone"], h[0] - 4.0, h[1] - 24.0, h[2] - 3.8, h[0] + 4.0, h[1] - 12.0, h[2] - 2.2,
                  metal(P, "red", dark="red_dark"))
            m.box(ar["bone"], h[0] - 5.4, h[1] - 23.0, h[2] - 3.6, h[0] - 4.0, h[1] - 13.0, h[2] - 2.4, metal(P, "steel"))
        return m

    return build
