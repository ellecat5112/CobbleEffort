"""Targetmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a wiry pink puppet brawler: a bald pink head with a flame for a top-knot, a red-and-white visor
over its eyes and a huge toothy grin, a black shaggy vest, an ammo belt, black wrapped forearms and shins, a long thin
tail, and two giant red sneakers worn on its raised fists with a crackle of electricity between them. 15 blocks.

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import fabric, fur, leather, plane, skin, solid
from _route import pal, tone

HEIGHT = 68
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a wiry pink puppet brawler with a flame top-knot, a red visor, a toothy grin, an ammo belt and giant red sneakers on its fists"
BASE = {"pink": (246, 170, 190), "pink_dark": (200, 110, 140), "black": (34, 32, 36), "black_dark": (12, 12, 14),
        "red": (220, 50, 40), "red_dark": (140, 20, 14), "white": (250, 250, 250), "navy": (40, 50, 110),
        "orange": (250, 150, 40), "flame": (255, 200, 60), "brass": (220, 170, 70), "bolt": (255, 250, 120),
        "tooth": (255, 255, 250), "mouth": (90, 20, 30), "sole": (240, 230, 210)}
SHINY = {"pink": (150, 200, 240), "pink_dark": (80, 130, 190), "red": (60, 170, 80), "red_dark": (20, 100, 40)}


def P(v):
    return pal(BASE, SHINY, v)


PINK = skin(P, "pink", dark="pink_dark")
WRAP = fabric(P, "black", "black_dark", axis="x", period=1.4)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        if 58.0 < b < 59.8:
            return (p["white"] if abs(a) < 0.8 else p["red"]), None
        if 54.6 < b < 57.0 and abs(a) < 2.6:
            if abs(b - 55.8) < 0.25:
                return p["mouth"], None
            return (p["tooth"] if (a * 2.0) % 1.0 > 0.15 else p["mouth"]), None
    return PINK(x, y, z, face, variant, box=box, **k)


def shoef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if box is None:
        return tone(p["red"], face), None
    t = (y - box.lo[1]) / max(box.size[1], 1e-6)
    if t < 0.2:
        return tone(p["sole"], face), None
    if face in ("east", "west") and abs(t - 0.5) < 0.08:
        return tone(p["navy"], face), None
    if face == "up" and int((z - box.lo[2]) * 1.2) % 2 == 0:
        return tone(p["white"], face), None
    return tone(p["red"] if t < 0.8 else p["orange"], face), None


def build():
    m = Model("targetmon")
    mats = {"skin": PINK, "chest": fur(P, "black", "black_dark"), "abs": PINK, "pelvis": fur(P, "black", "black_dark"),
            "deltoid": PINK, "upper_arm": PINK, "forearm": WRAP, "hand": PINK, "thigh": PINK, "knee": PINK,
            "shin": WRAP, "calf": WRAP, "foot": leather(P, "black", "black_dark"), "neck": PINK}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=0.9, leg_bulk=0.9, name="targetmon")
    bd = a["body"]
    m.round_box(bd, 0, 0, 5.4, 4.0, 30.0, 32.4, leather(P, "black", "black_dark"), cut=1)
    for j in range(10):                                                                 # ammo belt
        t = j / 9
        x = -5.0 + t * 10.0
        y = 50.0 - t * 16.0
        m.box(bd, x - 0.5, y - 1.2, -4.6, x + 0.5, y + 1.2, -3.8, solid(P, "brass"))
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 3.4, 3.4, 53.0, 62.0, headf, cut=2)
    for j in range(4):                                                                  # flame top-knot
        spike(m, hd, ((j - 1.5) * 0.8, 61.6, 0), ((j - 1.5) * 0.2, 1, 0.2), 1.4, 6.0 - abs(j - 1.5),
              solid(P, "flame", glow=True), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                 # giant sneaker fists
        h = a[nm]["hand"]
        ab = a[nm]["bone"]
        m.box(ab, h[0] - 3.2, h[1] - 2.0, h[2] - 9.0, h[0] + 3.2, h[1] + 4.0, h[2] + 4.0, shoef,
              rotation=(50, 0, 0), pivot=(h[0], h[1], h[2]))
    bl = m.bone("bolt", bd, (0, 66, -2))                                                # crackle between the shoes
    for j in range(8):
        x = -10.0 + j * 2.8
        y = 66.0 + (1.0 if j % 2 else -1.0)
        m.box(bl, x - 1.6, y - 0.4, -2.4, x + 1.6, y + 0.4, -1.6, solid(P, "bolt", glow=True), rotation=(0, 0, 30 if j % 2 else -30),
              pivot=(x, y, -2.0))
    tl = m.bone("tail", bd, (0, 30, 4))
    pts = [(0, 30.0, 4.0), (2.0, 20.0, 9.0), (6.0, 12.0, 10.0), (10.0, 10.0, 8.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, solid(P, "black"), extend=0.4)
    return m
