"""Voltobautamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a skeletal demon pirate captain: a black tricorn hat over a grinning skull face with
a red scarf, a gold-buttoned black coat, baggy blue pantaloons, a ragged peg-leg trailing black smoke, huge tattered
red-and-black bat wings, a whip of a barbed tail, and long thin mechanical arms reaching high with clawed hands, one
holding a golden pistol. 35 blocks.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, bat_wing
from _digibody import humanoid
from _digidetail import fabric, leather, metal, plane, skin, solid
from _route import pal, tone

HEIGHT = 74
SCALE, HITBOX = sized(35, HEIGHT, 8.0)
KIND = "floater"
K = 3
LOOK = "a skeletal demon pirate with a tricorn hat, a skull face, a black coat, blue pantaloons, red bat wings and long clawed mechanical arms"
BASE = {"black": (34, 32, 38), "black_dark": (12, 12, 14), "bone": (230, 222, 200), "bone_dark": (160, 150, 120),
        "red": (180, 30, 40), "red_dark": (100, 10, 16), "blue": (50, 70, 170), "blue_dark": (20, 30, 100),
        "gold": (240, 196, 60), "gold_dark": (170, 120, 20), "smoke": (60, 56, 66, 170), "eye": (255, 60, 50),
        "membrane": (150, 24, 34, 230), "steel": (160, 164, 176)}
SHINY = {"red": (60, 130, 180), "red_dark": (20, 70, 110), "membrane": (40, 100, 150, 230), "blue": (140, 60, 40),
         "blue_dark": (80, 24, 10)}


def P(v):
    return pal(BASE, SHINY, v)


COAT = fabric(P, "black", "black_dark")
BONE = skin(P, "bone", dark="bone_dark")


def skullf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            if math.hypot(a - sx * 1.2, b - 58.4) < 0.7:
                return p["eye"], p["eye"]
        if 55.0 < b < 56.2 and abs(a) < 1.8 and (a * 2.0) % 1.0 < 0.5:
            return p["black"], None
    return BONE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("voltobautamon")
    mats = {"skin": COAT, "chest": COAT, "abs": COAT, "pelvis": fabric(P, "blue", "blue_dark"), "deltoid": COAT,
            "upper_arm": COAT, "forearm": COAT, "hand": BONE, "finger": BONE, "claw": metal(P, "steel"),
            "thigh": fabric(P, "blue", "blue_dark"), "knee": fabric(P, "blue", "blue_dark"),
            "shin": leather(P, "black", "black_dark"), "calf": leather(P, "black", "black_dark"),
            "foot": leather(P, "black", "black_dark"), "neck": BONE}
    a = humanoid(m, mats, bulk=0.9, arm_bulk=0.85, leg_bulk=1.0, claws=True, name="voltobautamon")
    bd = a["body"]
    for nm in ("leg_left", "leg_right"):                                               # baggy pantaloons
        k = a[nm]["knee"]
        m.round_box(a[nm]["bone"], k[0], k[2], 3.0, 3.0, 12.0, 26.0, fabric(P, "blue", "blue_dark"), cut=1)
    for j in range(4):
        ball(m, bd, (0.6 * j - 1.0, 4.0 - j * 1.2, 0), 2.0 - j * 0.3, solid(P, "smoke"), layers=1)
    for j in range(5):
        ball(m, bd, (-1.6, 48.0 - j * 3.0, -3.8), 0.6, metal(P, "gold"), layers=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.8, 3.0, 54.0, 61.0, skullf, cut=1)
    m.round_box(hd, 0, 0, 5.0, 4.0, 61.0, 62.4, leather(P, "black", "black_dark"), cut=2)   # tricorn
    m.round_box(hd, 0, 0, 3.2, 3.0, 62.4, 65.0, leather(P, "black", "black_dark"), cut=1)
    m.round_box(hd, 0, 0, 3.0, 3.2, 52.6, 54.4, solid(P, "red"), cut=1)                   # scarf
    m.box(hd, 2.0, 48.0, 2.0, 4.0, 54.0, 3.0, solid(P, "red"), rotation=(0, 0, -12), pivot=(3.0, 54.0, 2.5))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                # long mechanical arms
        sh = a[nm]["shoulder"]
        ab = a[nm]["bone"]
        pts = [sh, (sh[0] + sx * 6.0, sh[1] + 10.0, sh[2] - 2.0), (sh[0] + sx * 8.0, sh[1] + 22.0, sh[2] - 3.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 1, metal(P, "steel"), extend=0.3)
        tip = pts[-1]
        for f in range(3):
            spike(m, ab, tip, ((f - 1) * 0.5, 1, -0.3), 0.8, 3.0, metal(P, "steel"), tip=0.8)
        if sx < 0:
            m.box(ab, tip[0] - 0.6, tip[1] - 1.0, tip[2] - 4.0, tip[0] + 0.6, tip[1] + 0.6, tip[2], metal(P, "gold"))
    for sx in (-1, 1):
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 3.0, 48.0, 4.0))
        bat_wing(m, wb, (sx * 3.0, 48.0, 4.0), 26.0, 28.0, 4, solid(P, "black"), solid(P, "membrane"), side=sx,
                 sweep=-15)
    tl = m.bone("tail", bd, (0, 30, 4))
    pts = [(0, 30.0, 4.0), (6.0, 24.0, 10.0), (14.0, 28.0, 12.0), (18.0, 38.0, 10.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, solid(P, "black"), extend=0.3)
    spike(m, tl, pts[-1], (0.2, 1, -0.3), 1.6, 4.0, metal(P, "gold"), tip=0.8)
    return m
