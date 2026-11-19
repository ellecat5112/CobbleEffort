"""Strikedramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a punk dragon-man: a lean lilac dragon with a long silver armoured snout-helm and red mane, a
studded silver chest harness with a red flame mark, green cargo trousers with a belt, studded steel bands, silver claws
on its hands and feet, and a long lilac tail. 15 blocks.

Front is -z, y is up. 62 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, fabric, leather, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 62
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a lean lilac dragon-man with a long silver snout-helm, a red mane, a studded chest harness, green cargo trousers and silver claws"
BASE = {"lilac": (150, 130, 200), "lilac_dark": (80, 60, 140), "silver": (210, 214, 226), "silver_dark": (110, 114, 130),
        "red": (200, 40, 40), "green": (90, 120, 60), "green_dark": (40, 60, 24), "brown": (110, 70, 40),
        "black": (30, 28, 32), "eye": (250, 200, 40), "white": (246, 246, 246)}
SHINY = {"lilac": (60, 130, 190), "lilac_dark": (20, 70, 130)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "lilac", dark="lilac_dark")
STEEL = metal(P, "silver", dark="silver_dark")


def chestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and math.hypot(x, y - 46.0) < 2.2 and abs(math.sin(math.atan2(y - 46.0, x) * 3)) > 0.5:
        return tone(p["red"], face), None
    return tone(p["white"], face), None


def build():
    m = Model("strikedramon")
    mats = {"skin": SKIN, "chest": chestf, "pelvis": fabric(P, "green", "green_dark", axis="y"),
            "thigh": fabric(P, "green", "green_dark", axis="y"), "knee": fabric(P, "green", "green_dark"),
            "claw": STEEL, "talon": STEEL}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.9, claws=True, talons=True, digitigrade=True,
                 name="strikedramon")
    bd = a["body"]
    m.round_box(bd, 0, 0, 5.0, 3.8, 31.0, 33.0, leather(P, "brown", "black"), cut=1)
    for sx in (-1, 1):
        m.round_box(bd, sx * 7.4, 0, 3.0, 3.2, 46.0, 51.0, armour(P, "silver", "silver_dark"), cut=1)
        for j in range(3):
            spike(m, bd, (sx * 8.6, 50.0, -1.0 + j), (sx * 0.6, 1, 0), 0.8, 2.0, STEEL, tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.4, 2.6, 3.6, 54.0, 60.0, armour(P, "silver", "silver_dark"), cut=1)
    m.round_box(hd, 0, -6.0, 1.6, 2.4, 54.0, 57.6, armour(P, "silver", "silver_dark"), cut=0)   # long snout-helm
    spike(m, hd, (0, 59.0, -3.0), (0, 0.6, 1), 1.4, 8.0, STEEL, tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.5, sx * 2.7), 57.6, -3.4, max(sx * 2.5, sx * 2.7), 58.4, -2.0, solid(P, "eye", glow=True))
    for j in range(5):
        spike(m, hd, ((j - 2) * 1.0, 58.0, 2.0), ((j - 2) * 0.2, 0.2, 1), 1.2, 5.0, strands(P, "red", "red"), tip=0.8)
    for side in ("arm_left", "arm_right", "leg_left", "leg_right"):                      # studded steel bands
        p0 = a[side]["wrist" if side.startswith("arm") else "knee"]
        m.round_box(a[side]["bone"], p0[0], p0[2], 2.0, 2.0, p0[1] + 0.4, p0[1] + 2.0, STEEL, cut=0)
    tl = m.bone("tail", bd, (0, 32, 3))
    pts = [(0, 32.0, 3.0), (3.0, 22.0, 10.0), (6.0, 14.0, 16.0), (8.0, 10.0, 22.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 3 - i, SKIN, extend=0.4)
    return m
