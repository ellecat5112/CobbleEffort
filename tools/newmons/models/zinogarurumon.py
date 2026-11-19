"""Zino Garurumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a thunder-wolf of scales: a lean blue-and-teal scaled wolf-dragon on four clawed legs,
a long fanged muzzle with a horned brow, a crest of tall pale-blue crystal spines running down its neck and back,
gold-studded scales along its flanks, pink-tipped claws and a long spined tail. 35 blocks.

Front is -z, y is up. Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import eye, gem, scales, solid
from _route import pal, tone

HEIGHT = 37
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a lean blue-and-teal scaled wolf-dragon with a crest of tall pale-blue crystal spines, gold-studded flanks and pink-tipped claws"
BASE = {"blue": (90, 130, 200), "blue_dark": (34, 60, 130), "teal": (90, 190, 180), "gold": (240, 210, 90),
        "crystal": (170, 200, 250), "crystal_light": (240, 250, 255), "pink": (230, 80, 140), "eye": (230, 50, 60),
        "pupil": (20, 10, 10), "white": (255, 255, 255), "cream": (240, 236, 220)}
SHINY = {"blue": (200, 130, 80), "blue_dark": (130, 70, 30), "crystal": (250, 200, 160)}


def P(v):
    return pal(BASE, SHINY, v)


def hidef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and (int(z * 0.9 + 40) + int(y * 0.9)) % 7 == 0:
        return tone(p["gold"], face), None
    if face in ("east", "west") and (y + z * 0.3) % 5.0 < 0.8:
        return tone(p["teal"], face), None
    return scales(P, "blue", "blue_dark", size=1.0)(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 23.0, y - 27.0, 0.9, "eye", slit=True)
        if c is not None:
            return c, None
    return hidef(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("zinogarurumon")
    mats = {"skin": hidef, "belly": scales(P, "cream", "blue"), "neck": hidef, "head": headf, "leg": hidef,
            "paw": hidef, "claw": solid(P, "pink"), "tail": hidef}
    a = quadruped(m, mats, "zinogarurumon", length=30.0, body_y=18.0, body_rx=6.0, body_ry=6.0, chest_bulk=1.15,
                  neck=((0, 24, -17), (0, 26, -21)), head_len=11.0, head_w=3.6, head_h=4.4, snout=0.7, mouth_open=14,
                  teeth=6, tail=((0, 20, 15), (0, 24, 21), (0, 30, 24), (0, 36, 24)), tail_r=(2.4, 1.8, 1.4, 1.0),
                  toes=3, claws=True)
    bd, hd = a["body"], a["head"]
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 29.0, -19.0), (sx * 0.3, 0.6, 1), 1.2, 6.0, solid(P, "cream"), tip=0.8)
    for i in range(10):                                                                 # crystal spines
        z = -18.0 + i * 3.6
        spike(m, bd, (0, 24.0 - abs(i - 3) * 0.4, z), (0, 1, 0.3), 2.2, 10.0 - abs(i - 2) * 0.8,
              gem(P, "crystal", "crystal_light", glow=False), tip=0.8)
    for j in range(5):
        spike(m, bd, (0, 26.0 + j * 2.4, 21.0 + j * 0.6), (0, 0.4, 1), 1.2, 4.0, gem(P, "crystal", "crystal_light"),
              tip=0.8)
    return m
