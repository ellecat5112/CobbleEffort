"""Sepikmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Armor Digimon of kindness: a tawny monkey-like spirit dancer hidden behind a great painted
oval mask-shield of red, blue and green, a crown of red-and-yellow feathers, a green grass ruff, bandaged limbs, and a
huge painted boomerang. 15 blocks.

Front is -z, y is up. 50 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fabric, fur, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a tawny monkey spirit dancer behind a great painted red-blue-green mask-shield, a feather crown, a grass ruff and a painted boomerang"
BASE = {"tan": (190, 140, 80), "tan_dark": (120, 80, 40), "red": (210, 40, 40), "blue": (40, 90, 200),
        "green": (60, 160, 80), "yellow": (250, 210, 60), "cream": (246, 236, 210), "grass": (100, 150, 50),
        "gold": (230, 190, 70), "black": (30, 26, 24), "bandage": (240, 230, 210)}
SHINY = {"tan": (150, 150, 170), "tan_dark": (90, 90, 110)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "tan", "tan_dark", length=1.2)


def maskf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        dx, dy = x / 6.0, (y - 52.0) / 8.0
        r = math.hypot(dx, dy)
        if r > 0.9:
            return tone(p["gold"], face), None
        if abs(dx) < 0.12:
            return tone(p["black"], face), None
        if r < 0.35 and abs(dy + 0.1) < 0.2:
            return tone(p["green"], face), None
        return tone(p["red"] if dx < 0 else p["blue"], face), None
    return tone(p["black"], face), None


def boomf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "south") and int((x + y) * 1.2) % 4 == 0:
        return tone(p["blue"], face), None
    return tone(p["cream"] if (abs(x) % 10.0) > 1.0 else p["red"], face), None


def build():
    m = Model("sepikmon")
    mats = {"skin": FUR, "forearm": fabric(P, "bandage", "tan", axis="y", period=1.2),
            "shin": fabric(P, "bandage", "tan", axis="y", period=1.2), "talon": solid(P, "black")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.8, leg_bulk=0.85, talons=True, digitigrade=True, name="sepikmon")
    bd = a["body"]
    for j in range(12):                                                                  # green grass ruff
        ang = 2 * math.pi * j / 12
        spike(m, bd, (4.0 * math.cos(ang), 46.0, 3.0 * math.sin(ang)), (math.cos(ang), -0.4, math.sin(ang)), 1.4, 4.0,
              solid(P, "grass"), tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.6, 54.0, 59.0, FUR, cut=1)
    m.round_box(hd, 0, -4.6, 6.0, 0.8, 44.0, 60.0, maskf, cut=0)                            # mask-shield
    for j in range(9):                                                                   # feather crown
        ang = math.radians(-60 + j * 15)
        spike(m, hd, (5.0 * math.sin(ang), 59.0, -3.0), (math.sin(ang), 1, 0.2), 1.4, 8.0,
              solid(P, "red" if j % 2 else "yellow"), tip=0.8)
    w = a["arm_right"]["wrist"]                                                          # painted boomerang
    ab = a["arm_right"]["bone"]
    m.box(ab, w[0] - 1.0, w[1] - 2.0, w[2] - 3.0, w[0] + 1.0, w[1] + 22.0, w[2] - 1.0, boomf,
          rotation=(0, 0, 20), pivot=(w[0], w[1], w[2] - 2.0))
    m.box(ab, w[0] - 18.0, w[1] - 2.0, w[2] - 3.0, w[0], w[1], w[2] - 1.0, boomf,
          rotation=(0, 0, 20), pivot=(w[0], w[1], w[2] - 2.0))
    tl = m.bone("tail", bd, (0, 32, 3))
    pts = [(0, 32.0, 3.0), (4.0, 22.0, 10.0), (10.0, 26.0, 14.0), (12.0, 32.0, 12.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, FUR, extend=0.2, t2=2)
    return m
