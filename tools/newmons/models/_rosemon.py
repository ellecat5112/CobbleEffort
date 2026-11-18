"""Shared builder for Rosemon and its forms (CobbleEffort: Digital; hand-built after the official art on wikimon.net):
the queen of flowers: a tall figure in a fitted crimson bodysuit with leaf-green shoulder petals and black thigh-high
heeled boots, a closed red rose for a hood-mask, long golden hair, red gloves, a long cape of white petals marked with
gold crescents, and a thorned golden vine whip (Thorn Whip). Looks: "base"; "x" (X-Antibody: a dark rose crown of
petals, a long dark-green cape, gold vine coils wound round its red suit, a black belt and a pink brooch);
"burst" (Burst Mode: a white bodysuit, a white rose hood, black gloves and boots, vast glowing pink petal wings and a
long thorned whip). Revealing art is built covered: a full bodysuit. Shiny: violet.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import cape, humanoid
from _digidetail import fabric, gem, leather, metal, solid, strands
from _route import pal, tone


def make(name, look="base"):
    base = {"red": (210, 40, 50), "red_dark": (120, 14, 24), "green": (80, 160, 70), "green_dark": (30, 90, 30),
            "black": (30, 28, 34), "black_dark": (10, 10, 12), "gold": (236, 196, 70), "gold_dark": (150, 110, 20),
            "white": (246, 246, 250), "white_dark": (190, 190, 206), "hair": (240, 210, 110), "hair_dark": (180, 140, 50),
            "pink": (250, 160, 210, 190), "pink_dark": (220, 100, 170, 190), "brooch": (230, 120, 200),
            "dark_green": (30, 70, 40), "dark_red": (90, 20, 30)}
    shiny = {"red": (130, 60, 190), "red_dark": (60, 20, 100), "white": (240, 220, 250), "pink": (170, 140, 250, 190)}

    def P(v):
        return pal(base, shiny, v)

    suit_key = ("white", "white_dark") if look == "burst" else ("red", "red_dark")
    SUIT = fabric(P, suit_key[0], suit_key[1], axis="y", period=3.0)
    BOOT = leather(P, "black", "black_dark")
    GOLD = metal(P, "gold", dark="gold_dark")

    def capef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "south" and abs((x * 1.3) % 5.0 - 2.5) < 0.8 and abs((y % 7.0) - 3.5) < 0.8:
            return tone(p["gold"], face), None
        c = p["dark_green"] if look == "x" else p["white"]
        return tone(c if face != "north" else (p["dark_red"] if look == "x" else p["white_dark"]), face), None

    def suitf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if look == "x" and abs(((y + math.atan2(z, x) * 2.0) % 4.0) - 2.0) < 0.35:
            return tone(p["gold"], face), None
        return SUIT(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        glove = BOOT if look == "burst" else fabric(P, "red", "red_dark", axis="y")
        mats = {"skin": suitf, "shin": BOOT, "calf": BOOT, "foot": BOOT, "knee": BOOT, "forearm": glove,
                "hand": glove, "finger": glove}
        a = humanoid(m, mats, bulk=0.75, arm_bulk=0.72, leg_bulk=0.8, name=name)
        bd = a["body"]
        for side in ("leg_left", "leg_right"):                                           # heeled boots
            an = a[side]["ankle"]
            m.box(a[side]["bone"], an[0] - 0.6, 0.0, an[2] + 1.6, an[0] + 0.6, 3.0, an[2] + 2.4, BOOT)
        hd = m.bone("head", bd, (0, 55, 0))
        rose = "white" if look == "burst" else "red"
        m.round_box(hd, 0, -0.4, 2.6, 2.8, 54.0, 60.5, solid(P, rose), cut=1)               # rose hood-mask
        for j in range(6):
            ang = 2 * math.pi * j / 6
            spike(m, hd, (2.4 * math.cos(ang), 59.0, -0.4 + 2.4 * math.sin(ang)), (math.cos(ang), 0.8, math.sin(ang)),
                  1.4, 2.6, solid(P, rose), tip=0.8)
        if look == "x":                                                                  # dark petal crown
            for j in range(9):
                ang = math.radians(-80 + j * 20)
                spike(m, hd, (3.0 * math.sin(ang), 59.0, 1.0), (math.sin(ang) * 0.6, 1, 0.3), 1.6, 6.0,
                      solid(P, "dark_red"), tip=0.8)
        m.box(hd, -2.6, 36.0, 0.6, 2.6, 58.0, 3.0, strands(P, "hair", "hair_dark"))           # long golden hair
        if look != "burst":
            for sx in (-1, 1):                                                           # shoulder petals
                spike(m, bd, (sx * 6.0, 51.0, 0), (sx * 0.8, 0.6, -0.2), 2.4, 6.0,
                      fabric(P, "green", "green_dark", axis="y"), tip=0.8)
            cape(m, bd, 52.0, 16.0, 46.0, capef, z=4.0, flare=1.8, panels=7, seed=8)
            if look == "x":
                m.round_box(bd, 0, 0, 4.6, 3.6, 32.0, 33.6, BOOT, cut=1)
                m.box(bd, -1.0, 46.0, -4.0, 1.0, 48.0, -3.6, gem(P, "brooch", "white"))
        else:                                                                            # glowing petal wings
            wb = m.bone("wings", bd, (0, 46, 4))
            for sx in (-1, 1):
                for j in range(3):
                    ang = math.radians(-20 + j * 35)
                    spike(m, wb, (sx * 3.0, 44.0, 4.0 + j * 0.4), (sx * math.cos(ang), math.sin(ang), 0.3), 4.0, 22.0,
                          solid(P, "pink", glow=True), tip=0.8)
        w = a["arm_right"]["wrist"]                                                      # thorned vine whip
        pts = [w]
        for i in range(1, 7):
            pts.append((w[0] - 2.0 - i * 0.8, w[1] - i * 4.4, w[2] - 2.0 + 2.0 * math.sin(i)))
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, a["arm_right"]["bone"], p0, p1, 1, GOLD if look != "burst" else solid(P, "black"), extend=0.2)
            spike(m, a["arm_right"]["bone"], p1, (-1, 0, 0.2), 0.8, 1.2, GOLD if look != "burst" else solid(P, "black"),
                  tip=0.8)
        return m

    return build
