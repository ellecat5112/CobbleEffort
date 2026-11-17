"""Etemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the rock
'n' roll monkey king. A stitched-together orange plush monkey with a cream face and belly, black sunglasses, a wide
loud grin, a pompadour quiff, a little yellow teddy-bear charm on a cord round its neck, long arms with big grasping
hands held up high, and a long curling tail. 25 blocks tall.

Front is -z, y is up. 48 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fur, metal, skin, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a stitched orange plush monkey with a cream face, black sunglasses, a loud grin, a pompadour, a teddy-bear "
        "charm, big grasping hands held high and a curling tail")
BASE = {"orange": (240, 130, 40), "orange_dark": (170, 70, 10), "cream": (250, 236, 210), "cream_dark": (200, 180, 150),
        "black": (24, 24, 28), "stitch": (90, 50, 20), "mouth": (180, 30, 40), "tooth": (250, 250, 246),
        "yellow": (250, 210, 60)}
SHINY = {"orange": (120, 120, 140), "orange_dark": (60, 60, 76)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "orange", "orange_dark", length=1.2, density=2.4)
CREAM = skin(P, "cream", dark="cream_dark")


def stitchedf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west") and abs((x * 0.7 + y) % 9.0 - 4.5) < 0.12 and (y * 3) % 1.0 < 0.5:
        return tone(p["stitch"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if abs(y - 49.0) < 0.9 and abs(x) < 3.2 and not abs(x) < 0.4:
            return tone(p["black"], face), None                         # sunglasses
        if 43.6 < y < 46.6 and abs(x) < 3.0 - (46.6 - y) * 0.3:
            return tone(p["tooth"] if y > 45.8 else p["mouth"], face), None   # loud grin
    return CREAM(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("etemon")
    mats = {"skin": stitchedf, "chest": CREAM, "abs": CREAM, "pelvis": stitchedf, "neck": stitchedf,
            "deltoid": stitchedf, "upper_arm": stitchedf, "forearm": stitchedf, "hand": CREAM, "finger": CREAM,
            "thigh": stitchedf, "knee": stitchedf, "shin": stitchedf, "calf": stitchedf, "foot": CREAM, "toe": CREAM}
    a = humanoid(m, mats, bulk=0.9, arm_bulk=1.1, leg_bulk=1.0, hand_pose="open", name="etemon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 52, 0))
    m.round_box(hd, 0, 0, 4.0, 3.8, 41.0, 53.0, stitchedf, cut=1)                     # big monkey head
    m.round_box(hd, 0, -3.2, 3.4, 1.0, 42.0, 51.0, facef, cut=1)
    for sx in (-1, 1):
        m.round_box(hd, sx * 4.6, 0, 1.4, 1.0, 46.0, 49.0, CREAM, cut=0)            # ears
    for i in range(5):                                                               # pompadour quiff
        spike(m, hd, ((i - 2) * 0.8, 53.0, -1.0), ((i - 2) * 0.2, 0.6, -1), 1.6, 5.0, FUR, tip=0.5)
    for j in range(5):                                                               # cord + teddy charm
        m.box(bd, -0.3 + (j % 2) * 0.2, 40.0 - j * 0.8, -4.2, 0.3 + (j % 2) * 0.2, 40.8 - j * 0.8, -3.8, solid(P, "black"))
    m.round_box(bd, 0, -4.4, 1.4, 1.0, 34.0, 36.6, solid(P, "yellow"), cut=0)
    for nm in ("arm_left", "arm_right"):                                             # big grasping hands
        hx, hy, hz = a[nm]["hand"]
        m.round_box(a[nm]["bone"], hx, hz, 2.6, 2.2, hy - 3.0, hy + 1.0, CREAM, cut=1)
    tl = m.bone("tail", bd, (0, 30, 3))
    pts = [(0, 30.0, 3.0), (4.0, 26.0, 8.0), (10.0, 28.0, 10.0), (13.0, 34.0, 8.0), (11.0, 38.0, 6.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 2, stitchedf, extend=0.5)
    return m
