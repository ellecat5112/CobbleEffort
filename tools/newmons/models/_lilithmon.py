"""Shared builder for Lilithmon and Lilithmon (X-Antibody) (CobbleEffort: Digital; hand-built at the detail standard
after the official art on wikimon.net): the Demon Lord of Lust, drawn as a dark sorceress-queen: a tall figure in a
long purple kimono-robe with wide sleeves and gold trim over a black under-robe, long black hair crowned with golden
hairpins and a jewel, a pale face with violet eyes, a golden clawed gauntlet on one hand (Nazar Nail), and black bat
wings sprouting long golden spear-ribs. X-Antibody: crimson-and-violet robes, horned crown, and great tattered wings
traced with glowing green circuit rings. Built as officially drawn, fully robed. Shiny: crimson robe.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import bat_wing
from _digibody import humanoid
from _digidetail import cutout, fabric, gem, local, metal, noise2, skin, solid, strands
from _route import pal, tone

BASE = {"purple": (130, 90, 190), "purple_dark": (60, 34, 110), "black": (34, 30, 40), "black_dark": (10, 8, 14),
        "gold": (240, 200, 80), "gold_dark": (160, 120, 30), "skin": (232, 214, 220), "skin_dark": (180, 150, 170),
        "eye": (160, 80, 220), "red": (190, 30, 50), "red_dark": (100, 10, 24), "green": (60, 240, 180),
        "membrane": (60, 50, 70), "membrane_dark": (24, 20, 30), "jewel": (220, 40, 80), "jewel_light": (255, 170, 190)}
SHINY = {"purple": (200, 50, 70), "purple_dark": (110, 14, 30)}


def P(v):
    return pal(BASE, SHINY, v)


def tatter(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return v / max(H, 1e-6) > 0.16 * abs(math.sin(u * 0.8)) + 0.07 * noise2(u, 0.0, 11)


def make(name, x=False):
    ROBE = fabric(P, "purple" if not x else "red", "purple_dark" if not x else "red_dark", seam="gold")
    UNDER = fabric(P, "black", "black_dark")
    SK = skin(P, "skin", dark="skin_dark")

    def wingf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if x:
            u, v, W, H = local(xx, y, z, face, box)
            if abs(math.hypot(u - W * 0.5, v - H * 0.5) - W * 0.25) < 0.4:
                return tone(p["green"], face), p["green"]
        return tone(p["membrane"], face), None

    def build():
        m = Model(name)
        mats = {"skin": UNDER, "chest": ROBE, "abs": UNDER, "pelvis": ROBE, "neck": SK, "deltoid": ROBE,
                "upper_arm": ROBE, "forearm": ROBE, "hand": SK, "finger": SK, "thigh": ROBE, "knee": ROBE,
                "shin": ROBE, "calf": ROBE, "foot": UNDER, "toe": UNDER}
        a = humanoid(m, mats, bulk=0.8, arm_bulk=0.8, leg_bulk=0.9, name=name)
        bd = a["body"]
        for j in range(6):                                                         # long robe to the ground
            r = 4.6 + j * 0.9
            m.round_box(bd, 0, 0.6, r, r * 0.8, 33.0 - (j + 1) * 5.6, 33.4 - j * 5.6, ROBE, cut=max(1, int(r * 0.3)))
        for sx in (-1, 1):                                                         # wide sleeves
            ab = a["arm_left" if sx > 0 else "arm_right"]["bone"]
            m.round_box(ab, sx * 8.0, -1.0, 2.6, 4.0, 30.0, 42.0, ROBE, cut=1)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 60.0, SK, cut=1)
        m.box(hd, -1.6, 57.4, -2.9, -0.5, 58.0, -2.8, solid(P, "eye"))
        m.box(hd, 0.5, 57.4, -2.9, 1.6, 58.0, -2.8, solid(P, "eye"))
        for i in range(11):                                                        # long black hair
            ang = math.radians(-110 + i * 22)
            rod(m, hd, (2.4 * math.sin(ang), 60.0, 0.8 + 1.4 * math.cos(ang)), (3.6 * math.sin(ang), 34.0, 3.6), 1,
                strands(P, "black", "black_dark"), extend=0.3, t2=2)
        m.round_box(hd, 0, 0.6, 2.8, 2.8, 59.0, 62.0, strands(P, "black", "black_dark"), cut=1)
        for sx in (-1, 1):                                                         # golden hairpins
            rod(m, hd, (sx * 1.0, 61.0, 0), (sx * 5.0, 65.0, 0), 1, metal(P, "gold", dark="gold_dark"), extend=0, t2=1)
            m.round_box(hd, sx * 5.0, 0, 0.8, 0.8, 64.4, 65.8, gem(P, "jewel", "jewel_light"), cut=0)
            if x:
                spike(m, hd, (sx * 2.0, 61.0, -1.0), (sx * 0.4, 1, 0), 1.0, 4.0, solid(P, "red"), tip=0.8)
        m.round_box(hd, 0, -2.4, 0.8, 0.4, 60.0, 61.4, gem(P, "jewel", "jewel_light"), cut=0)
        hr = a["arm_right"]                                                         # golden claw (Nazar Nail)
        hx, hy, hz = hr["hand"]
        m.round_box(hr["bone"], hx, hz, 1.8, 1.8, hy - 2.0, hy + 1.0, metal(P, "gold", dark="gold_dark"), cut=1)
        for j in range(4):
            spike(m, hr["bone"], (hx + (j - 1.5) * 0.9, hy - 2.0, hz - 0.6), (0, -1, -0.2), 0.8, 5.0,
                  metal(P, "gold", dark="gold_dark"), tip=0.8)
        for side in (1, -1):                                                       # bat wings with spear ribs
            wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 2.6, 50.0, 3.4))
            bat_wing(m, wb, (side * 2.6, 50.0, 3.4), 26.0 if not x else 32.0, 28.0, 4, solid(P, "black"),
                     cutout(tatter, wingf) if x else wingf, side=side, sweep=15)
            if not x:
                for j in range(3):
                    spike(m, wb, (side * (6.0 + j * 5.0), 46.0 - j * 4.0, 4.0), (side * 0.3, -1, 0.2), 1.0, 14.0,
                          metal(P, "gold", dark="gold_dark"), tip=0.8)
        return m

    return build
