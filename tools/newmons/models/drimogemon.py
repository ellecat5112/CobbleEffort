"""Drimogemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
drill mole. A shaggy pale-yellow mole with a dark blue-violet mane down its back, a little black eye, a huge gaping
red mouth full of white teeth, a steel drill on its nose and steel drill-tipped claws on its forepaws and hind feet.
15 blocks tall.

Front is -z, y is up. 34 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import fur, metal, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 3.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a shaggy pale-yellow mole with a dark blue-violet mane, a gaping fanged red mouth, a steel nose drill and steel "
        "drill-tipped claws")
BASE = {"yellow": (246, 238, 170), "yellow_dark": (190, 170, 100), "mane": (70, 70, 150), "mane_dark": (30, 30, 80),
        "steel": (180, 184, 196), "steel_dark": (70, 74, 86), "mouth": (200, 40, 50), "tooth": (250, 250, 246),
        "eye": (24, 24, 28)}
SHINY = {"yellow": (200, 220, 250), "yellow_dark": (130, 150, 190), "mane": (170, 60, 60), "mane_dark": (90, 20, 20)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "yellow", "yellow_dark", length=1.6, density=2.0)
MANE = fur(P, "mane", "mane_dark", length=2.0, density=1.8)
DRILL = metal(P, "steel", dark="steel_dark", streak=1.0)


def drill(m, bone, base, d, length, r0):
    n = math.sqrt(sum(v * v for v in d))
    u = tuple(v / n for v in d)
    for j in range(4):
        t0, t1 = j / 4, (j + 1) / 4
        rod(m, bone, tuple(b + u_ * length * t0 for b, u_ in zip(base, u)),
            tuple(b + u_ * length * t1 for b, u_ in zip(base, u)), max(1, round(r0 * 2 * (1 - t0))), DRILL, extend=0.2)


def build():
    m = Model("drimogemon")
    mats = {"skin": FUR, "belly": FUR, "neck": FUR, "head": FUR, "snout": FUR, "jaw": FUR,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": FUR, "leg_lower": FUR, "paw": FUR,
            "claw": DRILL, "tail": FUR}
    a = quadruped(m, mats, "drimogemon", length=26.0, body_y=14.0, body_rx=8.0, body_ry=8.4, chest_bulk=1.3,
                  neck=((0, 20, -11), (0, 22, -14)), head_len=10.0, head_w=5.0, head_h=5.6, snout=0.4, mouth_open=34,
                  teeth=6, leg_bulk=1.6, toes=3, tail=((0, 12, 13), (0, 10, 16)), tail_r=(2.0, 1.4))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.5, ez - 0.5, max(sx * ex, sx * (ex + 0.3)), ey + 0.5, ez + 0.5,
              solid(P, "eye"))
    drill(m, hd, (0, ey + 1.0, a["snout_front"] + 2.0), (0, 0.5, -1), 10.0, 2.4)          # nose drill
    for i in range(9):                                                                    # dark mane down the back
        t = i / 8
        spike(m, bd, (0, 23.0 - 4.0 * t, -12.0 + 24.0 * t), (0, 1, 0.8), 4.0 - t, 5.0 - 2.0 * t, MANE, tip=1.0)
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):  # drill claws
        w = a[nm]["wrist"]
        for j in range(3):
            drill(m, a[nm]["bone"], (w[0] + (j - 1) * 1.8, 2.0, w[2] - 2.4), (0, -0.2, -1), 4.0, 0.8)
    return m
