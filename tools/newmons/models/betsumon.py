"""Betsumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a puppet in a white cat suit. A stitched white plush body with a sleepy smug cat face, big pink-lined
ears tipped violet, huge yellow paw-gloves striped red with steel claws, a long tail ending in a violet tuft and a
steel ring, and clawed white feet. 25 blocks tall.

Front is -z, y is up. 60 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import fabric, fur, local, metal, plane, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(25, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a puppet in a stitched white cat suit: a sleepy smug face, big pink-lined ears tipped violet, huge yellow "
        "red-striped paw-gloves with steel claws and a tail with a violet tuft and a steel ring")
BASE = {"white": (246, 246, 248), "white_dark": (190, 190, 200), "pink": (240, 160, 200), "violet": (150, 110, 210),
        "yellow": (250, 210, 70), "yellow_dark": (200, 150, 30), "red": (220, 60, 40), "steel": (200, 204, 216),
        "steel_dark": (100, 104, 116), "black": (40, 40, 46), "stitch": (150, 150, 160)}
SHINY = {"white": (60, 60, 70), "white_dark": (30, 30, 36), "yellow": (120, 200, 250), "yellow_dark": (60, 130, 200),
         "red": (40, 60, 180)}


def P(v):
    return pal(BASE, SHINY, v)


SUIT = fabric(P, "white", "white_dark", axis="y", period=3.4, seam="stitch")
STEEL = metal(P, "steel", dark="steel_dark")


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            if abs(b - 58.2 + 0.2 * abs(a - sx * 1.4)) < 0.2 and abs(a - sx * 1.4) < 1.0:
                return p["black"], None                          # half-closed eyes
        if abs(b - 56.0 - 0.15 * a * a) < 0.2 and abs(a) < 1.2:
            return p["black"], None
        if abs(a) < 0.5 and 55.0 < b < 55.8:
            return p["white"], None
    return SUIT(x, y, z, face, variant, box=box, **k)


def glovef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    a, b = plane(x, y, z, face)
    if (b % 3.0) < 0.9:
        return tone(p["red"], face), None
    return fur(P, "yellow", "yellow_dark", length=1.0)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("betsumon")
    mats = {"skin": SUIT, "hand": glovef, "finger": glovef, "claw": STEEL, "foot": SUIT, "talon": STEEL}
    a = humanoid(m, mats, bulk=1.05, arm_bulk=1.0, leg_bulk=1.1, claws=True, talons=True, name="betsumon",
                 hand_pose="open")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 3.4, 3.2, 53.6, 61.4, facef, cut=1)
    for sx in (-1, 1):                                           # big ears
        ear = m.bone("ear_left" if sx > 0 else "ear_right", hd, (sx * 2.4, 61.0, 0))
        m.box(ear, min(sx * 1.6, sx * 6.0), 60.0, -0.4, max(sx * 1.6, sx * 6.0), 67.0, -0.4,
              lambda x, y, z, face, variant=None, box=None, **k: (P(variant)["pink"] if face in ("north",)
                                                                  else P(variant)["white"], None),
              rotation=(0, 0, -sx * 15), pivot=(sx * 2.4, 61.0, 0))
        spike(m, ear, (sx * 5.0, 66.6, -0.4), (sx * 0.4, 1, 0), 1.4, 2.0, solid(P, "violet"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):          # huge paw-gloves
        h = a[nm]["hand"]
        ball(m, a[nm]["bone"], (h[0], h[1], h[2]), 4.0, glovef, layers=4)
        for f in range(4):
            spike(m, a[nm]["bone"], (h[0] + (f - 1.5) * 1.6, h[1] + 3.0, h[2] - 3.0), (0, 0.6, -1), 1.0, 2.4, STEEL)
    tl = m.bone("tail", bd, (0, 31, 3))
    pts = [(0, 31, 3), (5, 28, 9), (11, 30, 12), (16, 34, 12)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 2, SUIT, extend=0.3)
    rod(m, tl, (14.0, 33.0, 12.0), (15.0, 34.0, 12.0), 4, STEEL, extend=0)
    for j in range(3):
        spike(m, tl, pts[-1], (1, (j - 1) * 0.6, 0), 1.2, 3.0, solid(P, "violet"))
    return m
