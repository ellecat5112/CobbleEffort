"""Shared builder for Mugendramon and Mugendramon: MFS-3 Mode (CobbleEffort: Digital; hand-built after the official art
on wikimon.net): the infinite machine dragon: a hunched colossus of chrome Chrondigizoit plates, a dinosaur's head
of steel with red eyes and a jagged jaw, two great Giga Cannons on its back, a heavy segmented body, huge arms ending
in three long steel claws and thick clawed legs with a spined tail. MFS-3 Mode ("mfs3"): black-and-chrome armour with
skull-faced shoulder and knee plates, a huge drill-cone on its left arm, a black helm and a long dark rail-gun barrel.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, metal, solid
from _route import pal, tone

BASE = {"chrome": (200, 204, 216), "chrome_dark": (90, 94, 108), "chrome_light": (246, 248, 255), "black": (40, 40, 48),
        "black_dark": (14, 14, 20), "red": (220, 40, 40), "eye": (250, 50, 50), "mouth": (40, 20, 24),
        "tooth": (240, 240, 244), "bone": (236, 232, 224)}
SHINY = {"chrome": (240, 200, 90), "chrome_dark": (160, 110, 30), "chrome_light": (255, 240, 180),
         "black": (110, 40, 40), "black_dark": (60, 14, 14)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, mfs3=False):
    CHROME = armour(P, "chrome", "chrome_dark", light="chrome_light", trim="chrome_dark", trim_w=0.25, rivets=True)
    STEEL = metal(P, "chrome", dark="chrome_dark", light="chrome_light")
    DARK = armour(P, "black", "black_dark", trim="chrome", trim_w=0.25)

    def skullf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            return tone(p["bone"], face), None
        return DARK(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        body = DARK if mfs3 else CHROME
        mats = {"skin": body, "chest": CHROME, "neck": STEEL, "upper_arm": STEEL, "thigh": STEEL,
                "deltoid": skullf if mfs3 else CHROME, "knee": skullf if mfs3 else CHROME, "claw": STEEL,
                "talon": STEEL}
        a = humanoid(m, mats, bulk=1.5, arm_bulk=1.4, leg_bulk=1.5, claws=True, talons=True, digitigrade=True,
                     name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 54, -3))
        m.round_box(hd, 0, -4.0, 3.4, 5.0, 52.0, 58.0, DARK if mfs3 else CHROME, cut=1)  # steel dinosaur head
        m.round_box(hd, 0, -9.0, 2.6, 3.0, 52.6, 56.0, CHROME, cut=1)
        m.box(hd, -2.0, 51.8, -12.0, 2.0, 52.6, -5.0, solid(P, "mouth"))
        for j in range(5):
            for sx in (-1, 1):
                spike(m, hd, (sx * 2.0, 52.6, -11.4 + j * 1.4), (0, -1, 0), 0.8, 1.6, solid(P, "tooth"), tip=0.8)
        for sx in (-1, 1):
            m.box(hd, min(sx * 2.0, sx * 3.0), 56.0, -8.4, max(sx * 2.0, sx * 3.0), 57.0, -8.2,
                  solid(P, "eye", glow=True))
        for sx in (-1, 1):                                                             # two great Giga Cannons
            root = (sx * 5.0, 52.0, 5.0)
            tip = (sx * 7.0, 70.0, 2.0)
            rod(m, bd, root, tip, 7, STEEL, extend=0.8)
            m.round_box(bd, tip[0], tip[2], 4.2, 4.2, tip[1] - 2.0, tip[1] + 1.0, CHROME, cut=1)
            m.round_box(bd, tip[0], tip[2], 2.4, 2.4, tip[1] + 0.9, tip[1] + 1.1, solid(P, "black_dark"), cut=0)
        for nm in ("arm_left", "arm_right"):                                           # three long steel claws
            anc = a[nm]
            h = anc["hand"]
            sx = 1 if h[0] > 0 else -1
            if mfs3 and sx > 0:                                                         # drill-cone arm
                spike(m, anc["bone"], (h[0], h[1] + 2.0, h[2]), (0, -1, -0.3), 7.0, 14.0, DARK, tip=0.8)
                continue
            for f in range(3):
                spike(m, anc["bone"], (h[0] + (f - 1) * 1.6, h[1], h[2] - 1.0), (sx * 0.1, -1, -0.4), 1.4, 9.0, STEEL,
                      tip=0.8)
        if mfs3:                                                                        # rail-gun barrel
            rod(m, bd, (-6.0, 44.0, 4.0), (-24.0, 40.0, 14.0), 3, DARK, extend=0.4)
        tb = m.bone("tail", bd, (0, 32, 3))                                             # spined tail
        pts = [(0, 32.0, 3.0), (0, 26.0, 12.0), (0, 20.0, 20.0), (0, 16.0, 28.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, tb, p0, p1, 6 - j * 2, CHROME, extend=0.6)
            spike(m, tb, p0, (0, 1, 0.4), 1.6, 4.0, STEEL, tip=0.8)
        return m

    return build
