"""Sekkamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the snow-fox archer: a tall lavender fox-man with a huge white fur collar and a great plumed tail, a
long navy happi coat edged red with a white snowflake crest and a red sash, black leggings, furry clawed feet, an ice
quiver and a long crystal ice bow. 25 blocks.

Front is -z, y is up. 66 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import fabric, fur, gem, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a tall lavender snow-fox archer with a huge white fur collar, a navy snowflake happi coat, a plumed tail and a crystal ice bow"
BASE = {"lav": (190, 180, 240), "lav_dark": (130, 120, 200), "white": (248, 248, 252), "white_dark": (200, 204, 220),
        "navy": (40, 50, 110), "navy_dark": (14, 18, 60), "red": (200, 30, 40), "black": (30, 28, 34),
        "ice": (150, 220, 250), "eye": (220, 60, 90)}
SHINY = {"lav": (240, 200, 140), "lav_dark": (190, 140, 80), "navy": (120, 30, 40), "navy_dark": (60, 10, 14)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "lav", "lav_dark", length=1.4)


def coatf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "south" and abs(x) < 6.0 and 18.0 < y < 30.0:
        a = math.atan2(y - 24.0, x) * 3
        if math.hypot(x, y - 24.0) < 5.0 and abs(math.sin(a)) < 0.25:
            return tone(p["white"], face), None
    return fabric(P, "navy", "navy_dark", axis="y", period=3.0)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("sekkamon")
    mats = {"skin": coatf, "neck": FUR, "hand": FUR, "finger": FUR, "thigh": fabric(P, "black", "black", axis="y"),
            "shin": fabric(P, "black", "black", axis="y"), "foot": FUR, "talon": solid(P, "white")}
    a = humanoid(m, mats, bulk=0.9, arm_bulk=0.9, leg_bulk=0.9, talons=True, digitigrade=True, name="sekkamon")
    bd = a["body"]
    cape(m, bd, 52.0, 16.0, 40.0, coatf, z=4.0, flare=1.8, panels=6, seed=5)
    m.round_box(bd, 0, 0, 5.2, 4.0, 31.0, 33.0, solid(P, "red"), cut=1)                    # red sash
    m.round_box(bd, 0, 0.6, 8.0, 6.0, 47.0, 55.0, fur(P, "white", "white_dark", length=1.8), cut=3)   # fur collar
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 2.6, 3.4, 54.0, 60.0, FUR, cut=1)
    m.round_box(hd, 0, -4.4, 1.4, 1.6, 54.4, 57.0, FUR, cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.0), 57.6, -4.5, max(sx * 0.8, sx * 2.0), 58.2, -4.3, solid(P, "eye"))
        spike(m, hd, (sx * 1.8, 60.0, 0), (sx * 0.3, 1, 0.2), 1.8, 7.0, FUR, tip=0.8)       # tall ears
    tl = m.bone("tail", bd, (0, 32, 4))                                                  # great plumed tail
    pts = [(0, 32.0, 4.0), (-6.0, 24.0, 12.0), (-14.0, 26.0, 16.0), (-18.0, 34.0, 16.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 5 + (1 if i == 1 else 0), fur(P, "lav", "white", length=1.6), extend=0.8)
    w = a["arm_left"]["wrist"]                                                           # crystal ice bow
    bow = [(w[0] + 1.0, w[1] + 22.0, w[2] - 2.0), (w[0] + 3.0, w[1] + 10.0, w[2] - 5.0), (w[0] + 2.0, w[1], w[2] - 2.0),
           (w[0] + 3.0, w[1] - 10.0, w[2] - 5.0), (w[0] + 1.0, w[1] - 22.0, w[2] - 2.0)]
    for p0, p1 in zip(bow, bow[1:]):
        rod(m, a["arm_left"]["bone"], p0, p1, 1, gem(P, "ice", "white"), extend=0.3, t2=2)
    rod(m, a["arm_left"]["bone"], bow[0], bow[-1], 1, solid(P, "white"), extend=0.0, t2=1)
    m.box(bd, 2.0, 40.0, 4.0, 5.0, 54.0, 7.0, gem(P, "ice", "white", glow=False))           # ice quiver
    return m
