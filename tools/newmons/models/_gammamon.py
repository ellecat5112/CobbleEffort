"""Shared builder for the Gammamon line (CobbleEffort: Digital; hand-built after the official art on wikimon.net).
Gammamon (Child): a fluffy white little beast with three grey horns tipped red, big yellow eyes, a blue bandana, a red
band on its leg, a blue-flamed tail and violet claws. Gulus Gammamon (Adult): the same spirit grown into a lean,
upright white dragon-man with long horns, a blue scarf trailing like flame, violet claws and red bands.
Shiny: black fur with orange accents.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import humanoid
from _digidetail import cutout, fabric, flame_inside, fur, local, solid
from _route import pal, tone

BASE = {"white": (246, 246, 250), "white_dark": (190, 194, 210), "horn": (170, 170, 180), "red": (220, 40, 50),
        "eye": (250, 210, 40), "pupil": (20, 20, 24), "blue": (50, 90, 200), "blue_dark": (20, 40, 120),
        "violet": (60, 40, 150), "tongue": (240, 100, 120), "mouth": (120, 20, 30), "fire": (90, 160, 255, 220),
        "fire_core": (220, 240, 255, 240)}
SHINY = {"white": (50, 50, 58), "white_dark": (20, 20, 26), "blue": (240, 120, 30), "blue_dark": (160, 60, 10),
         "fire": (255, 150, 40, 220)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "white", "white_dark", length=1.0, density=2.2)
SCARF = fabric(P, "blue", "blue_dark")


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
    return c, c[:3]


def flame(m, bone, at, w, h, seed):
    for ang in (0, 90):
        m.box(bone, at[0] - w / 2, at[1], at[2], at[0] + w / 2, at[1] + h, at[2],
              cutout(flame_inside(4, 0.2, seed), firef), rotation=(0, ang, 0), pivot=at)


def horn(m, bone, at, d, w, h):
    spike(m, bone, at, d, w, h * 0.7, solid(P, "horn"), tip=None)
    n = math.sqrt(sum(v * v for v in d))
    tip_at = tuple(a + v / n * h * 0.7 for a, v in zip(at, d))
    spike(m, bone, tip_at, d, max(0.8, w * 0.6), h * 0.3, solid(P, "red"))


def make(name, stage):
    def build():
        m = Model(name)
        if stage == "child":
            top = m.bone(name, None, (0, 0, 0))
            bd = m.bone("body", top, (0, 8, 0))
            m.round_box(bd, 0, 0.4, 4.0, 3.4, 6.0, 16.0, FUR, cut=2)
            m.round_box(bd, 0, -0.4, 4.4, 3.8, 14.4, 16.6, SCARF, cut=1)                 # blue bandana
            spike(m, bd, (0, 15.0, -3.8), (0, -1, -0.4), 2.4, 3.0, SCARF, tip=1.0)
            hd = m.bone("head", bd, (0, 17, -1))
            m.round_box(hd, 0, -1.0, 5.0, 4.4, 16.0, 25.0, FUR, cut=2)
            for sx in (-1, 1):
                m.round_box(hd, sx * 2.2, -5.4, 1.4, 0.4, 19.6, 22.8, solid(P, "eye"), cut=0)
                m.box(hd, sx * 2.2 - 0.4, 20.2, -5.9, sx * 2.2 + 0.4, 22.0, -5.7, solid(P, "pupil"))
                horn(m, hd, (sx * 3.2, 24.0, 0), (sx * 0.5, 1, 0.1), 1.8, 4.6)
            horn(m, hd, (0, 24.6, -1.0), (0, 1, -0.2), 2.0, 5.4)
            m.box(hd, -1.6, 17.4, -5.6, 1.6, 18.8, -5.2, solid(P, "mouth"))
            m.box(hd, -0.8, 16.8, -5.7, 0.8, 17.6, -5.3, solid(P, "tongue"))
            for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
                ab = m.bone(nm, bd, (sx * 4.0, 13.0, -1.0))
                rod(m, ab, (sx * 4.0, 13.0, -1.0), (sx * 7.0, 8.0, -4.0), 2, FUR, extend=0.4)
                for j in range(3):
                    spike(m, ab, (sx * 7.0 + (j - 1) * 0.9, 7.6, -4.6), (sx * 0.3, -0.5, -1), 0.8, 2.6,
                          solid(P, "violet"), tip=0.8)
            for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
                lg = m.bone(nm, top, (sx * 2.2, 8.0, 0))
                rod(m, lg, (sx * 2.2, 8.0, 0), (sx * 2.4, 1.6, -0.6), 2, FUR, extend=0.4, t2=3)
                m.round_box(lg, sx * 2.4, -0.6, 1.6, 1.6, 4.0, 5.0, solid(P, "red"), cut=0)
                for j in range(3):
                    spike(m, lg, (sx * 2.4 + (j - 1) * 1.0, 0.6, -2.4), (0, 0, -1), 0.8, 2.0, solid(P, "violet"),
                          tip=0.8)
            tb = m.bone("tail", bd, (0, 9, 3))
            rod(m, tb, (0, 9.0, 3.0), (3.0, 14.0, 8.0), 2, FUR, extend=0.4)
            flame(m, tb, (3.0, 14.0, 8.0), 3.0, 5.0, 4)
            return m
        mats = {"skin": FUR, "claw": solid(P, "violet"), "talon": solid(P, "violet")}             # Gulus Gammamon
        a = humanoid(m, mats, bulk=0.85, arm_bulk=0.95, leg_bulk=1.0, claws=True, talons=True, digitigrade=True,
                     name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -1.0, 2.8, 3.4, 53.4, 60.0, FUR, cut=1)
        m.round_box(hd, 0, -5.0, 1.8, 1.6, 53.6, 56.6, FUR, cut=1)
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.8, sx * 2.2), 57.2, -4.5, max(sx * 0.8, sx * 2.2), 58.0, -4.3, solid(P, "eye"))
            horn(m, hd, (sx * 2.2, 59.4, 0), (sx * 0.4, 1, 0.5), 1.6, 9.0)
        horn(m, hd, (0, 60.0, -1.0), (0, 1, 0.2), 1.8, 7.0)
        m.round_box(bd, 0, 0.0, 5.0, 4.0, 50.0, 52.6, SCARF, cut=1)                              # scarf
        pts = [(1.0, 51.0, 3.6), (6.0, 52.0, 10.0), (12.0, 50.0, 14.0), (18.0, 53.0, 16.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, bd, p0, p1, 1, SCARF, extend=0.4, t2=4 - j)
        for nm in ("arm_left", "arm_right", "leg_left", "leg_right"):                               # red bands
            jt = a[nm].get("wrist") or a[nm].get("ankle")
            m.round_box(a[nm]["bone"], jt[0], jt[2], 1.8, 1.8, jt[1] + 1.0, jt[1] + 2.2, solid(P, "red"), cut=0)
        tb = m.bone("tail", bd, (0, 32, 3))
        pts = [(0, 32.0, 3.0), (2.0, 24.0, 10.0), (5.0, 20.0, 17.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, tb, p0, p1, 2, FUR, extend=0.4)
        flame(m, tb, pts[-1], 5.0, 8.0, 6)
        return m

    return build
