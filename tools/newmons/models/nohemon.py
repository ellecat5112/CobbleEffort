"""Nohemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the scarecrow puppet: a pale stitched sack face with a straw fringe under a brown wide-brimmed hat with
a lamp, a green patched tunic belted brown, a red scarf streaming behind, brown leather gloves and boots, a crossbow
and a blue crow perched on its raised fist. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import fabric, leather, metal, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a scarecrow puppet with a stitched sack face, a wide brown hat with a lamp, a green patched tunic, a red scarf, "
        "leather gloves and boots, a crossbow and a blue crow on its fist")
BASE = {"sack": (230, 220, 190), "sack_dark": (170, 160, 130), "straw": (230, 200, 90), "green": (80, 120, 60),
        "green_dark": (40, 70, 30), "brown": (130, 80, 40), "brown_dark": (70, 40, 18), "red": (210, 50, 30),
        "red_dark": (130, 20, 10), "blue": (60, 90, 200), "yellow": (250, 200, 50), "black": (30, 28, 32),
        "lamp": (255, 230, 120)}
SHINY = {"green": (90, 90, 160), "green_dark": (40, 40, 100), "red": (230, 190, 60), "red_dark": (160, 120, 20)}


def P(v):
    return pal(BASE, SHINY, v)


SACK = fabric(P, "sack", "sack_dark")
TUNIC = fabric(P, "green", "green_dark", seam="brown")
LEATHER = leather(P, "brown", "brown_dark", stitch="black")


def build():
    m = Model("nohemon")
    mats = {"skin": SACK, "chest": TUNIC, "abs": TUNIC, "pelvis": TUNIC, "neck": SACK, "deltoid": TUNIC,
            "upper_arm": TUNIC, "forearm": LEATHER, "hand": LEATHER, "finger": LEATHER, "thigh": SACK, "knee": SACK,
            "shin": LEATHER, "calf": LEATHER, "foot": LEATHER, "toe": LEATHER}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.9, leg_bulk=0.9, name="nohemon")
    bd = a["body"]
    m.round_box(bd, 0, 0.4, 4.4, 3.4, 33.0, 35.0, LEATHER, cut=1)                         # belt
    for j in range(5):                                                                   # streaming red scarf
        m.box(bd, -6.0 - j * 3.0, 49.0 - j * 1.6, 2.0, -3.0 - j * 3.0, 51.0 - j * 1.6, 2.2, fabric(P, "red", "red_dark"),
              rotation=(0, 0, 15), pivot=(-4.5 - j * 3.0, 50.0 - j * 1.6, 2.1))
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.6, 2.8, 54.0, 60.0, SACK, cut=1)                           # stitched sack face
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.6), 57.4, -3.1, max(sx * 0.6, sx * 1.6), 58.0, -2.95, solid(P, "black"))
    m.box(hd, -1.6, 55.4, -3.05, 1.6, 55.8, -2.95, solid(P, "black"))
    for i in range(8):                                                                   # straw fringe
        ang = math.radians(-90 + i * 26)
        spike(m, hd, (2.6 * math.sin(ang), 58.6, -2.0 * math.cos(ang)), (math.sin(ang) * 0.5, -0.6, -0.4), 1.0, 3.0,
              strands(P, "straw", "brown"), tip=0.8)
    m.round_box(hd, 0, 0, 5.6, 5.4, 60.0, 60.8, LEATHER, cut=1)                           # wide-brimmed hat
    m.round_box(hd, 0, 0, 3.0, 3.0, 60.8, 63.4, LEATHER, cut=1)
    ball(m, hd, (2.4, 62.0, -3.0), 0.9, solid(P, "lamp", glow=True), layers=1)
    al = a["arm_left"]                                                                   # crow on raised fist
    w = al["hand"]
    ball(m, al["bone"], (w[0], w[1] + 3.0, w[2]), 2.0, solid(P, "blue"), layers=3)
    ball(m, al["bone"], (w[0], w[1] + 5.6, w[2] - 0.6), 1.4, solid(P, "blue"), layers=2)
    spike(m, al["bone"], (w[0], w[1] + 5.4, w[2] - 2.0), (0, -0.2, -1), 1.0, 2.0, solid(P, "yellow"), tip=0.8)
    for sx in (-1, 1):
        x0, x1 = sorted((w[0] + sx * 1.4, w[0] + sx * 5.0))
        m.box(al["bone"], x0, w[1] + 2.0, w[2], x1, w[1] + 5.0, w[2], solid(P, "blue"), rotation=(0, 0, sx * 30),
              pivot=(w[0] + sx * 1.4, w[1] + 3.5, w[2]))
    ar = a["arm_right"]                                                                  # crossbow
    h = ar["hand"]
    rod(m, ar["bone"], (h[0], h[1], h[2]), (h[0], h[1] + 1.0, h[2] - 8.0), 1, solid(P, "brown"), extend=0.2, t2=2)
    m.box(ar["bone"], h[0] - 4.0, h[1] + 0.6, h[2] - 7.0, h[0] + 4.0, h[1] + 1.4, h[2] - 6.4, solid(P, "brown_dark"))
    return m
