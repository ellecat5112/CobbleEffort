"""Petaldramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Hybrid of wood, a dragon of the forest: a long low four-legged body of mossy green foliage over
bark, a round wooden face ringed by a ruff of red-brown leaves, legs ending in clusters of dark red leaves, twisted
branch-roots rising from its back and a long tail of tangled roots. 25 blocks long.

Front is -z, y is up. 30 units tall; Perfect (Hybrid) stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digidetail import fur, skin, solid, twisted
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a long low forest dragon of mossy foliage over bark, a round wooden face ringed by red-brown leaves, red leaf "
        "feet, twisted branch-roots on its back and a tail of tangled roots")
BASE = {"moss": (60, 130, 60), "moss_dark": (24, 70, 24), "bark": (140, 100, 60), "bark_dark": (80, 54, 30),
        "leaf": (150, 50, 40), "leaf_dark": (90, 20, 14), "face": (170, 130, 80), "eye": (240, 220, 120)}
SHINY = {"moss": (190, 150, 60), "moss_dark": (120, 90, 20), "leaf": (230, 180, 60)}


def P(v):
    return pal(BASE, SHINY, v)


MOSS = fur(P, "moss", "moss_dark", length=1.4)
BARK = twisted(P, "bark", "bark_dark")


def build():
    m = Model("petaldramon")
    mats = {"skin": MOSS, "claw": solid(P, "leaf"), "mouth": solid(P, "bark_dark"), "tooth": solid(P, "bark")}
    a = quadruped(m, mats, "petaldramon", length=34.0, body_y=12.0, body_rx=5.6, body_ry=4.6, chest_bulk=1.1,
                  neck=((0, 14, -16), (0, 14, -19)), head_len=5.0, head_w=4.0, head_h=4.0, snout=0.2, mouth_open=4,
                  teeth=0, leg_bulk=1.2, toes=3,
                  tail=((0, 12, 17), (4, 10, 24), (10, 9, 28), (16, 10, 30)), tail_r=(2.0, 1.6, 1.2, 0.8))
    hd = a["head"]
    hc = a["head_c"]
    ball(m, hd, (0, hc[1], hc[2] - 1.0), 3.6, skin(P, "face", dark="bark_dark"), layers=3, squash=0.6)  # wooden face
    for sx in (-1, 1):
        m.box(hd, sx * 1.4 - 0.4, hc[1] + 0.4, hc[2] - 3.3, sx * 1.4 + 0.4, hc[1] + 1.0, hc[2] - 3.15, solid(P, "eye"))
    m.box(hd, -1.4, hc[1] - 1.6, hc[2] - 3.3, 1.4, hc[1] - 1.2, hc[2] - 3.15, solid(P, "bark_dark"))
    for i in range(12):                                                                  # ruff of red leaves
        ang = 2 * math.pi * i / 12
        m.box(hd, -1.2, hc[1], hc[2] - 0.2, 1.2, hc[1] + 6.0, hc[2] + 0.2, skin(P, "leaf", dark="leaf_dark"),
              rotation=(0, 0, math.degrees(ang)), pivot=(0, hc[1], hc[2]))
    for j in range(6):                                                                   # branch-roots on its back
        z = -10.0 + j * 4.0
        pts = [(0, 16.0, z), ((j % 2 - 0.5) * 3.0, 22.0, z + 1.0), ((j % 2 - 0.5) * 2.0, 27.0 - j * 0.4, z + 2.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, a["body"], p0, p1, 1, BARK, extend=0.2)
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):  # red leaf feet
        anc = a[nm]
        w = anc.get("wrist") or anc.get("ankle")
        if w:
            for f in range(4):
                ang = 2 * math.pi * f / 4
                spike(m, anc["bone"], (w[0], 1.0, w[2]), (math.cos(ang), 0.2, math.sin(ang)), 1.4, 3.0,
                      solid(P, "leaf"), tip=0.8)
    return m
