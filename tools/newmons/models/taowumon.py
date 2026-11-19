"""Taowumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a huge pale-blue demon beast, half tiger and half boar: dark stripes on its hide, a pale boar head
with long curving tusks and pointed ears, a bony white plated back bristling with tall bone spines, ice-blue spirit
flames streaming off its back, icy crystal hooves, and a long spined tail ending in a little biting head. 35 blocks.

Front is -z, y is up. Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digidetail import armour, eye, metal, plane, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a huge pale-blue tiger-boar demon beast with long tusks, a spiny bone-plated back, ice-blue spirit flames and a biting tail"
BASE = {"blue": (120, 190, 210), "blue_dark": (50, 110, 140), "stripe": (40, 70, 100), "bone": (230, 226, 210),
        "bone_dark": (160, 150, 130), "ice": (160, 230, 250), "ice_dark": (80, 160, 210), "flame": (110, 230, 240, 190),
        "tusk": (246, 244, 236), "eye": (250, 210, 40), "pupil": (20, 10, 10), "white": (255, 255, 255),
        "mouth": (120, 20, 40)}
SHINY = {"blue": (200, 140, 210), "blue_dark": (130, 70, 150), "flame": (240, 120, 230, 190)}


def P(v):
    return pal(BASE, SHINY, v)


def hidef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face != "down" and (z * 0.6 + math.sin(y * 0.8) * 1.2) % 4.0 < 0.8:
        return tone(p["stripe"], face), None
    return skin(P, "blue", dark="blue_dark")(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 24.0, y - 29.0, 1.2, "eye", slit=True)
        if c is not None:
            return c, None
    return skin(P, "bone", dark="bone_dark")(x, y, z, face, variant, box=box, **k)


ICE = metal(P, "ice", dark="ice_dark")


def build():
    m = Model("taowumon")
    mats = {"skin": hidef, "belly": skin(P, "blue", dark="blue_dark"), "neck": hidef, "head": headf, "leg": hidef,
            "paw": ICE, "claw": ICE, "tail": hidef}
    a = quadruped(m, mats, "taowumon", length=40.0, body_y=20.0, body_rx=8.0, body_ry=8.0, chest_bulk=1.2,
                  neck=((0, 26, -20), (0, 27, -23)), head_len=12.0, head_w=5.0, head_h=6.0, snout=0.5, mouth_open=12,
                  teeth=6, tail=((0, 22, 20), (0, 18, 28), (0, 14, 36), (0, 16, 42)), tail_r=(2.4, 2.0, 1.6, 1.2),
                  toes=3, claws=True)
    bd, hd = a["body"], a["head"]
    for i in range(9):                                                                 # bone plates + spines
        z = -16.0 + i * 4.0
        m.round_box(bd, 0, z, 5.0, 2.0, 27.0, 29.6, armour(P, "bone", "bone_dark"), cut=1)
        spike(m, bd, (0, 29.0, z), (0, 1, 0.3), 2.0, 8.0 + 3.0 * math.sin(i / 8 * math.pi), solid(P, "bone"), tip=0.8)
        for sx in (-1, 1):
            spike(m, bd, (sx * 4.0, 27.6, z), (sx * 0.7, 1, 0.2), 1.2, 4.0, solid(P, "bone"), tip=0.8)
    fl = m.bone("flame", bd, (0, 30, 0))                                                # spirit flames
    for i in range(8):
        z = -14.0 + i * 4.4
        spike(m, fl, (0, 32.0, z), (0.2 * math.sin(i), 1, 0.7), 4.0, 12.0 + 4.0 * math.sin(i * 1.3) ** 2,
              solid(P, "flame", glow=True), tip=0.8)
    sf = a["snout_front"]
    for sx in (-1, 1):                                                                 # tusks + ears
        pts = [(sx * 3.4, 26.0, sf + 3.0), (sx * 6.0, 26.6, sf - 1.0), (sx * 8.6, 29.0, sf - 3.4), (sx * 9.6, 32.0, sf - 4.0)]
        for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 2 if i < 2 else 1, solid(P, "tusk"), extend=0.5)
        spike(m, hd, (sx * 3.8, 31.0, -20.0), (sx * 0.6, 1, 0.4), 2.0, 4.0, skin(P, "blue", dark="blue_dark"), tip=0.8)
    tl = a.get("tail") or bd
    ball(m, bd, (0, 16.0, 43.0), 2.4, headf, layers=2)                                  # the tail's little head
    for j in range(3):
        spike(m, bd, (0, 17.0, 44.4 + j * 0.6), (0, 0.3, 1), 0.8, 2.0, solid(P, "tusk"), tip=0.8)
    for j in range(6):
        spike(m, bd, (0, 20.0 - j * 0.8, 22.0 + j * 3.4), (0, 1, 0.3), 1.0, 2.6, solid(P, "bone"), tip=0.8)
    return m
