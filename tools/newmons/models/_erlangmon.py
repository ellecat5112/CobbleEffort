"""Shared builder for Erlangmon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): the god of
the three-pointed spear. make(blast=False): a tall warrior in silver and violet armour with gold trim, a horned gold
crest and a black topknot, a long violet tasset robe, a long gold three-pronged spear, and a spectral pale-blue dragon-
hound spirit coiling behind it in a swirl of cloud. make(blast=True): Blast Mode, sleeker violet-and-white armour with
gold, a gold crescent halo and a red jewel on its brow, long flowing pale-blue ribbon-hair streaming in waves, gold
spike feet and a towering crystal-blue trident. Shiny: crimson and gold.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import cape, humanoid
from _digidetail import armour, fabric, metal, solid, strands
from _route import pal, tone

BASE = {"silver": (220, 224, 236), "silver_dark": (110, 114, 128), "silver_light": (255, 255, 255),
        "violet": (110, 90, 170), "violet_dark": (50, 36, 90), "violet_light": (180, 160, 230), "gold": (240, 200, 70),
        "gold_dark": (160, 120, 20), "black": (30, 30, 36), "spirit": (190, 220, 245, 150), "spirit_light": (240, 250, 255, 190),
        "crystal": (140, 220, 240, 220), "red": (220, 40, 40), "hair": (170, 210, 250), "hair_dark": (80, 130, 200),
        "eye": (250, 220, 60)}
SHINY = {"violet": (170, 40, 50), "violet_dark": (80, 10, 20), "violet_light": (240, 120, 120), "hair": (250, 200, 120),
         "hair_dark": (200, 130, 40)}


def P(v):
    return pal(BASE, SHINY, v)


SILVER = armour(P, "silver", "silver_dark", light="silver_light", trim="gold", trim_w=0.25)
VIOLET = armour(P, "violet", "violet_dark", light="violet_light", trim="gold", trim_w=0.3)
GOLD = metal(P, "gold", dark="gold_dark")


def make(name, blast=False):
    def build():
        m = Model(name)
        mats = {"skin": VIOLET, "chest": SILVER, "abs": VIOLET, "pelvis": VIOLET, "neck": SILVER, "deltoid": SILVER,
                "upper_arm": VIOLET, "forearm": SILVER, "hand": SILVER, "finger": SILVER, "thigh": VIOLET,
                "knee": GOLD, "shin": SILVER, "calf": SILVER, "foot": GOLD, "toe": GOLD}
        a = humanoid(m, mats, bulk=1.0 if not blast else 0.85, arm_bulk=1.0, leg_bulk=1.0 if not blast else 0.9,
                     name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 2.4, 2.8, 54.0, 60.0, SILVER, cut=1)
        m.box(hd, -1.6, 57.0, -3.3, 1.6, 57.8, -3.1, solid(P, "eye", glow=True))
        if not blast:
            for sx in (-1, 1):                                                     # horned gold crest
                spike(m, hd, (sx * 1.6, 59.6, -1.0), (sx * 0.8, 1, 0), 1.2, 6.0, GOLD, tip=0.3)
            m.round_box(hd, 0, 1.0, 1.0, 1.0, 60.0, 63.0, solid(P, "black"), cut=0)   # topknot
            cape(m, bd, 34.0, 10.0, 26.0, fabric(P, "violet", "violet_dark"), z=-3.6, flare=0.3)   # long front tasset
            cape(m, bd, 34.0, 12.0, 28.0, fabric(P, "violet", "violet_dark"), z=3.6, flare=0.6)
            sb = m.bone("spirit", bd, (12, 50, 8))                                 # spectral dragon-hound spirit
            pts = [(6.0, 30.0, 8.0), (12.0, 40.0, 10.0), (16.0, 52.0, 8.0), (14.0, 62.0, 4.0)]
            for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
                rod(m, sb, p0, p1, 5 - j, solid(P, "spirit"), extend=0.8)
            m.round_box(sb, 14.0, 2.0, 4.0, 5.0, 60.0, 67.0, solid(P, "spirit_light"), cut=2)
            m.box(sb, 12.0, 61.0, -6.0, 16.0, 64.0, -2.0, solid(P, "spirit"))
        else:
            for j in range(9):                                                     # gold crescent halo
                ang = math.radians(200 + j * 17.5)
                rod(m, hd, (3.6 * math.cos(ang), 62.0 + 3.6 * math.sin(ang), 1.0),
                    (3.6 * math.cos(ang + 0.3), 62.0 + 3.6 * math.sin(ang + 0.3), 1.0), 1, GOLD, extend=0.3)
            m.round_box(hd, 0, -2.9, 0.6, 0.3, 58.4, 59.4, solid(P, "red", glow=True), cut=0)
            for i in range(10):                                                    # flowing ribbon hair
                sx = -1 if i % 2 else 1
                pts = [(sx * 2.0, 59.0, 1.0)]
                for j in range(1, 5):
                    pts.append((sx * (2.0 + j * 3.0 + (i // 2) * 1.2), 59.0 - j * 8.0 + math.sin(j + i) * 2.0,
                                2.0 + j * 1.6))
                for p0, p1 in zip(pts, pts[1:]):
                    rod(m, hd, p0, p1, 1, strands(P, "hair", "hair_dark"), extend=0.4, t2=2)
            for nm in ("leg_left", "leg_right"):
                ak = a[nm]["ankle"]
                spike(m, a[nm]["bone"], (ak[0], 3.0, ak[2]), (0, -1, 0), 2.0, 4.0, GOLD, tip=0.4)
        ar = a["arm_right"]                                                        # the three-pronged spear
        hx, hy, hz = ar["hand"]
        L = 44.0 if not blast else 58.0
        shaft = GOLD if not blast else solid(P, "crystal", glow=True)
        rod(m, ar["bone"], (hx, hy - 22.0, hz), (hx, hy + L - 20.0, hz), 1, shaft, extend=0, t2=2)
        tip_y = hy + L - 20.0
        spike(m, ar["bone"], (hx, tip_y, hz), (0, 1, 0), 2.0, 7.0, shaft, tip=0.5)
        for sx in (-1, 1):
            rod(m, ar["bone"], (hx, tip_y, hz), (hx + sx * 3.0, tip_y + 2.0, hz), 1, shaft, extend=0.3)
            spike(m, ar["bone"], (hx + sx * 3.0, tip_y + 2.0, hz), (0, 1, 0), 1.0, 4.0, shaft, tip=0.3)
        return m
    return build
