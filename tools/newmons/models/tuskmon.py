"""Tuskmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a squat green dinosaur crouched on four limbs: two great horns curling forward from its brow, banded
red and black, magenta stripes down its back and tail, rows of cream spikes along its spine, a skull-and-crossbones
mark on its shoulder, a toothy jaw and curved cream claws. 15 blocks.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digidetail import eye, plane, scales, skin, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a squat green dinosaur with two great red-and-black banded horns, magenta stripes, cream spine spikes and a skull mark"
BASE = {"green": (90, 160, 60), "green_dark": (36, 90, 24), "pink": (220, 60, 120), "cream": (250, 240, 200),
        "red": (210, 40, 40), "black": (30, 30, 34), "eye": (110, 60, 150), "pupil": (20, 10, 20),
        "white": (255, 255, 255), "skull": (230, 230, 220)}
SHINY = {"green": (80, 110, 170), "green_dark": (30, 50, 110)}


def P(v):
    return pal(BASE, SHINY, v)


def hidef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("up", "east", "west") and y > 12.0 and (z * 0.5 + abs(x) * 0.2) % 3.0 < 0.5:
        return tone(p["pink"], face), None
    if face == "east" and math.hypot(z + 5.0, y - 15.0) < 1.6:
        return tone(p["skull"], face), None
    return scales(P, "green", "green_dark", size=1.2)(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 17.0, y - 19.0, 1.0, "eye", slit=True)
        if c is not None:
            return c, None
    return hidef(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("tuskmon")
    mats = {"skin": hidef, "belly": skin(P, "green", dark="green_dark"), "neck": hidef, "head": headf, "leg": hidef,
            "paw": hidef, "claw": solid(P, "cream"), "tail": hidef}
    a = quadruped(m, mats, "tuskmon", length=24.0, body_y=12.0, body_rx=6.4, body_ry=6.0, chest_bulk=1.25,
                  neck=((0, 16, -12), (0, 18, -14)), head_len=11.0, head_w=4.6, head_h=5.0, snout=0.6, mouth_open=16,
                  teeth=6, tail=((0, 13, 12), (0, 12, 18), (0, 14, 24), (0, 19, 27)), tail_r=(2.6, 2.0, 1.4, 1.0),
                  toes=3, claws=True)
    bd, hd = a["body"], a["head"]
    for sx in (-1, 1):                                                                 # banded horns
        pts = [(sx * 3.0, 22.0, -13.0), (sx * 6.0, 26.0, -13.0), (sx * 8.0, 27.0, -17.0), (sx * 7.0, 24.0, -21.0)]
        for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
            for t in range(3):
                q0 = tuple(p0[c] + (p1[c] - p0[c]) * t / 3 for c in range(3))
                q1 = tuple(p0[c] + (p1[c] - p0[c]) * (t + 1) / 3 for c in range(3))
                rod(m, hd, q0, q1, 2 if i < 2 else 1, solid(P, "red" if (i * 3 + t) % 2 else "black"), extend=0.2)
    for j in range(9):                                                                 # spine spikes
        spike(m, bd, (0, 18.0 - (j > 5) * (j - 5) * 1.0, -8.0 + j * 3.6), (0, 1, 0.2), 1.4, 3.0, solid(P, "cream"),
              tip=0.8)
    return m
