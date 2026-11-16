"""Angewomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): an archangel in her official outfit: a white bodysuit with gold and silver fittings, a silver
helm over her eyes, long golden hair, eight white wings (four per side, the lowest darker-tipped), a long pink
ribbon of holy cloth wound about her and a gold bow of light. 25 blocks tall.

Front is -z, y is up. 72 units tall (the wings); Perfect stage. Angewomon (X-Antibody) uses angewomon.make(x=True):
more wings in rainbow colours and gold armour plates.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid, shell
from _digidetail import armour, fabric, feathers, local, metal, mix, skin, solid, strands
from _route import pal, tone

HEIGHT = 72
SCALE, HITBOX = sized(25, HEIGHT, 1.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("an archangel in a white bodysuit with gold fittings, a silver helm, long golden hair, eight white wings, a long "
        "pink ribbon and a gold bow of light")
BASE = {"white": (250, 250, 252), "white_dark": (190, 196, 214), "silver": (200, 204, 216), "silver_dark": (100, 104, 120),
        "gold": (236, 196, 70), "gold_dark": (160, 120, 30), "gold_light": (255, 240, 170), "hair": (250, 226, 130),
        "hair_dark": (210, 160, 70), "ribbon": (230, 170, 210), "ribbon_dark": (170, 100, 150), "skin": (246, 226, 214),
        "skin_dark": (200, 160, 150), "wing_tip": (70, 70, 90), "r1": (250, 200, 120), "r2": (170, 220, 250),
        "r3": (230, 170, 240), "r4": (170, 240, 200)}
SHINY = {"white": (60, 56, 70), "white_dark": (24, 22, 30), "ribbon": (150, 60, 200), "ribbon_dark": (90, 30, 130),
         "hair": (230, 230, 245), "hair_dark": (170, 170, 190), "gold": (210, 214, 226), "gold_dark": (140, 146, 162)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    SUIT = skin(P, "white", dark="white_dark", var=0.02)
    SILVER = armour(P, "silver", "silver_dark")
    GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")
    GOLD_ARM = armour(P, "gold", "gold_dark", light="gold_light")
    HAIR = strands(P, "hair", "hair_dark")
    RIBBON = fabric(P, "ribbon", "ribbon_dark", axis="x", period=1.4)
    WING = feathers(P, "white", "white_dark", size=(1.4, 3.0), flow=(0, -1))
    WING_DARK = feathers(P, "white", "white_dark", size=(1.4, 3.0), flow=(0, -1), tip="wing_tip")

    def rainbowf(i):
        key = ("r1", "r2", "r3", "r4")[i % 4]
        return feathers(P, key, "white_dark", size=(1.4, 3.0), flow=(0, -1), tip="gold")

    def build():
        m = Model(name)
        mats = {"skin": SUIT, "chest": GOLD_ARM if x else SUIT, "abs": SUIT, "pelvis": SUIT, "neck": SUIT,
                "deltoid": GOLD_ARM if x else SUIT, "upper_arm": SUIT, "forearm": GOLD_ARM if x else SUIT,
                "hand": SUIT, "finger": SUIT, "thigh": SUIT, "knee": GOLD, "shin": SUIT, "calf": SUIT,
                "foot": GOLD, "toe": GOLD}
        a = humanoid(m, mats, bulk=0.8, arm_bulk=0.78, leg_bulk=0.85, name=name, hand_pose="open", chest_depth=0.9)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, 0, 2.2, 2.4, 54.5, 60.5, skin(P, "skin", dark="skin_dark"), cut=1)
        m.box(hd, -2.4, 57.0, -2.7, 2.4, 61.0, 2.0, SILVER)                              # helm over the eyes
        for sx in (-1, 1):
            rod(m, hd, (sx * 2.2, 59.0, 0), (sx * 4.6, 62.0, 2.4), 1, SILVER, extend=0.2, t2=2)
        hr = m.bone("mane", hd, (0, 60, 2))
        for i in range(9):                                       # long golden hair
            xx = -3.0 + i * 0.75
            rod(m, hr, (xx, 60.0, 1.6), (xx * 1.6, 30.0 - (i % 3) * 3, 6.0), 2, HAIR, extend=0.3)
        m.box(bd, -4.0, 30.6, -3.8, 4.0, 32.4, 3.8, GOLD)                                # gold belt
        for sx in (-1, 1):
            m.box(bd, sx * 2.6 - 1.0, 44.0, -4.6, sx * 2.6 + 1.0, 47.0, -3.8, GOLD)      # gold chest clasps
        # the ribbon: wound round the arms, looping behind, hanging to the ground
        rb = m.bone("skirt", bd, (0, 40, 0))
        for i in range(10):
            t = i / 9
            ang = t * math.pi * 1.6
            p0 = (8.0 * math.cos(ang), 46.0 - 34.0 * t, 5.0 * math.sin(ang) + 3.0)
            p1 = (8.0 * math.cos(ang + 0.5), 46.0 - 34.0 * (t + 0.1), 5.0 * math.sin(ang + 0.5) + 3.0)
            rod(m, rb, p0, p1, 2, RIBBON, extend=0.4, t2=1)
        rod(m, rb, (-8.0, 12.0, 3.0), (-9.0, 0.5, 4.0), 2, RIBBON, extend=0.3, t2=1)
        n = 6 if x else 4
        for sx, nm in ((1, "wing_left"), (-1, "wing_right")):    # wings, the lowest darker-tipped
            wb = m.bone(nm, bd, (sx * 3.0, 49.0, 3.0))
            for j in range(n):
                ang = 50 - j * (80 / (n - 1))
                ln = 22.0 - abs(j - 1) * 2.0
                r = math.radians(ang)
                root = (sx * 3.0, 49.0, 3.0 + j * 0.5)
                tip = (sx * (3.0 + ln * math.cos(r)), 49.0 + ln * math.sin(r) + 4, 6.0 + j)
                rod(m, wb, root, tip, 2, WING, extend=0.3)
                sh = rainbowf(j) if x else (WING_DARK if j == n - 1 else WING)
                for i in range(9):
                    t = (i + 0.5) / 9
                    p = tuple(rr * (1 - t) + tt * t for rr, tt in zip(root, tip))
                    fl = 5.0 + 5.0 * t
                    m.box(wb, p[0] - 2.0, p[1] - fl, p[2], p[0] + 2.0, p[1], p[2], sh,
                          rotation=(-8, 0, -sx * (20 + 20 * t)), pivot=p)
        al = a["arm_left"]                                       # the bow of light
        h = al["hand"]
        bw = m.bone("bow", al["bone"], h)
        for i in range(7):
            t = i / 6 - 0.5
            p = (h[0] + 1.0 - 3.0 * (1 - 4 * t * t), h[1] + t * 18.0, h[2] - 1.0)
            m.box(bw, p[0] - 0.5, p[1] - 1.6, p[2] - 0.5, p[0] + 0.5, p[1] + 1.6, p[2] + 0.5, GOLD)
        if x:
            for sx, nm in ((1, "arm_left"), (-1, "arm_right")):  # gold pauldrons and a sun-halo behind
                sh_ = a[nm]["shoulder"]
                dome(m, a[nm]["bone"], (sh_[0] + sx * 0.8, 49.5, 0.2), 2.8, 2.6, GOLD_ARM, layers=3)
            for i in range(12):
                ang = math.radians(i * 30)
                c = (9.0 * math.cos(ang), 58.0 + 9.0 * math.sin(ang), 5.0)
                m.box(bd, c[0] - 0.8, c[1] - 0.8, c[2] - 0.4, c[0] + 0.8, c[1] + 0.8, c[2] + 0.4, GOLD)
        return m
    return build


build = make("angewomon")
