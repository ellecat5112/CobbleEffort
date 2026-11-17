"""Shared builder for Dark Knightmon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): the black
knight. A tall knight in black plate trimmed in gold with a horned gold-crested helm and gold face guard, a great black
crescent shield-wing on its back, pointed gold sabatons and a long black-and-red lance with a steel guard.
make(x=True): the X-Antibody form, a lurid violet-and-gold knight with neon pink and green seams, a skull face, a
tattered crimson cape, a glowing green spear and a huge curved white scythe-blade. Shiny: white plate.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import cape, dome, humanoid
from _digidetail import armour, fabric, local, metal, solid
from _route import pal, tone

BASE = {"black": (40, 40, 52), "black_dark": (14, 14, 20), "black_light": (110, 110, 130), "gold": (236, 190, 60),
        "gold_dark": (160, 110, 20), "red": (200, 30, 40), "red_dark": (110, 10, 18), "steel": (210, 214, 226),
        "steel_dark": (110, 114, 128), "violet": (100, 60, 150), "violet_dark": (40, 20, 70), "pink": (250, 60, 180),
        "green": (90, 250, 120), "skull": (230, 224, 210), "eye": (250, 60, 60), "under": (24, 24, 30)}
SHINY = {"black": (230, 230, 240), "black_dark": (150, 150, 170), "black_light": (255, 255, 255),
         "violet": (220, 220, 236), "violet_dark": (140, 140, 160)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = metal(P, "gold", dark="gold_dark")
STEEL = metal(P, "steel", dark="steel_dark")


def make(name, x=False):
    PLATE = armour(P, "violet" if x else "black", "violet_dark" if x else "black_dark", light="black_light",
                   trim="gold", trim_w=0.35, glow_key="pink" if x else None)

    def build():
        m = Model(name)
        mats = {"skin": solid(P, "under"), "chest": PLATE, "abs": PLATE, "pelvis": PLATE, "deltoid": PLATE,
                "upper_arm": PLATE, "forearm": PLATE, "hand": PLATE, "finger": GOLD, "claw": GOLD, "thigh": PLATE,
                "knee": GOLD, "shin": PLATE, "calf": PLATE, "foot": GOLD, "toe": GOLD}
        a = humanoid(m, mats, bulk=1.05, arm_bulk=1.05, leg_bulk=1.05, name=name, hand_pose="fist")
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.2, 2.8, 3.0, 54.0, 61.0, PLATE, cut=1)
        if x:
            m.box(hd, -2.2, 54.6, -3.4, 2.2, 58.6, -3.0, solid(P, "skull"))           # skull face
            m.box(hd, -1.8, 57.2, -3.5, 1.8, 57.8, -3.4, solid(P, "green", glow=True))
        else:
            m.box(hd, -2.0, 54.6, -3.6, 2.0, 57.0, -3.0, GOLD)                        # gold face guard
            m.box(hd, -2.0, 57.4, -3.4, 2.0, 58.0, -3.1, solid(P, "eye", glow=True))
        for sx in (-1, 1):                                                           # horned crest
            spike(m, hd, (sx * 2.2, 60.0, 0), (sx * 0.6, 1, -0.2), 1.6, 7.0 if x else 5.0, GOLD, tip=0.3)
        spike(m, hd, (0, 60.8, -1.4), (0, 1, -0.4), 1.4, 4.0, GOLD, tip=0.3)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            dome(m, a[nm]["bone"], (a[nm]["shoulder"][0] + sx * 1.8, 49.4, 0.3), 4.4, 4.2, PLATE, layers=4)
            spike(m, a[nm]["bone"], (a[nm]["shoulder"][0] + sx * 3.0, 51.0, 0.3), (sx, 0.8, 0), 1.6, 5.0, GOLD)
        wb = m.bone("wings", bd, (0, 48, 4))                                          # crescent shield-wing
        for sx in (-1, 1):
            pts = []
            for i in range(8):
                ang = math.radians(-10 + i * 22)
                pts.append((sx * (4.0 + 12.0 * math.sin(ang) * 1.2), 48.0 + 14.0 * math.cos(ang) * 0.9 - 4.0,
                            6.0 + i * 0.4))
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, wb, p0, p1, 2, PLATE, extend=0.4, t2=5)
        if x:
            cb = m.bone("cap", bd, (0, 52, 3))
            cape(m, cb, 52.0, 18.0, 40.0, fabric(P, "red", "red_dark"), z=4.4, flare=1.2, panels=8, sweep=(0, 6),
                 seed=13)
        ar = a["arm_right"]                                                           # lance / glowing spear
        h = ar["hand"]
        lb = m.bone("lance", ar["bone"], h)
        tip = (h[0] - 10.0, h[1] + 24.0, h[2] - 20.0)
        n = math.dist(h, tip)
        u = tuple((t - b) / n for t, b in zip(tip, h))
        if x:
            rod(m, lb, tuple(b - c * 8.0 for b, c in zip(h, u)), tip, 1, solid(P, "green", glow=True), extend=0)
            spike(m, lb, tip, u, 2.4, 6.0, solid(P, "pink", glow=True), tip=0.4)
            al = a["arm_left"]                                                        # the huge scythe-blade
            g = al["hand"]
            pts = []
            for i in range(9):
                ang = math.radians(-60 + i * 18)
                pts.append((g[0] + 6.0, g[1] + 14.0 * math.sin(ang) + 4.0, g[2] - 12.0 * math.cos(ang) + 4.0))
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, al["bone"], p0, p1, 1, STEEL, extend=0.4, t2=4)
        else:
            steps = 6
            for i in range(steps):
                p0 = tuple(b + (t - b) * i / steps for b, t in zip(h, tip))
                p1 = tuple(b + (t - b) * (i + 1) / steps for b, t in zip(h, tip))
                rod(m, lb, p0, p1, max(1, round(4 * (1 - i / steps))), solid(P, "red" if i % 2 else "black"),
                    extend=0.3)
            m.round_box(lb, h[0], h[2], 2.6, 2.6, h[1] - 0.6, h[1] + 1.4, STEEL, cut=1)
        return m
    return build
