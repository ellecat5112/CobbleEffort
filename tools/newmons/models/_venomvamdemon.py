"""Shared builder for Venom Vamdemon and Venom Vamdemon Undead (CobbleEffort: Digital; hand-built after the official art
on wikimon.net): Vamdemon's monstrous true form: a towering red demon with an exposed ribbed chest streaked with
violet, a small horned head with a mane of wild blond hair, great tattered black-and-red bat wings, huge shaggy brown
furred legs ending in pale lilac claws, long arms with giant clawed red hands (one marked with a bat sigil) and a
whip tail. Undead: darker and rotting, shredded wings trailing smoke, sickly grey-blue claws and pale bone streaks.
Shiny: violet / grey-green."""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, bat_wing
from _digibody import humanoid
from _digidetail import fur, plane, skin, solid, strands
from _route import pal, tone

LOOKS = {False: {"red": (190, 40, 40), "red_dark": (110, 14, 14), "fur": (110, 80, 60), "fur_dark": (60, 40, 26),
                 "claw": (210, 190, 240), "streak": (130, 80, 200)},
         True: {"red": (120, 30, 40), "red_dark": (50, 10, 14), "fur": (80, 70, 70), "fur_dark": (36, 30, 30),
                "claw": (170, 180, 210), "streak": (220, 220, 210)}}
COMMON = {"wing": (40, 36, 46), "membrane": (120, 30, 40, 220), "hair": (240, 220, 140), "hair_dark": (180, 150, 70),
          "eye": (250, 230, 80), "smoke": (90, 86, 96, 140), "bat": (240, 200, 60)}
SHINY = {"red": (120, 60, 160), "red_dark": (60, 24, 90), "membrane": (80, 40, 120, 220)}


def make(name, undead=False):
    base = dict(COMMON, **LOOKS[undead])

    def P(v):
        return pal(base, SHINY, v)

    def redf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face in ("north", "south") and abs((x * 0.8 + y * 0.6) % 6.0 - 3.0) < 0.35:
            return tone(p["streak"], face), None
        if face == "north" and 40.0 < y < 52.0 and abs(x) < 5.0 and (y % 2.4) < 0.6:
            return tone(p["red_dark"], face), None                                     # ribs
        return skin(P, "red", dark="red_dark")(x, y, z, face, variant, box=box, **k)

    FUR = fur(P, "fur", "fur_dark", length=2.0)

    def build():
        m = Model(name)
        mats = {"skin": redf, "chest": redf, "abs": redf, "pelvis": FUR, "deltoid": redf, "upper_arm": redf,
                "forearm": redf, "hand": redf, "finger": redf, "claw": solid(P, "claw"), "thigh": FUR, "knee": FUR,
                "shin": FUR, "calf": FUR, "foot": FUR, "talon": solid(P, "claw"), "neck": redf}
        a = humanoid(m, mats, bulk=1.35, arm_bulk=1.4, leg_bulk=1.6, claws=True, talons=True, name=name)
        bd = a["body"]
        for nm in ("leg_left", "leg_right"):                                            # shaggy leg mass
            k = a[nm]["knee"]
            m.round_box(a[nm]["bone"], k[0], k[2], 4.4, 4.4, 4.0, 26.0, FUR, cut=2)
            ank = a[nm]["ankle"]
            for t in range(4):
                spike(m, a[nm]["bone"], (ank[0] + (t - 1.5) * 1.8, 1.2, ank[2] - 3.4), (0, -0.3, -1), 1.6, 4.0,
                      solid(P, "claw"), tip=0.8)
        for nm in ("arm_left", "arm_right"):                                            # giant clawed hands
            h = a[nm]["hand"]
            ball(m, a[nm]["bone"], h, 3.4, redf, layers=3)
            for t in range(4):
                ang = (t - 1.5) * 0.5
                spike(m, a[nm]["bone"], (h[0] + math.sin(ang) * 2.4, h[1] - 2.4, h[2] - 1.0), (math.sin(ang), -1, -0.4),
                      1.2, 5.0, solid(P, "claw"), tip=0.8)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, 0, 2.6, 3.0, 54.0, 60.0, redf, cut=1)
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.6, sx * 1.8), 57.6, -3.4, max(sx * 0.6, sx * 1.8), 58.4, -3.1, solid(P, "eye", glow=True))
            spike(m, hd, (sx * 2.0, 59.6, 0), (sx * 0.6, 1, 0.2), 1.0, 5.0, redf, tip=0.8)
        for j in range(9):
            ang = (j - 4) * 0.4
            spike(m, hd, (math.sin(ang) * 2.4, 59.0, 1.6), (math.sin(ang) * 0.8, 0.2 - abs(ang) * 0.3, 1), 1.6, 8.0,
                  strands(P, "hair", "hair_dark"), tip=0.8)
        for sx in (-1, 1):                                                              # bat wings
            wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 4.0, 50.0, 4.0))
            bat_wing(m, wb, (sx * 4.0, 50.0, 4.0), 32.0, 30.0, 4, solid(P, "wing"), solid(P, "membrane"), side=sx,
                     sweep=10)
        tl = m.bone("tail", bd, (0, 30, 4))
        pts = [(0, 30.0, 4.0), (4.0, 20.0, 10.0), (10.0, 12.0, 12.0), (16.0, 10.0, 10.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, tl, p0, p1, 1, redf, extend=0.3)
        if undead:
            sm = m.bone("smoke", bd, (0, 40, 6))
            for j in range(8):
                ang = j * 0.8
                ball(m, sm, (14.0 * math.cos(ang), 30.0 + j * 4.0, 8.0 + 3.0 * math.sin(ang)), 3.0, solid(P, "smoke"),
                     layers=1)
        return m
    return build
