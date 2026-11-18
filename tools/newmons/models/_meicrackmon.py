"""Shared builder for Meicrackmon and Meicrackmon: Vicious Mode (CobbleEffort: Digital; hand-built after the official
art on wikimon.net): a slender cat warrior in a golden-orange fur bodysuit striped black, a great white fluffy collar
over its chest, a cat face framed by orange hair, its two ribbon ears looping up over its head into a heart, paws
glowing with pink orbs, dark armoured boots and a long ribbon tail. Vicious Mode ("vicious"): a wilder white mane,
black armour on its forearms and shins, long red claws trailing red slashes, its ribbons crackling dark and its tail
burning at the tip.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, cutout, flame_inside, gem, local, solid
from _meicoo import FUR, P, WHITE, cat_eye, ribbon, striped
from _route import tone


def make(name, vicious=False):
    SUIT = striped(FUR, period=4.0, width=0.35)
    BOOT = armour(P, "black", "black", trim="eye", trim_w=0.2)

    def slashf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        c = (*p["red"], 200)
        return c, p["red"]

    def firef(x, y, z, face, variant, box=None, **k):
        c = (255, 140, 40, 215)
        return c, c[:3]

    def build():
        m = Model(name)
        mats = {"skin": SUIT, "chest": SUIT, "abs": SUIT, "pelvis": SUIT, "neck": WHITE, "deltoid": SUIT,
                "upper_arm": SUIT, "forearm": BOOT if vicious else SUIT, "hand": WHITE, "finger": WHITE,
                "claw": solid(P, "red" if vicious else "claw"), "thigh": SUIT, "knee": SUIT, "shin": BOOT,
                "calf": BOOT, "foot": BOOT, "talon": solid(P, "red" if vicious else "claw")}
        a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=1.0, claws=True, talons=True, digitigrade=True,
                     name=name)
        bd = a["body"]
        n = 14 if vicious else 10                                                          # great white collar
        for ring, (r, y) in enumerate(((5.4, 50.0), (4.6, 46.0))):
            for i in range(n):
                ang = math.radians(-90 + 180 * (i + 0.5) / n)
                spike(m, bd, (r * math.sin(ang), y, -r * 0.6 * math.cos(ang)),
                      (math.sin(ang) * 0.6, -0.6 - ring * 0.2, -math.cos(ang)), 2.4, 5.0 + (1.6 if vicious else 0),
                      WHITE, tip=0.8)
        hd = m.bone("head", bd, (0, 55, 0))
        ball(m, hd, (0, 58.0, -0.2), 3.0, SUIT, layers=4, ry=3.2)
        m.round_box(hd, 0, -2.6, 1.6, 0.8, 55.6, 57.6, WHITE, cut=0)                       # white muzzle
        for sx in (-1, 1):
            cat_eye(m, hd, sx * 0.4, 58.0, -3.15, sx, w=1.4, h=1.2)
            spike(m, hd, (sx * 2.0, 60.6, 0.0), (sx * 0.4, 1, 0), 1.6, 2.4, FUR, tip=0.8)  # cat ears
            for j in range(4 if not vicious else 6):                                       # hair / mane locks
                spike(m, hd, (sx * 2.6, 59.0 - j * 1.4, 0.6), (sx * 0.8, -0.6, 0.5), 1.4, 4.0 + j * 0.5,
                      WHITE if vicious else FUR, tip=0.8)
        rb = m.bone("ears", hd, (0, 60, 1))                                                # ribbon heart loops
        for sx in (-1, 1):
            pts = [(sx * 1.6, 60.0, 1.0)]
            for i in range(1, 9):
                t = i / 8
                ang = math.radians(200 * t)
                pts.append((sx * (5.0 + 8.0 * math.sin(ang * 0.9)), 62.0 + 14.0 * math.sin(math.radians(170 * t)),
                            1.0 + 2.0 * t))
            pts.append((sx * 0.8, 64.0, 4.0))
            ribbon(m, rb, pts, 2)
        for nm in ("arm_left", "arm_right"):
            hnd = a[nm]["hand"]
            if not vicious:                                                                # glowing pink orbs
                ball(m, a[nm]["bone"], (hnd[0], hnd[1] - 1.0, hnd[2] - 2.6), 1.8, gem(P, "orb", "pink"), layers=3)
            else:                                                                          # red claw slashes
                sx = 1 if hnd[0] > 0 else -1
                for j in range(3):
                    x0, x1 = sorted((hnd[0] + sx * 1.0, hnd[0] + sx * 14.0))
                    m.box(a[nm]["bone"], x0, hnd[1] - 4.0 + j * 1.6, hnd[2] - 3.0 - j, x1, hnd[1] - 3.0 + j * 1.6,
                          hnd[2] - 3.0 - j, slashf, rotation=(0, 0, -sx * 30), pivot=(hnd[0], hnd[1] - 3.0, hnd[2]))
        tb = m.bone("tail", bd, (0, 32, 3))                                                # long ribbon tail
        pts = [(0, 32.0, 3.0), (2.0, 26.0, 9.0), (6.0, 20.0, 12.0), (8.0, 12.0, 10.0), (5.0, 6.0, 12.0),
               (8.0, 2.0, 14.0)]
        ribbon(m, tb, pts, 2, claw=not vicious)
        if vicious:
            e = pts[-1]
            for ang in (0, 90):
                m.box(tb, e[0] - 2.4, e[1], e[2], e[0] + 2.4, e[1] + 6.0, e[2], cutout(flame_inside(4, 0.1, 2), firef),
                      rotation=(0, ang, 0), pivot=e)
        return m

    return build
