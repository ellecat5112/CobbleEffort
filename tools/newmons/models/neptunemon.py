"""Neptunemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Olympos god of the sea: a warrior king in blue scale armour over a violet robe with a long
red sash, a silver winged helm and beard-like face guard, one huge silver gauntlet raised, a great silver trident with
a shark-toothed head, and below the waist a vast blue fish body with fin-blades and a forked tail. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, fabric, metal, scales, skin, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = ("a sea-god king in blue scale armour over a violet robe with a red sash, a silver winged helm, a huge silver "
        "gauntlet, a shark-toothed trident and a vast blue fish body")
BASE = {"blue": (60, 120, 200), "blue_dark": (20, 50, 120), "blue_light": (150, 200, 250), "violet": (110, 70, 160),
        "violet_dark": (54, 30, 90), "red": (200, 40, 40), "red_dark": (120, 14, 18), "silver": (210, 214, 226),
        "silver_dark": (110, 116, 130), "gold": (230, 190, 70), "skin": (230, 190, 160), "eye": (60, 120, 200),
        "fin": (190, 220, 240)}
SHINY = {"blue": (60, 160, 120), "blue_dark": (20, 90, 60), "blue_light": (150, 230, 190), "violet": (180, 60, 60)}


def P(v):
    return pal(BASE, SHINY, v)


SCALE_ = scales(P, "blue", "blue_dark", size=1.4, light="blue_light")
SILVER = metal(P, "silver", dark="silver_dark")


def build():
    m = Model("neptunemon")
    mats = {"skin": SCALE_, "chest": SCALE_, "abs": fabric(P, "violet", "violet_dark"), "pelvis": SCALE_,
            "neck": skin(P, "skin", dark="red_dark"), "deltoid": armour(P, "silver", "silver_dark", trim="gold"),
            "upper_arm": fabric(P, "violet", "violet_dark"), "forearm": SILVER, "hand": SILVER, "finger": SILVER}
    a = humanoid(m, mats, bulk=1.15, arm_bulk=1.1, leg_bulk=1.0, name="neptunemon")
    m.boxes[:] = [b for b in m.boxes if b.bone not in ("leg_left", "leg_right")]          # a fish body below
    m.bones[:] = [b for b in m.bones if b["name"] not in ("leg_left", "leg_right")]
    bd = a["body"]
    ball(m, bd, (0, 22.0, 2.0), 11.0, SCALE_, layers=6, ry=12.0, squash=0.9)              # vast fish body
    tb = m.bone("tail", bd, (0, 10, 8))
    pts = [(0, 12.0, 8.0), (0, 6.0, 16.0), (0, 4.0, 24.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 5, SCALE_, extend=0.6)
    for s in (-1, 1):                                                                    # forked tail
        m.box(tb, -0.4, 2.0, 24.0, 0.4, 6.0, 32.0, solid(P, "fin"), rotation=(s * 30, 0, 0), pivot=(0, 4.0, 24.0))
    for sx in (-1, 1):                                                                   # fin-blades
        for j in range(3):
            spike(m, bd, (sx * 9.0, 16.0 + j * 6.0, 4.0), (sx * 1, -0.3, 0.6), 1.6, 9.0 - j, solid(P, "fin"), tip=0.8)
    m.box(bd, -1.6, 20.0, -9.6, 1.6, 50.0, -9.0, fabric(P, "red", "red_dark"))            # long red sash
    for sx in (-1, 1):
        m.box(bd, sx * 6.0 - 1.5, 34.0, 3.0, sx * 6.0 + 1.5, 50.0, 3.6, fabric(P, "red", "red_dark"),
              rotation=(15, 0, sx * 20), pivot=(sx * 6.0, 50.0, 3.0))
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 59.6, skin(P, "skin", dark="red_dark"), cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.6), 57.4, -2.9, max(sx * 0.6, sx * 1.6), 58.0, -2.8, solid(P, "eye"))
        spike(m, hd, (sx * 2.8, 59.0, 0), (sx * 0.8, 0.8, 0.4), 1.4, 6.0, SILVER, tip=0.8)    # winged helm
    m.round_box(hd, 0, 0, 3.0, 3.2, 58.6, 61.6, armour(P, "silver", "silver_dark", trim="gold"), cut=1)
    spike(m, hd, (0, 61.4, -1.0), (0, 1, 0.3), 1.4, 5.0, metal(P, "gold"), tip=0.8)
    m.round_box(hd, 0, -2.0, 2.2, 1.0, 53.4, 56.0, SILVER, cut=0)                         # face guard
    al = a["arm_left"]                                                                   # huge raised gauntlet
    w = al["wrist"]
    ball(m, al["bone"], (w[0] + 2.0, w[1] - 2.0, w[2] - 1.0), 4.4, SILVER, layers=4)
    for f in range(4):
        m.round_box(al["bone"], w[0] + 2.0 + (f - 1.5) * 1.8, w[2] - 5.4, 0.9, 1.0, w[1] - 4.0, w[1] + 3.0, SILVER, cut=0)
    ar = a["arm_right"]                                                                  # shark-toothed trident
    h = ar["hand"]
    rod(m, ar["bone"], (h[0], h[1] - 20.0, h[2]), (h[0], h[1] + 20.0, h[2]), 1, metal(P, "gold"), extend=0.2, t2=1)
    for sx in (-1, 0, 1):
        spike(m, ar["bone"], (h[0] + sx * 2.0, h[1] + 20.0, h[2]), (sx * 0.2, 1, 0), 1.6, 6.0 - abs(sx) * 2.0, SILVER,
              tip=0.8)
    m.box(ar["bone"], h[0] - 3.0, h[1] + 19.0, h[2] - 0.6, h[0] + 3.0, h[1] + 20.4, h[2] + 0.6, SILVER)
    return m
