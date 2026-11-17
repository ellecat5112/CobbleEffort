"""Shared builder for the Galgomon line (CobbleEffort: Digital; hand-built after the official art on wikimon.net):
Galgomon (Adult), Rapidmon (Perfect), Saint Galgomon (Ultimate), in their usual colours or as the Black versions.

Galgomon: a rabbit-eared dog-gunner with gatling-barrel arms, a belt and baggy trousers and big clawed feet.
Rapidmon: armoured, with rocket ears tipped red, cannon arms and a round hip plate. Saint Galgomon: a heavy armoured
mech with missile pods and a rabbit-faced warhead on its back, gatlings on its arms and spiked steel bands.
Black: dark green-grey hide and grey armour; shiny = the usual green-and-gold.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digibody import dome, humanoid, shell
from _digidetail import armour, fabric, fur, leather, metal, riveted, solid
from _route import pal, tone

GREEN = {"hide": (90, 170, 90), "hide_dark": (40, 100, 40), "armour": (110, 170, 80), "armour_dark": (50, 100, 30),
         "ear": (240, 200, 60), "pants": (60, 120, 200), "pants_dark": (24, 60, 130)}
BLACK = {"hide": (60, 70, 70), "hide_dark": (26, 32, 32), "armour": (80, 84, 92), "armour_dark": (34, 36, 42),
         "ear": (220, 180, 80), "pants": (60, 110, 60), "pants_dark": (24, 60, 24)}
COMMON = {"steel": (210, 214, 226), "steel_dark": (110, 114, 128), "red": (220, 40, 40), "tan": (200, 160, 100),
          "tan_dark": (140, 100, 50), "claw": (240, 240, 244), "eye": (255, 60, 60), "black": (30, 30, 36),
          "belt": (110, 70, 40), "warhead": (220, 60, 50)}


def make(name, stage, black=True):
    base = dict(COMMON, **(BLACK if black else GREEN))
    shiny = dict(COMMON, **(GREEN if black else BLACK))

    def P(v):
        return pal(base, shiny, v)

    HIDE = fur(P, "hide", "hide_dark", length=1.0)
    ARM = armour(P, "armour", "armour_dark", light="steel")
    STEEL = metal(P, "steel", dark="steel_dark")
    PANTS = fabric(P, "pants", "pants_dark", axis="y", period=2.4)

    def gatling(m, bone, c, d, length, r=2.0):
        n = math.sqrt(sum(q * q for q in d))
        u = tuple(q / n for q in d)
        m.round_box(bone, c[0], c[2], r + 0.6, r + 0.6, c[1] - r - 0.6, c[1] + r + 0.6, STEEL, cut=1)
        for i in range(6):
            ang = math.radians(i * 60)
            o = (c[0] + r * 0.6 * math.cos(ang), c[1] + r * 0.6 * math.sin(ang), c[2])
            rod(m, bone, o, tuple(oo + uu * length for oo, uu in zip(o, u)), 1, STEEL, extend=0)

    def build():
        m = Model(name)
        if stage == "adult":
            mats = {"skin": HIDE, "chest": HIDE, "abs": HIDE, "pelvis": PANTS, "thigh": PANTS, "knee": PANTS,
                    "shin": PANTS, "calf": PANTS, "foot": fur(P, "tan", "tan_dark"), "talon": solid(P, "claw"),
                    "hand": STEEL, "finger": STEEL}
            a = humanoid(m, mats, bulk=0.95, arm_bulk=1.0, leg_bulk=1.2, talons=True, name=name, hand_pose="fist")
            bd = a["body"]
            m.box(bd, -4.8, 31.0, -4.2, 4.8, 33.0, 4.0, leather(P, "belt", "black"))
            for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
                gatling(m, a[nm]["bone"], a[nm]["hand"], (sx * 0.3, 0.0, -1.0), 9.0)
        elif stage == "perfect":
            mats = {"skin": HIDE, "chest": ARM, "abs": ARM, "pelvis": ARM, "deltoid": ARM, "forearm": STEEL,
                    "hand": STEEL, "finger": STEEL, "thigh": fur(P, "tan", "tan_dark"), "knee": STEEL, "shin": STEEL,
                    "calf": STEEL, "foot": STEEL, "talon": STEEL}
            a = humanoid(m, mats, bulk=1.0, arm_bulk=1.1, leg_bulk=1.1, talons=True, name=name, hand_pose="fist")
            bd = a["body"]
            ball(m, bd, (0, 30.0, -1.0), 5.6, ARM, layers=4)
            for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
                h = a[nm]["hand"]
                m.round_box(a[nm]["bone"], h[0], h[2], 2.6, 2.6, h[1] - 3.0, h[1] + 3.0, ARM, cut=1)
                for j in range(3):
                    ang = math.radians(j * 120)
                    spike(m, a[nm]["bone"], (h[0] + 2.4 * math.cos(ang), h[1] + 2.4 * math.sin(ang), h[2]),
                          (math.cos(ang), math.sin(ang), -0.4), 1.2, 3.0, solid(P, "red"))
        else:
            mats = {"skin": STEEL, "chest": riveted(P, "armour", "armour_dark"), "abs": ARM, "pelvis": ARM,
                    "deltoid": ARM, "upper_arm": STEEL, "forearm": ARM, "hand": STEEL, "finger": STEEL, "thigh": ARM,
                    "knee": STEEL, "shin": ARM, "calf": ARM, "foot": ARM, "toe": STEEL}
            a = humanoid(m, mats, bulk=1.4, arm_bulk=1.5, leg_bulk=1.6, name=name, hand_pose="fist")
            bd = a["body"]
            for sx in (-1, 1):                                   # missile pods on its back
                rod(m, bd, (sx * 6.0, 40.0, 6.0), (sx * 10.0, 66.0, 12.0), 6, ARM, extend=0)
                ball(m, bd, (sx * 10.4, 67.0, 12.4), 3.6, solid(P, "warhead"), layers=3)
            for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
                gatling(m, a[nm]["bone"], a[nm]["hand"], (sx * 0.2, 0.0, -1.0), 10.0, r=2.6)
                kn = a[nm.replace("arm", "leg")]["knee"]
                m.round_box(a[nm.replace("arm", "leg")]["bone"], kn[0], kn[2], 3.6, 3.6, 10.0, 13.0, STEEL, cut=1)
                for j in range(4):
                    ang = math.radians(j * 90 + 45)
                    spike(m, a[nm.replace("arm", "leg")]["bone"], (kn[0] + 3.6 * math.cos(ang), 11.5,
                          kn[2] + 3.6 * math.sin(ang)), (math.cos(ang), 0, math.sin(ang)), 1.0, 2.0, STEEL)
        hd = m.bone("head", a["body"], (0, 55, 0))
        m.round_box(hd, 0, -0.6, 2.6, 2.8, 54.4, 60.4, ARM if stage != "adult" else HIDE, cut=1)
        m.box(hd, -1.6, 54.6, -5.0, 1.6, 57.0, -2.8, HIDE)
        for sx in (-1, 1):
            m.box(hd, sx * 1.2 - 0.5, 57.8, -3.5, sx * 1.2 + 0.5, 58.6, -3.3, solid(P, "eye", glow=True))
            ear = m.bone("ear_left" if sx > 0 else "ear_right", hd, (sx * 1.6, 60.0, 0))
            tip = (sx * 9.0, 72.0, 4.0) if stage != "ultimate" else (sx * 5.0, 66.0, 2.0)
            rod(m, ear, (sx * 1.6, 60.0, 0.0), tip, 3, fur(P, "ear", "tan_dark") if stage == "adult" else ARM,
                extend=0.4, t2=2)
            if stage == "perfect":
                spike(m, ear, tip, (sx * 0.6, 1, 0.3), 2.0, 3.0, solid(P, "red"))
        return m
    return build
