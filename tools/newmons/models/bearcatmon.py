"""Bearcatmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a bearcat skater-brawler. Shaggy black fur and a great bushy grey tail, a white-and-blue sports
suit, an orange-and-blue striped armoured right arm with a star and steel spikes on its fist, a spiked shoulder pad,
dark leggings and jet-skate boots with orange claws. 25 blocks tall.

Front is -z, y is up. 60 units tall (the tail); Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, fabric, fur, local, metal, solid, strands
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(25, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 14}
LOOK = ("a bearcat skater-brawler: black fur, a bushy grey tail, a white-and-blue sports suit, an orange-and-blue "
        "striped armoured arm with a spiked fist, and jet-skate boots with orange claws")
BASE = {"fur": (40, 38, 44), "fur_dark": (16, 14, 18), "fur_light": (110, 106, 120), "grey": (150, 146, 156),
        "grey_dark": (90, 86, 96), "white": (240, 242, 248), "white_dark": (180, 184, 198), "blue": (40, 70, 170),
        "orange": (240, 120, 40), "orange_dark": (170, 70, 16), "steel": (200, 204, 216), "steel_dark": (100, 104, 116),
        "legging": (90, 60, 50), "legging_dark": (50, 30, 24), "eye": (240, 50, 50), "star": (250, 220, 60),
        "boot": (40, 40, 48)}
SHINY = {"fur": (220, 200, 160), "fur_dark": (160, 140, 100), "fur_light": (250, 236, 210), "blue": (200, 40, 60),
         "orange": (60, 200, 220), "orange_dark": (20, 120, 140)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "fur", "fur_dark", tip="fur_light", length=1.4)
SUIT = fabric(P, "white", "white_dark", axis="y", period=3.0)
STEEL = metal(P, "steel", dark="steel_dark")


def stripedarm(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = (box.lo[2] + box.size[2] - z) if box else 0
    if face == "north" and abs(x + 11.0) < 1.0 and abs(y - 36.0) < 1.0:
        return p["star"], None
    return tone(p["orange"] if (t % 3.0) < 1.8 else p["blue"], face), None


def suitf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and abs(y % 6.0 - 3.0) < 0.5:
        return tone(p["blue"], face), None
    return SUIT(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("bearcatmon")
    mats = {"skin": FUR, "chest": suitf, "abs": suitf, "pelvis": suitf, "neck": FUR, "deltoid": FUR,
            "upper_arm": FUR, "forearm": FUR, "hand": FUR, "finger": FUR, "thigh": suitf,
            "knee": fabric(P, "legging", "legging_dark"), "shin": fabric(P, "legging", "legging_dark"),
            "calf": fabric(P, "legging", "legging_dark"), "foot": solid(P, "boot"), "talon": solid(P, "orange")}
    a = humanoid(m, mats, bulk=1.05, arm_bulk=1.1, leg_bulk=1.15, digitigrade=True, talons=True, name="bearcatmon",
                 hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 3.0, 3.0, 54.4, 61.0, FUR, cut=1)
    m.box(hd, -1.8, 54.6, -5.0, 1.8, 57.4, -3.0, FUR)                                    # muzzle
    for sx in (-1, 1):
        m.box(hd, sx * 1.4 - 0.5, 58.0, -3.7, sx * 1.4 + 0.5, 58.8, -3.5, solid(P, "eye", glow=True))
        m.round_box(hd, sx * 2.6, 0.0, 1.2, 1.0, 60.4, 62.8, FUR, cut=1)                 # ears
        spike(m, hd, (sx * 2.0, 61.0, 0.6), (sx * 0.2, 1, 0.3), 1.0, 2.6, solid(P, "white"))   # horn tufts
    ar = a["arm_right"]                                          # striped armoured arm with spiked fist
    el, wr, h = ar["elbow"], ar["wrist"], ar["hand"]
    rod(m, ar["bone"], el, wr, 5, stripedarm, extend=0.5)
    m.round_box(ar["bone"], h[0], h[2], 3.0, 3.0, h[1] - 3.4, h[1] + 2.0, armour(P, "orange", "orange_dark"), cut=1)
    for j in range(4):
        spike(m, ar["bone"], (h[0] - 3.0, h[1] - 2.0 + j * 1.2, h[2]), (-1, 0, -0.3), 1.0, 3.0, STEEL)
    sh = ar["shoulder"]
    for j in range(5):                                           # spiked shoulder pad
        ang = math.radians(-60 + j * 30)
        spike(m, ar["bone"], (sh[0] - 2.4, 51.0, 0.0), (-math.cos(ang), math.sin(ang) + 0.4, 0.2), 1.6, 5.0, STEEL,
              tip=0.6)
    tl = m.bone("tail", bd, (0, 32, 4))                          # great bushy tail
    pts = [(0, 32, 4), (4, 40, 12), (10, 50, 16), (18, 54, 16)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 7 - j, fur(P, "grey", "grey_dark", length=2.0), extend=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):          # jet-skate boots
        an = a[nm]["ankle"]
        m.box(a[nm]["bone"], an[0] - 2.2, 0.0, an[2] - 4.0, an[0] + 2.2, 3.6, an[2] + 3.0, solid(P, "boot"))
        m.round_box(a[nm]["bone"], an[0], an[2] + 3.6, 1.2, 1.2, 1.0, 3.0, metal(P, "orange", dark="orange_dark"),
                    cut=1)
    return m
