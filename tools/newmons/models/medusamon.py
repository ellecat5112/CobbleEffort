"""Medusamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the gorgon queen: a tall figure in a long red-and-black gown with a gold lattice bodice, a dark masked
face with a crown of golden horns and a single eye, red serpent locks with claw hands, a pink serpent tail, and two
huge muscular blue serpents arching over her shoulders, each splitting into fanged blue snake heads with gold crowns.
35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage. Built fully gowned as drawn.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, fabric, metal, scales, skin, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 4}
LOOK = "a tall gorgon queen in a long red-and-black gown with a gold lattice bodice, golden horns and two huge blue serpents arching over her"
BASE = {"red": (190, 30, 50), "red_dark": (100, 10, 24), "black": (34, 30, 40), "black_dark": (10, 8, 14), "gold": (240, 200, 70),
        "gold_dark": (160, 120, 20), "blue": (40, 70, 170), "blue_dark": (14, 26, 90), "blue_light": (110, 140, 230),
        "pink": (230, 60, 110), "pink_dark": (140, 20, 60), "eye": (250, 220, 60), "mouth": (200, 40, 70), "tooth": (250, 248, 236)}
SHINY = {"blue": (40, 140, 80), "blue_dark": (10, 70, 30), "blue_light": (120, 210, 150), "red": (60, 50, 140), "red_dark": (24, 14, 70)}


def P(v):
    return pal(BASE, SHINY, v)


GOWN = fabric(P, "red", "red_dark", seam="gold")
SNAKE = scales(P, "blue", "blue_dark", size=1.6, light="blue_light")


def bodicef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and ((x + y) % 2.0 < 0.3 or (x - y) % 2.0 < 0.3):
        return tone(p["gold"], face), None
    return fabric(P, "red", "red_dark")(x, y, z, face, variant, box=box, **k)


def snake_head(m, bone, c, sx):
    x, y, z = c
    m.round_box(bone, x, z - 1.0, 2.4, 3.4, y - 1.6, y + 1.8, SNAKE, cut=1)
    m.round_box(bone, x, z - 3.6, 2.0, 0.8, y - 2.4, y - 1.2, solid(P, "mouth"), cut=0)
    for j in range(2):
        spike(m, bone, (x + (j - 0.5) * 1.6, y - 1.4, z - 4.0), (0, -1, 0), 0.8, 1.6, solid(P, "tooth"), tip=0.8)
    for j in range(3):
        spike(m, bone, (x + (j - 1) * 1.0, y + 1.6, z), (0, 1, 0.2), 0.8, 1.4, solid(P, "gold"), tip=0.8)


def build():
    m = Model("medusamon")
    mats = {"skin": fabric(P, "black", "black_dark"), "chest": bodicef, "abs": bodicef, "pelvis": GOWN,
            "neck": fabric(P, "black", "black_dark"), "deltoid": GOWN, "upper_arm": GOWN, "forearm": GOWN,
            "hand": skin(P, "red", dark="red_dark"), "finger": skin(P, "red", dark="red_dark"), "thigh": GOWN, "knee": GOWN,
            "shin": GOWN, "calf": GOWN, "foot": metal(P, "gold", dark="gold_dark"), "toe": metal(P, "gold", dark="gold_dark")}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.95, name="medusamon")
    bd = a["body"]
    for j in range(6):                                                               # long gown
        r = 4.6 + j * 1.0
        m.round_box(bd, 0, 0.6, r, r * 0.8, 33.0 - (j + 1) * 5.6, 33.4 - j * 5.6, GOWN, cut=max(1, int(r * 0.3)))
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 60.0, armour(P, "black", "black_dark", trim="gold", trim_w=0.2), cut=1)
    m.box(hd, -0.8, 57.4, -2.9, 0.8, 58.4, -2.8, solid(P, "eye", glow=True))
    for sx in (-1, 1):                                                               # golden horn crown
        rod(m, hd, (sx * 1.4, 59.4, -0.6), (sx * 2.6, 68.0, -1.0), 1, metal(P, "gold", dark="gold_dark"), extend=0, t2=2)
    for i in range(6):                                                               # red serpent locks
        ang = math.radians(-60 + i * 24)
        rod(m, hd, (2.0 * math.sin(ang), 59.0, 1.0), (5.0 * math.sin(ang), 64.0, 3.0), 1, scales(P, "red", "red_dark"),
            extend=0.2, t2=1)
    tb = m.bone("tail", bd, (0, 10, 4))                                              # pink serpent tail
    pts = [(0, 10.0, 4.0), (4.0, 4.0, 12.0), (10.0, 2.0, 16.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 2, scales(P, "pink", "pink_dark"), extend=0.4)
    for sx in (-1, 1):                                                               # two huge arching serpents
        sb = m.bone("serpent_left" if sx > 0 else "serpent_right", bd, (sx * 6.0, 50.0, 2.0))
        pts = [(sx * 6.0, 50.0, 2.0), (sx * 14.0, 62.0, 2.0), (sx * 22.0, 56.0, 0.0), (sx * 24.0, 40.0, -2.0),
               (sx * 22.0, 26.0, -4.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, sb, p0, p1, 4, SNAKE, extend=1.0)
        e = pts[-1]
        for j in range(3):
            snake_head(m, sb, (e[0] + sx * (j - 1) * 4.0, e[1] - j * 3.0, e[2] - 3.0), sx)
    return m
