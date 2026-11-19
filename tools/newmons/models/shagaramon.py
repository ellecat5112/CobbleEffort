"""Shagaramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the dragon king of the sea: a blue-and-white serpent-tailed dragon sovereign in a flowing golden
kimono-robe with wide sleeves and a red sash, a slender pale-blue dragon head crowned with golden antlers and a pearl,
pale blue mist trailing from her shoulders, clawed blue hands, little white fin-wings along her coiled tail, and a
great blue feathered tail fin. 35 blocks.

Front is -z, y is up. 60 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import fabric, feathers, gem, metal, scales, skin, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "floater"
K = 3
LOOK = "a serpent-tailed dragon sovereign in a flowing golden kimono-robe with a pale-blue dragon head, golden antlers and a feathered tail fin"
BASE = {"blue": (90, 130, 220), "blue_dark": (40, 60, 150), "white": (240, 244, 252), "white_dark": (180, 190, 220),
        "gold": (240, 210, 120), "gold_dark": (170, 130, 50), "red": (200, 30, 40), "mist": (180, 210, 250, 140),
        "pearl": (240, 250, 255), "teal": (60, 180, 220), "eye": (250, 220, 60)}
SHINY = {"blue": (200, 90, 150), "blue_dark": (130, 40, 90), "teal": (240, 120, 180)}


def P(v):
    return pal(BASE, SHINY, v)


ROBE = fabric(P, "gold", "gold_dark", axis="y", period=3.0)
HIDE = scales(P, "blue", "blue_dark", size=1.4)


def tailf(x, y, z, face, variant, box=None, **k):
    if face == "down" or abs(math.sin(z * 0.5)) > 0.7:
        return skin(P, "white", dark="white_dark")(x, y, z, face, variant, box=box, **k)
    return HIDE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("shagaramon")
    mats = {"skin": ROBE, "neck": HIDE, "hand": HIDE, "finger": HIDE, "claw": solid(P, "white")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.8, leg_bulk=0.8, claws=True, name="shagaramon")
    m.boxes[:] = [b for b in m.boxes if b.bone not in ("leg_left", "leg_right")]
    m.bones[:] = [b for b in m.bones if b["name"] not in ("leg_left", "leg_right")]
    bd = a["body"]
    m.round_box(bd, 0, 0, 5.2, 4.0, 36.0, 38.6, solid(P, "red"), cut=1)                     # red sash
    for side in ("arm_left", "arm_right"):                                               # wide sleeves
        e = a[side]["elbow"]
        m.box(a[side]["bone"], e[0] - 3.0, e[1] - 14.0, e[2] - 3.0, e[0] + 3.0, e[1] + 2.0, e[2] + 3.0, ROBE)
    tl = m.bone("tail", bd, (0, 30, 0))                                                  # coiled serpent tail
    pts = [(0, 32.0, 0), (0, 22.0, 2.0), (4.0, 12.0, 6.0), (10.0, 8.0, 10.0), (18.0, 10.0, 12.0), (24.0, 16.0, 10.0),
           (28.0, 24.0, 8.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, max(2, 6 - i), tailf, extend=0.6)
        if 1 <= i <= 4:
            spike(m, tl, p1, (0, 1, 0.6), 1.2, 4.0, feathers(P, "white", "white_dark"), tip=0.8)
    for j in range(5):                                                                   # feathered tail fin
        spike(m, tl, pts[-1], (0.4 + (j - 2) * 0.2, 1, (j - 2) * 0.3), 2.0, 10.0, feathers(P, "teal", "blue_dark"),
              tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.4, 2.4, 3.4, 54.0, 59.0, HIDE, cut=1)                             # slender dragon head
    m.round_box(hd, 0, -5.4, 1.4, 1.6, 54.4, 56.6, HIDE, cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.3, sx * 2.5), 57.0, -3.4, max(sx * 2.3, sx * 2.5), 57.8, -2.2, solid(P, "eye", glow=True))
        pts2 = [(sx * 1.6, 59.0, -1.0), (sx * 3.0, 64.0, -1.0), (sx * 5.0, 66.0, 1.0)]
        for p0, p1 in zip(pts2, pts2[1:]):                                                # golden antlers
            rod(m, hd, p0, p1, 1, metal(P, "gold", dark="gold_dark"), extend=0.2, t2=2)
        spike(m, hd, pts2[1], (sx * 1, 0.4, 0), 0.8, 2.4, metal(P, "gold"), tip=0.8)
    ball(m, hd, (0, 59.6, -3.0), 1.0, gem(P, "pearl", "white"), layers=1)
    for sx in (-1, 1):                                                                   # trailing mist
        rod(m, bd, (sx * 6.0, 50.0, 2.0), (sx * 18.0, 54.0, 6.0), 2, solid(P, "mist"), extend=0.2, t2=4)
    return m
