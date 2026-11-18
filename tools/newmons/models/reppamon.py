"""Reppamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the holy beast weasel: a shaggy white-and-brown fur beast wearing a white fox mask with red markings,
a great silver crescent blade rising from its back like a scythe, red-and-white bound tail tufts, red ribbon cords
on its legs, and wisps of blue wind round its paws. 15 blocks.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import fur, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a shaggy white-and-brown weasel beast in a red-marked white fox mask with a great silver crescent blade rising from its back"
BASE = {"white": (240, 238, 232), "white_dark": (180, 176, 166), "brown": (120, 80, 50), "brown_dark": (70, 44, 24),
        "red": (210, 40, 40), "steel": (210, 214, 230), "steel_dark": (90, 100, 150), "wind": (170, 220, 255, 170),
        "eye": (230, 60, 40), "black": (30, 26, 26)}
SHINY = {"brown": (60, 70, 110), "brown_dark": (24, 30, 60), "red": (60, 140, 220)}


def P(v):
    return pal(BASE, SHINY, v)


def furf(x, y, z, face, variant, box=None, **k):
    if y < 10.0 or z > 6.0:
        return fur(P, "brown", "brown_dark", length=1.4)(x, y, z, face, variant, box=box, **k)
    return fur(P, "white", "white_dark", length=1.8)(x, y, z, face, variant, box=box, **k)


def maskf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "up") and abs(abs(x) - 1.4) < 0.3:
        return tone(p["red"], face), None
    return tone(p["white"], face), None


def build():
    m = Model("reppamon")
    mats = {"skin": furf, "head": maskf, "snout": maskf, "jaw": furf, "claw": solid(P, "black")}
    a = quadruped(m, mats, "reppamon", length=24.0, body_y=16.0, body_rx=6.0, body_ry=6.0, neck=((0, 22, -13),
                  (0, 26, -16)), head_len=9.0, head_w=3.6, head_h=4.0, snout=0.6, tail=((0, 18, 13), (0, 20, 18),
                  (0, 24, 22)), tail_r=(2.6, 2.4, 2.0))
    bd = a["body"]
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 3.5, sx * 3.8))
        m.box(a["head"], x0, 27.0, -20.0, x1, 27.8, -18.8, solid(P, "eye", glow=True))
        spike(m, a["head"], (sx * 2.0, 30.0, -15.0), (sx * 0.3, 1, 0.3), 1.6, 4.0, maskf, tip=0.8)
    for j in range(6):                                                                   # shaggy mane
        spike(m, bd, ((j % 2 * 2 - 1) * 3.0, 22.0, -10.0 + j * 2.6), ((j % 2 * 2 - 1) * 0.6, 1, 0.4), 1.8, 5.0, furf,
              tip=0.8)
    pts = [(0, 22.0, -2.0), (0, 32.0, -6.0), (0, 40.0, -2.0), (0, 42.0, 6.0), (0, 38.0, 12.0)]   # crescent blade
    for p0, p1 in zip(pts, pts[1:]):
        m.box(bd, -0.6, min(p0[1], p1[1]) - 1.4, min(p0[2], p1[2]) - 1.4, 0.6, max(p0[1], p1[1]) + 1.4,
              max(p0[2], p1[2]) + 1.4, metal(P, "steel", dark="steel_dark"))
    for j in range(3):                                                                   # bound tail tufts
        m.round_box("tail", 0, 18.0 + j * 2.0, 2.0, 1.0, 19.0 + j * 1.6, 20.0 + j * 1.6, solid(P, "red"), cut=0)
    spike(m, "tail", (0, 24.0, 22.0), (0, 1, 0.4), 2.4, 5.0, solid(P, "white"), tip=0.8)
    for sx in (-1, 1):                                                                   # wind wisps
        for zz in (-8.0, 8.0):
            m.round_box(bd, sx * 5.0, zz, 3.0, 3.0, 0.2, 1.2, solid(P, "wind", glow=True), cut=1)
    return m
