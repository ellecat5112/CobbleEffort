"""Nyabootmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the cat musketeer: a yellow cat with a violet eye-mask, tall ears and a curling tail, a black
plumed musketeer hat, a white ruffled shirt under a black doublet, a gold buckled belt, brown gauntlet gloves, big
cuffed brown boots with steel toes, a great black cape lined with green-to-blue, and a rapier blazing with green
flame. 35 blocks tall.

Front is -z, y is up. 60 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import cutout, fabric, flame_inside, fur, leather, local, metal, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a yellow cat musketeer with a violet eye-mask, a black plumed hat, a black doublet, cuffed brown boots, a great "
        "black cape and a rapier blazing with green flame")
BASE = {"yellow": (250, 210, 70), "yellow_dark": (200, 150, 20), "violet": (110, 60, 160), "black": (34, 32, 40),
        "black_dark": (12, 12, 16), "white": (244, 244, 240), "white_dark": (190, 190, 186), "gold": (230, 190, 70),
        "brown": (150, 90, 50), "brown_dark": (90, 50, 20), "steel": (200, 204, 216), "plume": (240, 190, 230),
        "green": (90, 220, 90, 200), "green_core": (220, 255, 180, 235), "blue": (50, 70, 170), "eye": (60, 190, 90)}
SHINY = {"yellow": (200, 200, 210), "yellow_dark": (130, 130, 146), "green": (100, 170, 255, 200),
         "green_core": (220, 240, 255, 235)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "yellow", "yellow_dark", length=1.0)
LEATHER = leather(P, "brown", "brown_dark", stitch="gold")


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["green_core"] if 0.3 < u / max(W, 1e-6) < 0.7 else p["green"]
    return c, c[:3]


def build():
    m = Model("nyabootmon")
    mats = {"skin": FUR, "chest": fabric(P, "black", "black_dark"), "abs": fabric(P, "white", "white_dark"),
            "pelvis": fabric(P, "black", "black_dark"), "deltoid": fabric(P, "white", "white_dark"),
            "upper_arm": fabric(P, "white", "white_dark"), "forearm": LEATHER, "hand": LEATHER, "finger": LEATHER,
            "thigh": fabric(P, "black", "black_dark"), "knee": LEATHER, "shin": LEATHER, "calf": LEATHER,
            "foot": metal(P, "steel"), "toe": metal(P, "steel")}
    a = humanoid(m, mats, bulk=0.9, arm_bulk=0.9, leg_bulk=1.0, name="nyabootmon")
    bd = a["body"]
    for nm in ("leg_left", "leg_right"):                                                 # big boot cuffs
        kn = a[nm]["knee"]
        m.round_box(a[nm]["bone"], kn[0], kn[2], 2.8, 2.8, kn[1] - 3.0, kn[1] + 1.0, LEATHER, cut=1)
    m.round_box(bd, 0, 0.4, 4.6, 3.6, 33.0, 35.0, leather(P, "black", "black"), cut=1)  # gold buckled belt
    m.box(bd, -1.2, 33.2, -4.0, 1.2, 34.8, -3.8, solid(P, "gold"))
    cape(m, bd, 52.0, 18.0, 44.0, fabric(P, "black", "blue"), z=4.0, flare=1.2, panels=7, seed=8)
    hd = m.bone("head", bd, (0, 55, 0))
    ball(m, hd, (0, 58.0, -0.2), 3.2, FUR, layers=4, ry=3.0)
    m.box(hd, -2.8, 58.0, -3.25, 2.8, 59.4, -3.05, solid(P, "violet"))                    # eye-mask
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 1.8), 58.4, -3.35, max(sx * 0.8, sx * 1.8), 59.0, -3.25, solid(P, "eye"))
        spike(m, hd, (sx * 2.0, 60.0, 0), (sx * 0.4, 1, 0), 1.6, 3.0, FUR, tip=0.8)        # tall ears
    m.round_box(hd, 0, 0.4, 5.0, 4.6, 61.0, 61.8, solid(P, "black"), cut=1)               # plumed musketeer hat
    m.round_box(hd, 0, 0.4, 3.0, 2.8, 61.8, 64.0, solid(P, "black"), cut=1)
    pts = [(2.0, 63.0, 0.0), (5.0, 66.0, 2.0), (7.0, 66.0, 5.0), (8.0, 63.0, 7.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, hd, p0, p1, 1, solid(P, "plume"), extend=0.2, t2=2)
    tb = m.bone("tail", bd, (0, 32, 3))                                                  # curling tail
    pts = [(0, 32.0, 3.0), (-3.0, 26.0, 8.0), (-6.0, 24.0, 11.0), (-7.0, 27.0, 13.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 1, FUR, extend=0.2, t2=1)
    ar = a["arm_right"]                                                                  # flaming rapier
    h = ar["hand"]
    m.round_box(ar["bone"], h[0], h[2] - 1.0, 1.4, 1.4, h[1] + 0.6, h[1] + 1.4, metal(P, "gold"), cut=0)
    rod(m, ar["bone"], (h[0], h[1] + 1.4, h[2] - 1.0), (h[0] + 4.0, h[1] + 20.0, h[2] - 6.0), 1,
        metal(P, "steel"), extend=0.1)
    for ang in (0, 90):
        m.box(ar["bone"], h[0] + 1.0, h[1] + 8.0, h[2] - 3.0, h[0] + 5.0, h[1] + 24.0, h[2] - 3.0,
              cutout(flame_inside(4, 0.2, 3), firef), rotation=(0, ang, 0), pivot=(h[0] + 3.0, h[1] + 8.0, h[2] - 3.0))
    return m
