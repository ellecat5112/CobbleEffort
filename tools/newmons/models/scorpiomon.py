"""Scorpiomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a skeletal scorpion of bleached bone: a ribbed bone carapace and segmented legs patched with dark
markings, a long jointed bone tail arching overhead to a hooked stinger blade, a fanged skull of a head with red mandible
sickles, and two great bone pincers lined with red spines. 25 blocks.

Front is -z, y is up. 44 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(25, HEIGHT, 7.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 5}
LOOK = "a skeletal bone scorpion with a ribbed carapace, a jointed bone tail arching to a hooked stinger and great red-spined pincers"
BASE = {"bone": (232, 226, 196), "bone_dark": (160, 150, 110), "mark": (70, 70, 74), "red": (200, 50, 50),
        "red_dark": (120, 20, 20), "steel": (200, 204, 216), "steel_dark": (110, 114, 130), "eye": (250, 200, 40)}
SHINY = {"bone": (60, 60, 70), "bone_dark": (24, 24, 30), "mark": (230, 230, 236)}


def P(v):
    return pal(BASE, SHINY, v)


def bonef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("up", "east", "west") and abs(math.sin(x * 1.1 + z * 0.9)) > 0.94:
        return tone(p["mark"], face), None
    return armour(P, "bone", "bone_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("scorpiomon")
    top = m.bone("scorpiomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    for i in range(6):                                                                   # ribbed carapace
        r = 6.0 - abs(i - 2) * 0.6
        m.round_box(bd, 0, -8.0 + i * 3.0, r, 1.4, 10.0, 16.0, bonef, cut=1)
    hd = m.bone("head", bd, (0, 14, -10))
    m.round_box(hd, 0, -12.0, 3.4, 3.0, 11.0, 17.0, bonef, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.2, sx * 2.4), 15.0, -15.1, max(sx * 1.2, sx * 2.4), 15.8, -14.9, solid(P, "eye", glow=True))
        pts = [(sx * 2.0, 12.0, -14.0), (sx * 4.0, 8.0, -18.0), (sx * 2.0, 5.0, -20.0)]
        for p0, p1 in zip(pts, pts[1:]):                                                  # red mandible sickles
            rod(m, hd, p0, p1, 1, armour(P, "red", "red_dark"), extend=0.2, t2=2)
    for j in range(4):
        spike(m, hd, (-1.5 + j, 11.0, -14.8), (0, -1, -0.2), 0.8, 1.6, solid(P, "bone"), tip=0.8)
    tl = m.bone("tail", bd, (0, 14, 8))                                                  # arching bone tail
    pts = [(0, 14.0, 8.0), (0, 22.0, 14.0), (0, 32.0, 14.0), (0, 40.0, 8.0), (0, 42.0, 0.0), (0, 38.0, -6.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, max(2, 4 - i // 2), bonef, extend=0.6)
        m.round_box(tl, p1[0], p1[2], 2.6, 2.6, p1[1] - 0.6, p1[1] + 0.6, solid(P, "bone_dark"), cut=1)
    m.box(tl, -0.6, 32.0, -12.0, 0.6, 40.0, -4.0, metal(P, "steel", dark="steel_dark"), rotation=(30, 0, 0),
          pivot=(0, 38.0, -6.0))                                                          # stinger blade
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                  # great pincers
        ab = m.bone(nm, bd, (sx * 5.0, 14.0, -8.0))
        rod(m, ab, (sx * 5.0, 14.0, -8.0), (sx * 12.0, 18.0, -14.0), 3, bonef, extend=0.6)
        rod(m, ab, (sx * 12.0, 18.0, -14.0), (sx * 10.0, 22.0, -22.0), 3, bonef, extend=0.6)
        for d in (-1, 1):
            spike(m, ab, (sx * 10.0 + d * 1.6, 22.0, -22.0), (d * 0.3, 0.5, -1), 1.6, 6.0, bonef, tip=0.8)
        for j in range(3):
            spike(m, ab, (sx * 11.0, 19.0 + j * 1.2, -16.0 - j * 2.0), (-sx * 1, 0, 0), 0.8, 2.0, solid(P, "red"), tip=0.8)
    for sx in (-1, 1):                                                                   # segmented legs
        for j, zz in enumerate((-4.0, 0.0, 4.0)):
            nm = f"leg_{('front', 'mid', 'back')[j]}_{'left' if sx > 0 else 'right'}"
            lg = m.bone(nm, top, (sx * 5.0, 12.0, zz))
            rod(m, lg, (sx * 5.0, 12.0, zz), (sx * 11.0, 14.0, zz + 1.0), 2, bonef, extend=0.4)
            rod(m, lg, (sx * 11.0, 14.0, zz + 1.0), (sx * 14.0, 0.6, zz + 2.0), 1, bonef, extend=0.4)
    return m
