"""Bagramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the emperor of the Bagra Army. A tall demon lord in a white long coat with gold chest plates over a
muscled grey body, a horned silver helm with a white beard, a navy-lined black cape, and in place of its right arm a
huge grafted skeletal arm of bone with crimson claws. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage. make(archangel=True): Bagramon (Archangel Form) (the hooded
angel it once was: a long white robe and hood, long black hair, white wings, gentle hands; no bone arm).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, dome, humanoid, shell
from _digidetail import armour, fabric, feathers, metal, skin, solid, strands, torso_bulges
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a demon lord emperor in a white long coat with gold chest plates, a horned silver helm with a white beard, a "
        "black cape and a huge grafted skeletal bone arm with crimson claws")
BASE = {"white": (240, 240, 244), "white_dark": (180, 182, 196), "gold": (236, 196, 60), "gold_dark": (160, 120, 30),
        "gold_light": (255, 240, 170), "grey": (150, 150, 160), "grey_dark": (80, 80, 90), "grey_light": (210, 210, 220),
        "silver": (200, 204, 216), "silver_dark": (100, 104, 116), "bone": (226, 216, 190), "bone_dark": (160, 146, 120),
        "red": (200, 30, 40), "cape": (30, 30, 40), "cape_lining": (40, 50, 130), "hair": (30, 28, 34),
        "hair_light": (90, 86, 100), "skin": (240, 224, 214), "skin_dark": (200, 170, 160), "eye": (255, 60, 60)}
SHINY = {"white": (60, 56, 70), "white_dark": (24, 22, 30), "gold": (200, 60, 60), "gold_dark": (130, 20, 20),
         "cape": (220, 216, 230), "cape_lining": (180, 40, 60), "bone": (90, 80, 70), "bone_dark": (50, 44, 36)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, archangel=False):
    COAT = fabric(P, "white", "white_dark", axis="y", period=3.0)
    GOLD = armour(P, "gold", "gold_dark", light="gold_light")
    SILVER = armour(P, "silver", "silver_dark")
    BONE = armour(P, "bone", "bone_dark", seams=(2.0,))
    BODY = skin(P, "grey", dark="grey_dark", light="grey_light", bulges=torso_bulges(0, 50.5, 5.4, abs_rows=4))

    def build():
        m = Model(name)
        mats = {"skin": COAT, "chest": COAT if archangel else BODY, "abs": COAT if archangel else BODY,
                "pelvis": COAT, "neck": COAT, "deltoid": COAT, "upper_arm": COAT, "forearm": COAT,
                "hand": skin(P, "skin", dark="skin_dark"), "finger": skin(P, "skin", dark="skin_dark"),
                "thigh": COAT, "knee": COAT, "shin": COAT, "calf": COAT, "foot": SILVER, "toe": SILVER}
        a = humanoid(m, mats, bulk=1.05, arm_bulk=1.0, leg_bulk=1.0, name=name, hand_pose="open")
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, 0, 2.4, 2.6, 54.6, 60.6, skin(P, "skin", dark="skin_dark"), cut=1)
        sk = m.bone("skirt", bd, (0, 32, 0))
        for i in range(10):                                      # long coat / robe skirt
            ang = math.radians(-162 + i * 36)
            c = (4.8 * math.sin(ang), 32.0, -4.2 * math.cos(ang))
            if not archangel and math.cos(ang) < -0.8:
                continue                                         # the coat is open at the front
            m.box(sk, c[0] - 1.8, 2.0 if archangel else 8.0, c[2], c[0] + 1.8, 32.0, c[2] + 0.8, COAT,
                  rotation=(-6 * math.cos(ang), -math.degrees(ang), 0), pivot=c)
        if archangel:
            m.round_box(hd, 0, 0.6, 3.2, 3.2, 56.0, 62.4, COAT, cut=1)                  # the hood
            hr = m.bone("mane", hd, (0, 58, 2))
            for i in range(9):                                   # long black hair
                xx = -3.0 + i * 0.75
                rod(m, hr, (xx, 59.0, 1.0), (xx * 1.4, 30.0 - (i % 3) * 3, 4.0), 2, strands(P, "hair", "hair",
                    tip="hair_light"), extend=0.3)
            for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
                wb = m.bone(nm, bd, (sx * 3.0, 49.0, 3.0))
                W = feathers(P, "white", "white_dark", size=(1.4, 3.0), flow=(0, -1))
                for i in range(10):
                    t = i / 9
                    base = (sx * (3.0 + 12.0 * t), 49.0 + 14.0 * t, 3.0 + 4.0 * t)
                    ln = 12.0 + 14.0 * t
                    m.box(wb, base[0] - 1.8, base[1] - ln, base[2], base[0] + 1.8, base[1], base[2], W,
                          rotation=(-10, 0, -sx * (50 - 35 * t)), pivot=base)
            return m
        m.box(hd, -2.6, 57.2, -2.9, 2.6, 61.2, 2.8, SILVER)                              # horned helm
        m.box(hd, -0.9, 57.4, -3.1, 0.9, 58.2, -2.9, solid(P, "eye", glow=True))
        for sx in (-1, 1):
            pts = [(sx * 2.4, 60.0, 0.0), (sx * 5.0, 63.0, 0.6), (sx * 6.0, 67.0, 2.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, hd, p0, p1, 2, solid(P, "red"), extend=0.3)
        m.box(hd, -1.8, 51.0, -3.0, 1.8, 55.4, -2.2, strands(P, "white", "white_dark"))  # white beard
        for sx in (-1, 1):                                       # gold chest plates and collar
            m.box(bd, min(sx * 0.4, sx * 5.0), 44.0, -5.6, max(sx * 0.4, sx * 5.0), 50.0, -4.4, GOLD)
        shell(m, bd, (0, 0, 0.4), 4.0, 50.6, 53.0, -100, 100, 8, 1.0, GOLD)
        m.box(bd, -2.0, 28.0, -4.6, 2.0, 32.0, -3.8, GOLD)
        cb = m.bone("cap", bd, (0, 51, 4))
        cape(m, cb, 52.0, 20.0, 50.0, fabric(P, "cape", "cape_lining"), z=5.0, flare=0.9, panels=9, sweep=(0, 6))
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            sh = a[nm]["shoulder"]
            dome(m, a[nm]["bone"], (sh[0] + sx * 1.2, 50.0, 0.3), 3.8, 3.4, GOLD, layers=3)
        ar = a["arm_right"]                                      # the grafted skeletal arm
        sh = ar["shoulder"]
        ba = m.bone("bone_arm", ar["bone"], sh)
        pts = [(sh[0] - 1.0, 49.0, 0.0), (sh[0] - 6.0, 38.0, -4.0), (sh[0] - 8.0, 26.0, -10.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ba, p0, p1, 4, BONE, extend=0.6)
            rod(m, ba, (p0[0] - 1.0, p0[1], p0[2] + 1.0), (p1[0] - 1.0, p1[1], p1[2] + 1.0), 2, BONE, extend=0.4)
        h = pts[-1]
        m.round_box(ba, h[0], h[2], 3.4, 3.0, h[1] - 3.0, h[1] + 1.0, BONE, cut=1)
        for f in range(4):
            spike(m, ba, (h[0] + (f - 1.5) * 1.4, h[1] - 3.0, h[2] - 1.0), (0, -1, -0.5), 1.2, 6.0, solid(P, "red"),
                  tip=0.5)
        return m
    return build


build = make("bagramon")
