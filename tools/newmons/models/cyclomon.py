"""Cyclomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the one-eyed brute. A hulking hunched yellow dragon-man with a heavily muscled, scaly body, a dark
brown face with a single glaring eye under a long brown horn, a fanged red mouth, a steel helmet plate with a horn on
one side, a curved steel back spike, enormous arms ending in red-clawed hands, and thick clawed legs. 15 blocks tall.

Front is -z, y is up. 56 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import Bulge, metal, scales, skin, solid, torso_bulges
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a hulking hunched yellow dragon-man with a scaly muscled body, a single glaring eye under a long brown horn, "
        "a steel helmet plate, a curved back spike and enormous red-clawed hands")
BASE = {"yellow": (240, 200, 60), "yellow_dark": (180, 130, 20), "yellow_light": (255, 240, 150), "brown": (100, 70, 40),
        "brown_dark": (60, 40, 20), "steel": (200, 204, 216), "steel_dark": (100, 104, 116), "red": (200, 40, 40),
        "claw": (40, 36, 34), "mouth": (180, 30, 40), "tooth": (250, 250, 246), "eye": (250, 230, 120),
        "pupil": (30, 20, 50)}
SHINY = {"yellow": (120, 180, 230), "yellow_dark": (60, 110, 170), "yellow_light": (200, 230, 255)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "yellow", "yellow_dark", size=1.6, light="yellow_light", rim_mix=0.3)
MUSCLE = skin(P, "yellow", dark="yellow_dark", light="yellow_light", bulges=torso_bulges(0, 51.0, 6.6, abs_rows=4),
              var=0.04)
STEEL = metal(P, "steel", dark="steel_dark")


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        d = math.hypot(x, y - 51.4)
        if d < 1.4:
            return tone(p["pupil"] if d < 0.5 else p["eye"], face), (p["eye"] if d >= 0.5 else None)
    return skin(P, "brown", dark="brown_dark", var=0.04)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("cyclomon")
    mats = {"skin": HIDE, "chest": MUSCLE, "abs": MUSCLE, "hand": HIDE, "finger": HIDE, "claw": solid(P, "red"),
            "foot": HIDE, "talon": solid(P, "claw")}
    a = humanoid(m, mats, bulk=1.6, arm_bulk=1.8, leg_bulk=1.5, digitigrade=True, claws=True, talons=True,
                 name="cyclomon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 49, -4))                                       # head sunk low between the shoulders
    m.round_box(hd, -1.0, -5.0, 3.4, 3.6, 46.0, 54.0, facef, cut=1)
    m.box(hd, -3.4, 45.0, -10.0, 1.6, 48.4, -5.0, skin(P, "brown", dark="brown_dark"))     # snout
    m.box(hd, -3.0, 44.4, -9.4, 1.2, 45.6, -5.4, solid(P, "mouth"))
    for i in range(4):
        spike(m, hd, (-2.6 + i * 1.2, 45.0, -9.0), (0, -1, 0), 0.8, 1.6, solid(P, "tooth"))
    spike(m, hd, (0, 54.0, -5.0), (0.1, 1, -0.4), 2.0, 9.0, skin(P, "brown", dark="brown_dark"), tip=0.4)  # long horn
    m.round_box(hd, -4.4, -4.0, 2.4, 3.6, 47.0, 54.0, STEEL, cut=1)            # steel helmet plate
    spike(m, hd, (-6.4, 52.0, -4.0), (-1, 0.6, 0.2), 1.6, 4.0, STEEL, tip=0.3)
    pts = [(2.0, 52.0, 4.0), (2.4, 58.0, 8.0), (2.0, 63.0, 6.0)]               # curved back spike
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, bd, p0, p1, 3 - j, STEEL, extend=0.4)
    for nm in ("arm_left", "arm_right"):                                       # enormous red-clawed hands
        h = a[nm]["hand"]
        m.round_box(a[nm]["bone"], h[0], h[2], 4.0, 4.0, h[1] - 3.0, h[1] + 3.0, HIDE, cut=2)
        for f in range(4):
            spike(m, a[nm]["bone"], (h[0] + (f - 1.5) * 1.8, h[1] - 3.0, h[2] - 2.0), (0, -1, -0.5), 1.4, 5.0,
                  solid(P, "red"), tip=0.4)
    for nm in ("arm_left", "arm_right"):                                       # extra arm bulk (huge arms)
        ab = a[nm]
        rod(m, ab["bone"], ab["shoulder"], ab["elbow"], 6, HIDE, extend=0.6)
    tl = m.bone("tail", bd, (0, 31, 4))
    pts = [(0, 31.0, 4.0), (0, 24.0, 10.0), (2.0, 18.0, 14.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 4 - j, HIDE, extend=0.5)
    return m
