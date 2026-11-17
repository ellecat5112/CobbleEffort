"""Beelzebumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Demon Lord of Gluttony, a demon biker. Black leather from head to toe with silver buckles and
straps, a purple helm-mask with three red eyes under a crest of blond spikes, red bandanas trailing from its left arm,
long steel claws, spiked boots and two sawn-off shotguns. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage. make("x"): Beelzebumon (X-Antibody) (great blue-and-red
wings, a red-white mane and a huge cannon on its arm); make("blast"): Beelzebumon: Blast Mode (ten black wings, a
silver demon claw for a left arm and the Death Slinger positron cannon on its right).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid, shell
from _digidetail import armour, feathers, leather, local, metal, solid, strands
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("the Demon Lord of Gluttony, a demon biker in black leather with silver buckles, a purple three-eyed helm under "
        "blond spikes, red bandanas, steel claws, spiked boots and two shotguns")
BASE = {"black": (36, 34, 42), "black_light": (110, 108, 126), "purple": (90, 60, 150), "purple_dark": (40, 24, 80),
        "hair": (240, 220, 120), "hair_dark": (190, 160, 60), "red": (200, 30, 40), "red_dark": (110, 10, 20),
        "steel": (200, 204, 216), "steel_dark": (100, 104, 116), "eye": (255, 40, 50), "blue": (40, 60, 150),
        "blue_dark": (16, 24, 80), "white": (240, 240, 246), "cannon": (110, 112, 124), "glow": (255, 230, 90)}
SHINY = {"black": (220, 216, 230), "black_light": (255, 255, 255), "purple": (40, 140, 120), "purple_dark": (16, 70, 60),
         "red": (40, 120, 220), "red_dark": (16, 60, 140), "blue": (160, 40, 60), "blue_dark": (90, 14, 24)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, variant=None):
    LEATHER = leather(P, "black", "black_light", stitch="steel")
    STEEL = metal(P, "steel", dark="steel_dark")
    PURPLE = armour(P, "purple", "purple_dark")
    HAIR = strands(P, "hair", "hair_dark")

    def shotgun(m, bone, h, d):
        rod(m, bone, (h[0], h[1] - 1.0, h[2] + 1.0), (h[0], h[1] + 1.0, h[2]), 2, LEATHER, extend=0)
        for dx in (-0.5, 0.5):
            rod(m, bone, (h[0] + dx, h[1] + 0.6, h[2]), (h[0] + dx + d[0] * 10, h[1] + 0.6 + d[1] * 10,
                h[2] + d[2] * 10), 1, STEEL, extend=0)

    def build():
        m = Model(name)
        mats = {"skin": LEATHER, "chest": LEATHER, "abs": LEATHER, "pelvis": LEATHER, "neck": LEATHER,
                "deltoid": LEATHER, "upper_arm": LEATHER, "forearm": LEATHER, "hand": LEATHER, "finger": STEEL,
                "claw": STEEL, "thigh": LEATHER, "knee": STEEL, "shin": LEATHER, "calf": LEATHER, "foot": LEATHER,
                "talon": STEEL}
        a = humanoid(m, mats, bulk=0.95, arm_bulk=0.95, leg_bulk=1.0, digitigrade=True, claws=True, talons=True,
                     name=name, hand_pose="open")
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 2.4, 2.8, 54.6, 60.6, PURPLE, cut=1)
        m.box(hd, -1.4, 54.8, -6.0, 1.4, 57.4, -2.6, PURPLE)                              # snout of the mask
        for ex, ey in ((-1.0, 58.0), (1.0, 58.0), (0.0, 59.2)):                          # three red eyes
            m.box(hd, ex - 0.4, ey - 0.3, -3.3, ex + 0.4, ey + 0.3, -3.1, solid(P, "eye", glow=True))
        mane = m.bone("mane", hd, (0, 60, 1))
        for i in range(12):                                      # blond spikes
            ang = math.radians(-80 + i * 14.5)
            rod(m, mane, (2.0 * math.sin(ang), 60.0, 0.6), (5.0 * math.sin(ang), 63.0 + 2.0 * math.cos(ang), 5.0),
                1, HAIR, extend=0.2, t2=2)
        for j in range(5):                                       # buckled straps across the torso
            m.box(bd, -5.0, 34.0 + j * 3.6, -4.4, 5.0, 34.8 + j * 3.6, 4.0, leather(P, "black", "steel"))
            m.box(bd, 1.0, 33.8 + j * 3.6, -4.8, 2.4, 35.0 + j * 3.6, -4.2, STEEL)
        al = a["arm_left"]
        for j in range(4):                                       # red bandanas trailing from the left arm
            p = tuple(e + (w - e) * 0.3 for e, w in zip(al["elbow"], al["wrist"]))
            rod(m, al["bone"], p, (p[0] + 3.0 + j, p[1] - 6.0 - j * 2, p[2] + 6.0), 1, solid(P, "red"), extend=0.2,
                t2=2)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):      # spiked boots
            kn = a[nm]["knee"]
            for j in range(3):
                spike(m, a[nm]["bone"], (kn[0], 10.0 + j * 3.0, 1.6), (sx * 0.3, 0.3, 1), 1.0, 2.4, STEEL)
        if variant is None:
            for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
                shotgun(m, a[nm]["bone"], a[nm]["hand"], (sx * 0.1, 0.0, -1.0))
            return m
        wings = 2 if variant == "x" else 5
        for sx, nm in ((1, "wing_left"), (-1, "wing_right")):    # wings
            wb = m.bone(nm, bd, (sx * 3.0, 49.0, 3.0))
            if variant == "x":
                F = feathers(P, "blue", "blue_dark", size=(1.8, 3.4), flow=(0, -1), tip="red")
            else:
                F = feathers(P, "black", "black_light", size=(1.8, 3.4), flow=(0, -1))
            for w in range(wings):
                ang0 = 40 - w * (70 / max(wings - 1, 1))
                for i in range(7):
                    t = i / 6
                    ang = math.radians(ang0)
                    base = (sx * (3.0 + 14.0 * t * math.cos(ang)), 49.0 + 14.0 * t * math.sin(ang) + 4.0 * t,
                            3.0 + w * 0.8 + 3.0 * t)
                    ln = 8.0 + 10.0 * t
                    m.box(wb, base[0] - 1.6, base[1] - ln, base[2], base[0] + 1.6, base[1], base[2], F,
                          rotation=(-8, 0, -sx * (40 - 20 * t)), pivot=base)
        ar, al = a["arm_right"], a["arm_left"]
        el, wr = ar["elbow"], ar["wrist"]
        cb = m.bone("cannon", ar["bone"], wr)                    # the cannon on its right arm
        m.round_box(cb, wr[0], wr[2] - 4.0, 3.2, 8.0, wr[1] - 3.0, wr[1] + 3.0, metal(P, "cannon", dark="black"),
                    cut=1)
        rod(m, cb, (wr[0], wr[1], wr[2] - 10.0), (wr[0], wr[1], wr[2] - 22.0), 4, metal(P, "cannon", dark="black"),
            extend=0)
        m.box(cb, wr[0] - 1.4, wr[1] - 1.4, wr[2] - 22.4, wr[0] + 1.4, wr[1] + 1.4, wr[2] - 21.8,
              solid(P, "glow", glow=True))
        if variant == "x":                                       # red-white mane
            for i in range(8):
                rod(m, mane, (-2.0 + i * 0.6, 58.0, 2.0), (-3.0 + i * 0.9, 50.0, 6.0), 2, strands(P, "white", "red"),
                    extend=0.3)
        else:                                                    # Blast Mode: silver demon claw on the left arm
            h = al["hand"]
            m.round_box(al["bone"], h[0], h[2], 2.6, 2.6, h[1] - 3.0, h[1] + 3.0, STEEL, cut=1)
            for f in range(4):
                spike(m, al["bone"], (h[0] + (f - 1.5) * 1.2, h[1] - 3.0, h[2]), (0.1, -1, -0.3), 1.0, 6.0, STEEL,
                      tip=0.4)
        return m
    return build


build = make("beelzebumon")
