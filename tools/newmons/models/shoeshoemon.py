"""Shoeshoemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a patchwork squirrel-girl puppet: a stitched orange felt body and a huge patched brown squirrel
tail, long blonde hair and big mouse ears with a safety pin, a smiley badge, a yellow jacket with a red scarf, a white
glove and a mitten hand, and big red roller skates with yellow wheels. 15 blocks.

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import fabric, fur, leather, metal, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a patchwork squirrel-girl puppet in a yellow jacket and red scarf, with blonde hair, big ears, a huge patched tail and red roller skates"
BASE = {"orange": (230, 140, 50), "orange_dark": (160, 80, 20), "brown": (150, 90, 50), "brown_dark": (90, 50, 24),
        "yellow": (250, 210, 60), "yellow_dark": (200, 150, 20), "red": (210, 40, 40), "red_dark": (120, 14, 14),
        "blonde": (250, 230, 140), "blonde_dark": (210, 180, 80), "white": (250, 250, 250), "pink": (240, 160, 170),
        "eye": (80, 180, 80), "steel": (200, 204, 216), "stitch": (90, 50, 30)}
SHINY = {"orange": (170, 170, 186), "orange_dark": (100, 100, 120), "brown": (110, 110, 130), "brown_dark": (60, 60, 76)}


def P(v):
    return pal(BASE, SHINY, v)


FELT = fabric(P, "orange", "orange_dark", axis="y", period=2.0, seam="stitch")


def build():
    m = Model("shoeshoemon")
    mats = {"skin": FELT, "chest": fabric(P, "yellow", "yellow_dark", axis="y"), "abs": fabric(P, "yellow", "yellow_dark"),
            "hand": solid(P, "white"), "finger": solid(P, "white"), "foot": leather(P, "red", "red_dark")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.8, leg_bulk=0.85, name="shoeshoemon")
    bd = a["body"]
    m.round_box(bd, 0, 0, 4.6, 3.6, 49.0, 52.0, fabric(P, "red", "red_dark", axis="x"), cut=1)   # red scarf
    m.box(bd, 2.0, 44.0, -4.6, 3.6, 45.6, -4.3, solid(P, "yellow"))                            # smiley badge
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.8, 3.0, 53.6, 60.0, FELT, cut=1)
    m.round_box(hd, 0, -3.4, 1.6, 0.8, 54.0, 56.6, solid(P, "white"), cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.2), 57.4, -3.7, max(sx * 0.8, sx * 2.2), 58.6, -3.5, solid(P, "eye"))
        ball(m, hd, (sx * 3.6, 62.0, 0), 2.6, fabric(P, "orange", "pink", axis="y"), layers=2, squash=0.4)   # big ears
    m.box(hd, -3.0, 48.0, -1.6, 3.0, 60.6, 3.0, strands(P, "blonde", "blonde_dark"))
    m.box(hd, -3.0, 58.6, -3.4, 3.0, 60.4, -1.6, strands(P, "blonde", "blonde_dark"))
    tl = m.bone("tail", bd, (0, 34, 4))                                                  # huge patched tail
    pts = [(0, 34.0, 4.0), (0, 40.0, 12.0), (2.0, 52.0, 14.0), (4.0, 60.0, 10.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 6 + (1 if i == 1 else 0), fur(P, "brown", "brown_dark", length=1.4), extend=0.8)
    for side in ("leg_left", "leg_right"):                                               # roller skates
        an = a[side]["ankle"]
        for zz in (-3.0, 1.0):
            m.round_box(a[side]["bone"], an[0], an[2] + zz, 0.8, 1.0, 0.0, 1.6, solid(P, "yellow"), cut=0)
    return m
