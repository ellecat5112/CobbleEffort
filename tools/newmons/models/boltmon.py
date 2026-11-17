"""Boltmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the patchwork brute. A towering green-skinned bruiser stitched together and studded with steel
bolts, a red spiked crest, a steel mask over the lower face, a great double-bladed axe strapped across its back,
enormous green fists with bolted knuckles, a harness of black straps and buckles, black trousers and brown boots
capped in spiked steel. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import (Bulge, cutout, eye, fabric, leather, local, metal, skin, solid, torso_bulges)
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a towering stitched green bruiser studded with steel bolts: a red spiked crest, a steel mask, a great "
        "double axe on its back, enormous fists, black strap harness and spiked steel-capped boots")
BASE = {"green": (150, 210, 110), "green_dark": (70, 130, 50), "green_light": (210, 250, 170), "stitch": (40, 50, 30),
        "steel": (210, 214, 226), "steel_dark": (100, 104, 116), "red": (210, 40, 40), "black": (36, 34, 42),
        "black_light": (90, 88, 100), "brown": (150, 96, 50), "brown_dark": (90, 54, 24), "eye": (250, 220, 60),
        "pupil": (30, 20, 10), "white": (255, 255, 255), "vein": (110, 170, 80)}
SHINY = {"green": (170, 160, 220), "green_dark": (90, 80, 150), "green_light": (230, 220, 255), "red": (250, 200, 50)}


def P(v):
    return pal(BASE, SHINY, v)


CHEST = skin(P, "green", dark="green_dark", light="green_light", bulges=torso_bulges(0, 51.0, 6.2, abs_rows=4),
             vein_key="vein", vein_rects=(((-6, 36, 6, 51), ("north",), 3),), var=0.03)
ARM = skin(P, "green", dark="green_dark", light="green_light", var=0.03,
           bulges=[Bulge("north", sx * 9.6, 42.0, 2.0, 3.8, light=0.35, shadow=0.45) for sx in (-1, 1)])
STEEL = metal(P, "steel", dark="steel_dark")
STRAP = leather(P, "black", "black_light", stitch="steel")
TROUSER = fabric(P, "black", "black_light", axis="y", period=2.6)
BOOT = leather(P, "brown", "brown_dark")


def stitched(sh):
    """Skin crossed by dark stitch seams (a zigzag line with cross-stitches)."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        for c in (44.0, 38.0):
            if abs(y - c - 0.6 * math.sin(x * 0.8)) < 0.18 or (abs(y - c) < 0.6 and (x * 2.0) % 1.4 < 0.2):
                return tone(p["stitch"], face), None
        return sh(x, y, z, face, variant, box=box, **k)
    return s


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            c = eye(p, x - sx * 1.2, y - 58.6, 0.6, "eye")
            if c is not None:
                return c, None
        if abs(y - 60.2) < 0.15 and abs(x) < 2.4:
            return tone(p["stitch"], face), None
    return ARM(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("boltmon")
    mats = {"skin": ARM, "chest": stitched(CHEST), "abs": stitched(CHEST), "pelvis": STRAP, "neck": ARM,
            "deltoid": ARM, "upper_arm": ARM, "forearm": ARM, "hand": ARM, "finger": ARM, "thigh": TROUSER,
            "knee": STEEL, "shin": TROUSER, "calf": TROUSER, "foot": BOOT, "toe": STEEL}
    a = humanoid(m, mats, bulk=1.35, arm_bulk=1.4, leg_bulk=1.3, name="boltmon", hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.8, 3.0, 54.2, 62.0, headf, cut=1)
    m.box(hd, -2.6, 54.0, -3.8, 2.6, 57.4, -2.6, STEEL)                                   # steel mask
    for i in range(4):
        m.box(hd, -2.0 + i * 1.3, 54.6, -3.9, -1.6 + i * 1.3, 56.8, -3.75, solid(P, "black"))
    for i in range(6):                                                                    # red spiked crest
        spike(m, hd, (0, 61.6, -2.0 + i * 1.0), (0, 1, 0.3 + 0.15 * i), 1.6, 4.0 - 0.3 * abs(i - 2), solid(P, "red"),
              tip=0.5)
    for sx in (-1, 1):                                                                    # neck and shoulder bolts
        rod(m, bd, (sx * 2.0, 53.0, 0), (sx * 4.6, 53.4, 0), 1, STEEL, extend=0)
        m.box(bd, sx * 4.6 - 0.8, 52.4, -0.8, sx * 4.6 + 0.8, 54.4, 0.8, STEEL)
        m.box(bd, min(sx * 6.0, sx * 9.6), 51.6, -1.0, max(sx * 6.0, sx * 9.6), 52.6, 1.0, STEEL)
    for sx in (-1, 1):                                                                    # the strap harness
        rod(m, bd, (sx * 5.6, 51.4, -4.6), (-sx * 4.6, 35.0, -4.8), 1, STRAP, extend=0.2, t2=2)
        rod(m, bd, (sx * 5.6, 51.4, 3.8), (-sx * 4.6, 35.0, 4.0), 1, STRAP, extend=0.2, t2=2)
    m.box(bd, -1.4, 42.0, -5.6, 1.4, 44.4, -4.8, STEEL)                                   # buckle
    # enormous green fists with bolted knuckles
    for nm in ("arm_left", "arm_right"):
        ab = a[nm]
        h = ab["hand"]
        sx = 1 if nm == "arm_left" else -1
        m.round_box(ab["bone"], h[0] + sx * 0.6, h[2], 4.6, 4.6, h[1] - 7.0, h[1] + 1.6, ARM, cut=2)
        for j in range(4):
            spike(m, ab["bone"], (h[0] + sx * 0.6 - 3.0 + j * 2.0, h[1] - 2.0, h[2] - 4.4), (0, 0, -1), 1.0, 1.4,
                  STEEL)
        m.box(ab["bone"], h[0] - 3.2, h[1] + 1.4, h[2] - 3.2, h[0] + 3.2, h[1] + 3.0, h[2] + 3.2, STRAP)
    # the great double axe across its back
    ab = m.bone("axe", bd, (0, 46, 5))
    rod(m, ab, (-8.0, 30.0, 5.6), (8.0, 62.0, 5.6), 1, solid(P, "brown_dark"), extend=0)
    c = (6.0, 58.0, 5.8)
    for sx in (-1, 1):
        def blade(x, y, z, f, b, sx=sx):
            u, v, W, H = local(x, y, z, f, b)
            du, dv = u / max(W, 1e-6), v / max(H, 1e-6) - 0.5
            du = du if sx > 0 else 1 - du
            return abs(dv) < 0.15 + 0.4 * du
        x0, x1 = sorted((c[0], c[0] + sx * 8.0))
        m.box(ab, x0, c[1] - 6.0, c[2], x1, c[1] + 6.0, c[2], cutout(blade, STEEL), rotation=(0, 0, 27),
              pivot=c)
    # spiked steel toe caps on the boots
    for nm in ("leg_left", "leg_right"):
        lg = a[nm]
        an = lg["ankle"]
        m.round_box(lg["bone"], an[0], an[2] - 2.0, 2.8, 3.0, 0.0, 3.4, STEEL, cut=1)
        for sx in (-1, 1):
            spike(m, lg["bone"], (an[0] + sx * 2.8, 2.4, an[2]), (sx, 0.2, 0), 1.0, 2.0, STEEL)
            spike(m, lg["bone"], (an[0] + sx * 2.2, 18.0, -1.4), (sx, 0.3, -0.3), 1.0, 2.2, STEEL)
    return m
