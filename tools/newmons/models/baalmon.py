"""Baalmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a wandering demon swordsman. A white-and-silver bodysuit under black armour plates and buckled belts,
a spiky blue hood-helm with a blond fringe, a long white scarf streaming in tatters, a cape of paper talismans, black
boots and a red-hilted short sword. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage. make(x=True): Baalmon (X-Antibody) (a cloak of violet feathers,
a white mantle, crossed red belts, a red gauntlet arm and a floating spellbook).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, dome, humanoid, shell
from _digidetail import armour, cutout, fabric, feathers, leather, local, metal, plane, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 1.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a wandering demon swordsman: a white bodysuit under black armour and buckled belts, a spiky blue hood-helm, a "
        "long tattered white scarf, a cape of paper talismans and a red-hilted sword")
BASE = {"white": (240, 242, 246), "white_dark": (170, 174, 190), "black": (40, 40, 48), "black_light": (110, 110, 126),
        "silver": (200, 204, 216), "silver_dark": (100, 104, 116), "blue": (50, 70, 170), "blue_dark": (20, 26, 90),
        "hair": (240, 210, 90), "hair_dark": (190, 150, 50), "paper": (220, 210, 180), "paper_dark": (160, 146, 110),
        "ink": (60, 40, 30), "red": (200, 30, 40), "red_dark": (110, 10, 20), "violet": (80, 70, 160),
        "violet_dark": (36, 30, 90), "book": (170, 110, 80), "page": (250, 230, 230, 200), "eye": (255, 220, 60)}
SHINY = {"blue": (170, 40, 60), "blue_dark": (90, 14, 24), "black": (60, 40, 90), "black_light": (130, 110, 170),
         "violet": (60, 140, 120), "violet_dark": (20, 80, 60), "red": (40, 140, 220), "red_dark": (16, 70, 140)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    SUIT = fabric(P, "white", "white_dark", axis="y", period=3.0)
    ARM = armour(P, "black", "black", light="black_light", trim="silver", trim_w=0.3)
    BELT = leather(P, "black", "black_light", stitch="silver")
    SILVER = metal(P, "silver", dark="silver_dark")
    HAIR = strands(P, "hair", "hair_dark")
    FEATHER = feathers(P, "violet", "violet_dark", size=(1.6, 3.0), flow=(0, -1))

    def talisman(xx, y, z, face, variant, box=None, **k):
        """Paper talismans: pale strips with dark ink script lines."""
        p = P(variant)
        u, v, W, H = local(xx, y, z, face, box)
        if (v * 1.3) % 2.0 < 0.3 and 0.3 < (u % 2.2) < 1.8:
            return tone(p["ink"], face), None
        if (u % 2.2) < 0.15:
            return tone(p["paper_dark"], face), None
        return tone(p["paper"], face), None

    def torn(xx, y, z, face, box):
        u, v, W, H = local(xx, y, z, face, box)
        return v / max(H, 1e-6) > 0.1 * abs(math.sin((box.lo[0] + u) * 2.1)) + 0.04

    def build():
        m = Model(name)
        mats = {"skin": SUIT, "chest": ARM, "abs": SUIT, "pelvis": BELT, "neck": SUIT, "deltoid": ARM,
                "upper_arm": SUIT, "forearm": ARM if not x else SUIT, "hand": solid(P, "black"),
                "finger": solid(P, "black"), "thigh": SUIT, "knee": ARM, "shin": ARM, "calf": SUIT,
                "foot": solid(P, "black"), "toe": solid(P, "black")}
        a = humanoid(m, mats, bulk=0.95, arm_bulk=0.95, leg_bulk=1.0, name=name, hand_pose="fist")
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, 0, 2.3, 2.5, 54.6, 60.4, solid(P, "white"), cut=1)
        m.box(hd, -2.2, 55.0, -2.8, 2.2, 57.4, -2.4, fabric(P, "white", "white_dark"))   # scarf over the mouth
        m.box(hd, -1.8, 57.6, -2.7, 1.8, 58.4, -2.5, solid(P, "eye", glow=True))
        for i in range(9):                                       # the spiky blue hood
            ang = math.radians(-80 + i * 20)
            spike(m, hd, (2.2 * math.sin(ang), 60.0, -2.2 * math.cos(ang) * 0.6 + 0.6),
                  (math.sin(ang), 0.8, 0.4), 1.6, 3.6, armour(P, "blue", "blue_dark"), tip=0.6)
        m.round_box(hd, 0, 0.4, 2.8, 2.8, 59.0, 61.6, armour(P, "blue", "blue_dark"), cut=1)
        for i in range(5):                                       # blond fringe
            rod(m, hd, (-1.6 + i * 0.8, 60.0, -2.4), (-2.0 + i, 57.6, -2.9), 1, HAIR, extend=0.2)
        sk = m.bone("skirt", bd, (0, 51, 3))                     # long tattered scarf streaming back
        for j in range(3):
            rod(m, sk, (-1.0 + j, 51.0, 3.0), (-10.0 - j * 3, 56.0 - j * 2, 18.0 + j * 2), 1,
                cutout(torn, fabric(P, "white", "white_dark")), extend=0.3, t2=3)
        for sx in (-1, 1):                                       # crossed belts
            rod(m, bd, (sx * 4.6, 50.0, -3.8), (-sx * 4.0, 32.0, -4.0), 1, BELT, extend=0.3, t2=1)
        m.box(bd, -4.8, 31.0, -4.2, 4.8, 33.0, 4.0, BELT)
        cb = m.bone("cap", bd, (0, 51, 4))
        if x:                                                    # X: cloak of violet feathers + white mantle
            for i in range(14):
                t = i / 13
                c = (-9.0 + 18.0 * t, 50.0, 4.4 + abs(t - 0.5) * 3)
                m.box(cb, c[0] - 1.5, 8.0, c[2], c[0] + 1.5, 50.0, c[2], FEATHER,
                      rotation=(10, 0, (t - 0.5) * 20), pivot=c)
            shell(m, bd, (0, 0, 0.4), 5.6, 44.0, 52.0, -170, 170, 12, 1.0, fabric(P, "white", "white_dark"))
            for sx in (-1, 1):
                rod(m, bd, (sx * 5.0, 46.0, -4.0), (-sx * 5.0, 36.0, -4.6), 1, solid(P, "red"), extend=0.2, t2=1)
            ar = a["arm_right"]                                  # red gauntlet arm and the spellbook
            el, wr = ar["elbow"], ar["wrist"]
            rod(m, ar["bone"], el, wr, 5, armour(P, "red", "red_dark", trim="silver"), extend=0.4)
            h = a["arm_left"]["hand"]
            bb = m.bone("book", a["arm_left"]["bone"], h)
            m.box(bb, h[0] - 0.5, h[1] + 4.0, h[2] - 7.0, h[0] + 6.0, h[1] + 9.0, h[2] - 3.0, solid(P, "book"),
                  rotation=(0, -20, 10), pivot=h)
            m.box(bb, h[0] + 0.5, h[1] + 9.0, h[2] - 6.6, h[0] + 5.0, h[1] + 13.0, h[2] - 6.6, solid(P, "page"))
        else:                                                    # the cape of paper talismans
            cape(m, cb, 52.0, 18.0, 42.0, cutout(torn, talisman), z=4.8, flare=0.9, panels=9, sweep=(0, 6))
        ar = a["arm_right"]                                      # the red-hilted short sword
        h = ar["hand"]
        sw = m.bone("sword", ar["bone"], h)
        rod(m, sw, (h[0], h[1] + 1.0, h[2]), (h[0], h[1] - 4.0, h[2]), 1, solid(P, "red"), extend=0)
        rod(m, sw, (h[0], h[1] - 4.0, h[2]), (h[0] + 2.0, h[1] - 14.0, h[2] - 6.0), 1, SILVER, extend=0, t2=2)
        return m
    return build


build = make("baalmon")
