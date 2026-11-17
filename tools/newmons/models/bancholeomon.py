"""Bancho Leomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the delinquent boss lion. A golden lion-man with a great swept mane of white hair, dark glasses
and a red headband with a sprouting leaf, a broad scarred muscular chest under a long open black coat with gold
buttons, a heavy chain over one shoulder, a studded belt, baggy black trousers, bandaged fists and a katana.
35 blocks tall.

Front is -z, y is up. 68 units tall; Ultimate stage. make(burst=True): Bancho Leomon: Burst Mode (its whole body and
mane blazing gold with fire, the coat thrown back).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid, shell
from _digidetail import (Bulge, cutout, fabric, flame_inside, fur, leather, local, metal, skin, solid, strands,
                         torso_bulges)
from _route import pal, tone

HEIGHT = 68
SCALE, HITBOX = sized(35, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a delinquent boss lion-man: golden fur, a swept white mane, dark glasses and a red headband, a scarred "
        "muscular chest under a long black coat, a chain, bandaged fists and a katana")
BASE = {"gold": (240, 190, 50), "gold_dark": (170, 110, 20), "gold_light": (255, 236, 150), "mane": (226, 226, 236),
        "mane_dark": (150, 150, 166), "coat": (40, 36, 50), "coat_dark": (16, 14, 20), "red": (200, 30, 40),
        "scar": (230, 120, 140), "black": (30, 30, 36), "steel": (200, 204, 216), "steel_dark": (100, 104, 116),
        "bandage": (240, 236, 226), "leaf": (90, 180, 70), "glass": (40, 60, 70), "trouser": (60, 56, 70),
        "trouser_dark": (30, 28, 36), "flame": (255, 200, 60, 220), "flame_core": (255, 250, 200, 235),
        "vein": (220, 160, 40)}
SHINY = {"gold": (230, 230, 240), "gold_dark": (160, 160, 176), "gold_light": (255, 255, 255), "mane": (60, 60, 70),
         "mane_dark": (30, 30, 36), "coat": (120, 30, 40), "coat_dark": (60, 10, 16), "flame": (120, 200, 255, 220)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, burst=False):
    CHEST = skin(P, "gold", dark="gold_dark", light="gold_light", bulges=torso_bulges(0, 51.0, 5.6, abs_rows=4),
                 vein_key="vein", vein_rects=(((-6, 36, 6, 51), ("north",), 3),), vein_count=3, var=0.03)
    ARM = skin(P, "gold", dark="gold_dark", light="gold_light", var=0.03,
               bulges=[Bulge("north", sx * 9.0, 42.0, 1.8, 3.6, light=0.35, shadow=0.45) for sx in (-1, 1)])
    COAT = fabric(P, "coat", "coat_dark", axis="y", period=3.0)
    TROUSER = fabric(P, "trouser", "trouser_dark", axis="y", period=2.4)
    MANE = strands(P, "mane", "mane_dark")
    STEEL = metal(P, "steel", dark="steel_dark")

    def scarf(x, y, z, face, variant, box=None, **k):
        """The chest with its X-shaped scar."""
        p = P(variant)
        if face == "north" and 40.0 < y < 50.0 and min(abs(x - (y - 45.0) * 0.8), abs(x + (y - 45.0) * 0.8)) < 0.35:
            return tone(p["scar"], face), None
        return CHEST(x, y, z, face, variant, box=box, **k)

    def flamef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        c = p["flame_core"] if v / max(H, 1e-6) < 0.35 else p["flame"]
        return c, c[:3]

    def build():
        m = Model(name)
        mats = {"skin": ARM, "chest": scarf, "abs": scarf, "pelvis": leather(P, "black", "coat"), "neck": ARM,
                "deltoid": ARM if burst else COAT, "upper_arm": ARM if burst else COAT, "forearm": ARM,
                "hand": solid(P, "bandage"), "finger": solid(P, "bandage"), "thigh": TROUSER, "knee": TROUSER,
                "shin": TROUSER, "calf": TROUSER, "foot": ARM, "talon": solid(P, "black")}
        a = humanoid(m, mats, bulk=1.25, arm_bulk=1.35, leg_bulk=1.3, digitigrade=True, talons=True, name=name,
                     hand_pose="fist")
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.6, 2.8, 3.0, 54.4, 61.0, ARM, cut=1)
        m.box(hd, -1.8, 54.6, -5.0, 1.8, 57.4, -3.0, ARM)                                # muzzle
        m.box(hd, -2.6, 57.6, -3.8, 2.6, 58.8, -3.4, solid(P, "glass"))                  # dark glasses
        m.box(hd, -3.0, 59.4, -3.2, 3.0, 60.6, 3.2, solid(P, "red"))                     # headband
        rod(m, hd, (1.0, 60.6, -3.0), (2.0, 63.0, -3.6), 1, solid(P, "leaf"), extend=0.2)
        mane = m.bone("mane", hd, (0, 60, 2))
        for i in range(16):                                      # the swept mane
            ang = math.radians(-100 + i * 13)
            base = (2.8 * math.sin(ang), 60.0 + math.cos(ang), 1.0)
            tip = (base[0] * 2.4, base[1] + 4.0 * math.cos(ang) + 2.0, 9.0 + (i % 3) * 2)
            rod(m, mane, base, tip, 2, MANE, extend=0.3, t2=2)
        rod(m, bd, (5.0, 52.0, -3.6), (-4.0, 31.0, -4.4), 1, STEEL, extend=0.2)          # the chain
        m.box(bd, -5.4, 30.6, -4.6, 5.4, 33.4, 4.4, leather(P, "black", "coat", stitch="steel"))
        for nm in ("arm_left", "arm_right"):                     # bandaged wrists
            w = a[nm]["wrist"]
            rod(m, a[nm]["bone"], w, (w[0], w[1] + 3.0, w[2]), 4, solid(P, "bandage"), extend=0)
        ar = a["arm_right"]                                      # the katana
        h = ar["hand"]
        kb = m.bone("sword", ar["bone"], h)
        rod(m, kb, (h[0], h[1] + 1.0, h[2]), (h[0], h[1] - 4.0, h[2]), 1, solid(P, "black"), extend=0)
        rod(m, kb, (h[0], h[1] - 4.0, h[2]), (h[0] - 2.0, h[1] - 30.0, h[2] + 6.0), 1, STEEL, extend=0, t2=2)
        if burst:                                                # flames blazing from its body and mane
            fl = m.bone("cap", bd, (0, 50, 4))
            for j, ang in enumerate((-40, 0, 40)):
                m.box(fl, -12.0, 36.0, 4.0 + j, 12.0, 74.0, 4.0 + j, cutout(flame_inside(6, 0.1, j), flamef),
                      rotation=(0, 0, ang * 0.5), pivot=(0, 50, 4.0 + j))
            for nm in ("arm_left", "arm_right"):
                h = a[nm]["hand"]
                m.box(a[nm]["bone"], h[0] - 3.0, h[1] - 2.0, h[2], h[0] + 3.0, h[1] + 9.0, h[2],
                      cutout(flame_inside(3, 0.0, 3), flamef))
        else:                                                    # the long open black coat
            cb = m.bone("cap", bd, (0, 52, 3))
            cape(m, cb, 52.0, 18.0, 46.0, COAT, z=4.6, flare=0.8, panels=8, sweep=(0, 4))
            for sx in (-1, 1):
                m.box(bd, min(sx * 4.6, sx * 7.0), 10.0, -4.0, max(sx * 4.6, sx * 7.0), 50.0, -3.4, COAT,
                      rotation=(-4, sx * 20, 0), pivot=(sx * 5.0, 50.0, -3.6))           # coat fronts
        return m
    return build


build = make("bancholeomon")
