"""Turuiemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a lilac rabbit kung-fu fighter: long drooping ears with ragged white tips, a small horn, a blue
scarf knotted at the neck, baggy yellow overalls, black slippers, a red gauntlet on each forearm and two curved
white sickle-blades on its arms. 15 blocks.

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fabric, fur, leather, metal, plane, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a lilac rabbit kung-fu fighter with long drooping ears, a blue scarf, baggy yellow overalls, red gauntlets and curved sickle blades"
BASE = {"lilac": (210, 170, 220), "lilac_dark": (150, 110, 170), "white": (250, 250, 252), "yellow": (240, 200, 60),
        "yellow_dark": (180, 140, 20), "blue": (60, 90, 190), "black": (30, 30, 34), "red": (200, 50, 40),
        "red_dark": (120, 20, 14), "steel": (230, 232, 240), "steel_dark": (140, 144, 156), "eye": (40, 30, 30)}
SHINY = {"lilac": (240, 200, 160), "lilac_dark": (190, 140, 100)}


def P(v):
    return pal(BASE, SHINY, v)


LILAC = fur(P, "lilac", "lilac_dark", length=0.8)
OVERALL = fabric(P, "yellow", "yellow_dark")


def earf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if y < 44.0:
        return tone(p["white"], face), None
    return LILAC(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            if abs(b - 58.0) < 0.4 and abs(a - sx * 1.4) < 0.7:
                return p["eye"], None
    return LILAC(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("turuiemon")
    mats = {"skin": LILAC, "chest": OVERALL, "abs": OVERALL, "pelvis": OVERALL, "deltoid": LILAC, "upper_arm": LILAC,
            "forearm": leather(P, "red", "red_dark"), "hand": LILAC, "thigh": OVERALL, "knee": OVERALL,
            "shin": OVERALL, "calf": OVERALL, "foot": leather(P, "black", "black"), "neck": LILAC}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=0.95, leg_bulk=1.1, name="turuiemon")
    bd = a["body"]
    for nm in ("leg_left", "leg_right"):                                               # baggy legs
        k = a[nm]["knee"]
        m.round_box(a[nm]["bone"], k[0], k[2], 3.0, 3.0, 8.0, 20.0, OVERALL, cut=1)
    m.round_box(bd, 0, 0, 3.6, 3.6, 51.0, 53.4, solid(P, "blue"), cut=1)                 # scarf
    m.box(bd, 2.0, 44.0, -4.2, 4.0, 52.0, -3.6, solid(P, "blue"), rotation=(0, 0, -15), pivot=(3.0, 52.0, -3.9))
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 3.0, 3.0, 53.4, 61.0, headf, cut=1)
    spike(m, hd, (0, 60.6, -1.4), (0, 1, -0.3), 1.0, 2.4, solid(P, "white"), tip=0.8)
    for sx in (-1, 1):                                                                 # drooping ears
        pts = [(sx * 2.0, 60.0, 0.6), (sx * 6.0, 62.0, 1.0), (sx * 9.0, 56.0, 1.4), (sx * 10.0, 46.0, 1.0),
               (sx * 9.6, 40.0, 0.6)]
        for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 1, earf, extend=0.5, t2=4)
    for nm in ("arm_left", "arm_right"):                                               # sickle blades
        w = a[nm]["wrist"]
        ab = a[nm]["bone"]
        sx = 1 if nm == "arm_left" else -1
        pts = [(w[0], w[1] + 4.0, w[2]), (w[0] + sx * 2.0, w[1] - 2.0, w[2] - 1.0), (w[0] + sx * 1.0, w[1] - 8.0, w[2] - 3.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 1, metal(P, "steel", dark="steel_dark"), extend=0.3, t2=2)
    return m
