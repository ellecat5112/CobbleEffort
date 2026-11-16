"""Arresterdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a sly dragon-man. Violet scales, a dragon head with swept-back blue spines, a crimson chest guard,
a long dark coat with rolled sleeves, baggy dark trousers, orange gauntlets and boots, white claws, and a long tail
ending in a steel anchor-hook. 15 blocks tall.

Front is -z, y is up. 62 units tall; Adult stage. make("superior"): Arresterdramon: Superior Mode (red-and-yellow chest
armour, huge tattered yellow wings, a gold trident tail, 25 blocks); make("brave"): Superior Mode (Brave Snatcher)
(a huge crimson claw gauntlet with a gold ring on its right arm, 35 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import dome, humanoid, shell
from _digidetail import armour, cutout, fabric, leather, local, metal, scales, solid
from _route import pal, tone

HEIGHT = 62
SCALE, HITBOX = sized(15, HEIGHT, 1.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a sly dragon-man: violet scales, a dragon head with blue spines, a crimson chest guard, a long dark coat, "
        "orange gauntlets and boots, white claws and an anchor-hook tail")
BASE = {"violet": (130, 100, 200), "violet_dark": (70, 50, 130), "violet_light": (190, 170, 240), "red": (210, 40, 50),
        "red_dark": (120, 14, 24), "red_light": (250, 120, 120), "coat": (50, 50, 60), "coat_dark": (20, 20, 26),
        "orange": (240, 150, 40), "orange_dark": (170, 90, 20), "claw": (240, 240, 246), "claw_dark": (170, 170, 186),
        "blue": (80, 120, 230), "steel": (200, 204, 216), "steel_dark": (100, 104, 116), "eye": (255, 220, 60),
        "pupil": (20, 16, 10), "white": (250, 250, 250), "wing": (250, 220, 60, 235), "wing_dark": (210, 160, 30, 240),
        "gold": (236, 196, 70), "gold_dark": (160, 120, 30), "mouth": (100, 20, 30), "tongue": (210, 70, 90)}
SHINY = {"violet": (60, 160, 120), "violet_dark": (24, 90, 60), "violet_light": (140, 220, 180), "red": (40, 90, 200),
         "red_dark": (16, 40, 120), "red_light": (120, 170, 250), "wing": (190, 240, 250, 235),
         "wing_dark": (110, 190, 220, 240)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, variant=None):
    SCALES = scales(P, "violet", "violet_dark", size=1.4, light="violet_light", rim_mix=0.4)
    RED = armour(P, "red", "red_dark", light="red_light", trim="gold" if variant else None)
    COAT = fabric(P, "coat", "coat_dark", axis="y", period=2.6)
    ORANGE = leather(P, "orange", "orange_dark")
    CLAW = metal(P, "claw", dark="claw_dark")
    STEEL = metal(P, "steel", dark="steel_dark")
    GOLD = metal(P, "gold", dark="gold_dark")

    def wing_inside(x, y, z, face, box):
        u, v, W, H = local(x, y, z, face, box)
        rag = 0.1 + 0.08 * abs(math.sin(u * 1.7)) + 0.06 * abs(math.sin(u * 3.1))
        return v / max(H, 1e-6) > rag

    def build():
        m = Model(name)
        mats = {"skin": SCALES, "chest": RED, "abs": SCALES, "pelvis": COAT, "neck": SCALES, "deltoid": RED,
                "upper_arm": COAT, "forearm": ORANGE, "hand": SCALES, "finger": CLAW, "claw": CLAW, "thigh": COAT,
                "knee": COAT, "shin": ORANGE, "calf": ORANGE, "foot": SCALES, "talon": CLAW}
        a = humanoid(m, mats, bulk=1.0, arm_bulk=1.05, leg_bulk=1.1, digitigrade=True, claws=True, talons=True,
                     name=name, hand_pose="open")
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.8, 2.4, 2.8, 54.6, 60.4, SCALES, cut=1)
        m.box(hd, -1.8, 55.0, -7.6, 1.8, 58.0, -2.6, SCALES)                             # dragon snout
        m.box(hd, -1.6, 54.0, -7.0, 1.6, 55.0, -2.8, solid(P, "mouth"))
        for sx in (-1, 1):
            m.box(hd, sx * 1.4 - 0.6, 58.6, -3.6, sx * 1.4 + 0.6, 59.2, -3.4, solid(P, "eye", glow=True))
        for i in range(6):                                       # swept-back blue spines
            ang = math.radians(-50 + i * 20)
            spike(m, hd, (2.0 * math.sin(ang), 60.0, 0.5), (math.sin(ang) * 0.6, 0.6, 1), 1.2, 5.0 + (i % 2),
                  solid(P, "blue"))
        shell(m, bd, (0, 0, 0.6), 5.0, 42.0, 51.0, -80, 80, 7, 1.2, RED)                  # crimson chest guard
        sk = m.bone("skirt", bd, (0, 33, 0))
        for i in range(8):                                       # long dark coat tails
            ang = math.radians(-160 + i * 45.7)
            c = (4.6 * math.sin(ang), 33.0, -4.0 * math.cos(ang))
            if math.cos(ang) < -0.6:
                continue                                         # open at the front
            m.box(sk, c[0] - 1.8, 10.0, c[2], c[0] + 1.8, 33.0, c[2] + 0.8, COAT,
                  rotation=(-10 * math.cos(ang), -math.degrees(ang), 0), pivot=c)
        m.box(bd, -4.6, 31.4, -4.2, 4.6, 33.0, 4.0, leather(P, "coat", "coat_dark"))     # belt
        tl = m.bone("tail", bd, (0, 31, 3))
        pts = [(0, 31, 3), (-3, 24, 10), (-8, 16, 14), (-14, 10, 14), (-20, 8, 10)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, tl, p0, p1, 3 - j * 0.5, SCALES, extend=0.5)
        e = pts[-1]
        if variant is None:                                      # anchor hook
            rod(m, tl, e, (e[0] - 4.0, e[1] - 2.0, e[2]), 2, STEEL, extend=0.3)
            for sx in (-1, 1):
                rod(m, tl, (e[0] - 4.0, e[1] - 2.0, e[2]), (e[0] - 6.0, e[1] + 2.0, e[2] + sx * 4.0), 2, STEEL,
                    extend=0.3)
                spike(m, tl, (e[0] - 6.0, e[1] + 2.0, e[2] + sx * 4.0), (0, 1, sx * 0.4), 1.4, 2.4, STEEL)
        else:                                                    # gold trident
            rod(m, tl, e, (e[0] - 6.0, e[1] + 2.0, e[2]), 1, GOLD, extend=0.2)
            for dz in (-2.4, 0.0, 2.4):
                rod(m, tl, (e[0] - 6.0, e[1] + 2.0, e[2]), (e[0] - 10.0, e[1] + 4.0, e[2] + dz), 1, GOLD, extend=0.2)
                spike(m, tl, (e[0] - 10.0, e[1] + 4.0, e[2] + dz), (-1, 0.4, dz * 0.2), 1.0, 2.0, GOLD)
            for sx, nm in ((1, "wing_left"), (-1, "wing_right")):  # huge tattered yellow wings
                wb = m.bone(nm, bd, (sx * 3.0, 50.0, 3.0))
                for j in range(3):
                    x0, x1 = sorted((sx * 3.0, sx * (26.0 - j * 4.0)))
                    m.box(wb, x0, 30.0 + j * 6.0, 4.0 + j, x1, 62.0 - j * 2.0, 4.0 + j,
                          cutout(wing_inside, lambda x, y, z, f, variant=None, box=None, **k:
                                 ((P(variant)["wing_dark"] if (x * 0.6) % 2.0 < 0.2 else P(variant)["wing"]), None)),
                          rotation=(-10, sx * 15, -sx * (10 - j * 10)), pivot=(sx * 3.0, 50.0, 4.0 + j))
                rod(m, wb, (sx * 3.0, 50.0, 3.0), (sx * 24.0, 62.0, 5.0), 2, RED, extend=0.3)
            for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
                sh = a[nm]["shoulder"]
                dome(m, a[nm]["bone"], (sh[0] + sx * 1.4, 50.0, 0.3), 4.2, 3.8, RED, layers=3)
        if variant == "brave":                                   # the Brave Snatcher claw gauntlet
            ar = a["arm_right"]
            el, h = ar["elbow"], ar["hand"]
            bs = m.bone("snatcher", ar["bone"], h)
            m.round_box(bs, h[0] - 1.0, h[2], 4.4, 4.4, h[1] - 6.0, h[1] + 6.0, STEEL, cut=1)
            for j in range(5):                                   # huge crimson claws
                ang = math.radians(-60 + j * 30)
                base = (h[0] - 1.0 + 3.0 * math.sin(ang), h[1] - 6.0, h[2] - 3.0 * math.cos(ang))
                tip = (base[0] + 4.0 * math.sin(ang), base[1] - 12.0, base[2] - 6.0 * math.cos(ang))
                rod(m, bs, base, tip, 3, RED, extend=0.4)
                spike(m, bs, tip, (0, -0.4, -1), 2.0, 4.0, CLAW, tip=0.8)
            for i in range(10):                                  # gold ring around it
                ang = math.radians(i * 36)
                c = (h[0] - 1.0, h[1] + 8.0 * math.sin(ang), h[2] + 8.0 * math.cos(ang))
                m.box(bs, c[0] - 0.6, c[1] - 1.4, c[2] - 1.4, c[0] + 0.6, c[1] + 1.4, c[2] + 1.4, GOLD,
                      rotation=(i * 36, 0, 0), pivot=c)
        return m
    return build


build = make("arresterdramon")
