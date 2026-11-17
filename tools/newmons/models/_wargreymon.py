"""Shared builder for War Greymon-type Digimon (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): a dragon-man in Chrome Digizoid armour with a dragon-skull helm, a wild mane of spiky hair, gauntlets
ending in three long claws (Dramon Destroyers), a round shield split in two on its back (Brave Shield), a dinosaur
tail and clawed feet.

Variants: "black" (Black War Greymon: black armour with gold trim, a golden mane), "blackx" (the X-Antibody form: the
shield halves opened into blade-wings, glowing red seams), "erosion" (Black War Greymon "G" Erosion Mode: violet-black
corrupted armour with tall glowing violet dorsal spines down its back and a long spined tail).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import dome, humanoid, shell
from _digidetail import armour, gem, metal, skin, solid, strands
from _route import pal, tone

BASE = {"armour": (50, 50, 58), "armour_dark": (16, 16, 20), "armour_light": (140, 142, 160), "gold": (236, 196, 60),
        "gold_dark": (160, 120, 30), "gold_light": (255, 240, 170), "hair": (250, 220, 80), "hair_dark": (200, 150, 30),
        "skin": (60, 56, 60), "skin_dark": (24, 22, 26), "claw": (220, 224, 236), "claw_dark": (110, 114, 128),
        "red": (230, 30, 40), "violet": (190, 90, 240), "violet_dark": (90, 30, 140), "eye": (255, 60, 60)}
SHINY = {"armour": (210, 210, 224), "armour_dark": (130, 130, 146), "armour_light": (255, 255, 255),
         "hair": (240, 120, 60), "hair_dark": (180, 60, 20), "violet": (90, 220, 160), "violet_dark": (30, 120, 80),
         "red": (60, 160, 255)}


def P(v):
    return pal(BASE, SHINY, v)


EROSION = {"armour": (56, 40, 70), "armour_dark": (18, 10, 26), "armour_light": (150, 120, 180)}


def make(name, variant="black"):
    def P(v):
        return pal(dict(BASE, **(EROSION if variant == "erosion" else {})), SHINY, v)

    ARM = armour(P, "armour", "armour_dark", light="armour_light", trim="gold", trim_w=0.35,
                 glow_key="red" if variant == "blackx" else ("violet" if variant == "erosion" else None))
    ARM_PLAIN = armour(P, "armour", "armour_dark", light="armour_light")
    SKIN = skin(P, "skin", dark="skin_dark")
    CLAW = metal(P, "claw", dark="claw_dark")
    GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")
    HAIR = strands(P, "hair", "hair_dark")

    def build():
        m = Model(name)
        mats = {"skin": SKIN, "chest": ARM, "abs": SKIN, "pelvis": ARM, "neck": SKIN, "deltoid": ARM,
                "upper_arm": SKIN, "forearm": ARM, "hand": ARM, "finger": ARM_PLAIN, "thigh": ARM, "knee": GOLD,
                "shin": ARM, "calf": ARM_PLAIN, "foot": ARM, "talon": CLAW}
        bulk = 1.4 if variant == "erosion" else 1.2
        a = humanoid(m, mats, bulk=bulk, arm_bulk=bulk * 1.05, leg_bulk=bulk * 1.05, digitigrade=True, talons=True,
                     name=name, hand_pose="fist")
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.8, 2.8, 3.0, 54.4, 61.0, ARM, cut=1)
        m.box(hd, -2.0, 54.6, -7.0, 2.0, 57.8, -3.0, ARM)                                # dragon-skull snout
        m.box(hd, -2.0, 58.0, -3.9, 2.0, 58.8, -3.5, solid(P, "eye", glow=True))
        for sx in (-1, 1):
            spike(m, hd, (sx * 2.6, 60.0, -1.0), (sx * 0.3, 0.5, 1), 1.4, 5.0, GOLD, tip=0.6)
        spike(m, hd, (0, 61.0, -4.0), (0, 1, -0.3), 1.6, 3.0, ARM)
        mane = m.bone("mane", hd, (0, 60, 2))
        for i in range(14):                                      # the wild spiky mane
            ang = math.radians(-90 + i * (180 / 13))
            base = (2.6 * math.sin(ang), 60.0 + math.cos(ang), 1.6)
            tip = (base[0] * 2.6, base[1] + 4.0 * math.cos(ang) + 2.0, 8.0 + (i % 3) * 2)
            rod(m, mane, base, tip, 2, HAIR, extend=0.3, t2=2)
        shell(m, bd, (0, 0, 0.6), 6.0, 41.0, 51.0, -85, 85, 9, 1.3, ARM)
        m.box(bd, -1.4, 44.0, -7.6, 1.4, 48.0, -6.4, gem(P, "red", "gold_light"))          # chest crest
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab, sh = a[nm]["bone"], a[nm]["shoulder"]
            dome(m, ab, (sh[0] + sx * 1.8, 50.0, 0.3), 4.8, 4.4, ARM, layers=4)
            h = a[nm]["hand"]                                    # Dramon Destroyers
            m.round_box(ab, h[0], h[2], 3.4, 3.4, h[1] - 3.0, h[1] + 4.0, ARM, cut=1)
            for f in range(3):
                spike(m, ab, (h[0] + (f - 1) * 1.6, h[1] - 3.0, h[2] - 1.0), (sx * 0.1, -1, -0.5), 1.4, 9.0, CLAW,
                      tip=0.5)
        sb = m.bone("shield", bd, (0, 46, 6))                    # Brave Shield halves on its back
        for sx in (-1, 1):
            if variant == "blackx":                              # opened into blade-wings
                for j in range(3):
                    rod(m, sb, (sx * 3.0, 48.0, 6.0), (sx * (18.0 + j * 2), 58.0 - j * 8, 10.0 + j), 2, CLAW,
                        extend=0.3, t2=5)
            else:
                for j in range(5):
                    ang = math.radians(-60 + j * 30)
                    c = (sx * (2.0 + 6.0 * abs(math.cos(ang)) * 0.6), 44.0 + 9.0 * math.sin(ang), 7.0)
                    m.box(sb, min(sx * 0.8, c[0] + sx * 2.0), c[1] - 2.0, 6.4, max(sx * 0.8, c[0] + sx * 2.0),
                          c[1] + 2.0, 7.6, ARM)
        tl = m.bone("tail", bd, (0, 31, 3))
        n = 6 if variant == "erosion" else 4
        pts = [(0, 31.0, 3.0)] + [(j * 1.6, 28.0 - j * 4.0, 6.0 + j * 4.0) for j in range(1, n + 1)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, tl, p0, p1, max(1, 5 - j), ARM_PLAIN, extend=0.5)
        if variant == "erosion":                                 # glowing violet dorsal spines
            for j in range(9):
                t = j / 8
                p = (0, 56.0 - 30.0 * t, 4.0 + 2.0 * t)
                spike(m, bd, p, (0, 0.6, 1), 2.4 - t, 6.0 - 2.0 * t, gem(P, "violet", "violet_dark"), tip=0.8)
            for p in pts[1:-1]:
                spike(m, tl, p, (0, 1, 0.4), 1.6, 3.6, gem(P, "violet", "violet_dark"))
        return m
    return build
