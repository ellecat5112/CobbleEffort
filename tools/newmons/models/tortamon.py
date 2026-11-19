"""Tortamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a yellow armoured tortoise-lizard: a low heavy body under a domed shell covered in tall spikes, a big
round shield-boss on its flank, a blunt head with blue eyes and a wide red mouth, spiked elbows and thick clawed feet,
and a short spiked tail. 15 blocks.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digidetail import armour, eye, skin, solid
from _route import pal, tone

HEIGHT = 23
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a yellow armoured tortoise-lizard with a spiked domed shell, a round shield-boss on its flank and a wide red mouth"
BASE = {"yellow": (240, 210, 60), "yellow_dark": (170, 130, 20), "spike": (250, 230, 120), "red": (210, 40, 50),
        "eye": (60, 150, 230), "pupil": (10, 10, 30), "white": (255, 255, 255), "spot": (190, 150, 30),
        "boss": (250, 220, 90), "boss_dark": (150, 110, 20)}
SHINY = {"yellow": (150, 200, 90), "yellow_dark": (80, 130, 40), "spike": (200, 240, 160)}


def P(v):
    return pal(BASE, SHINY, v)


def hidef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (int(x * 0.9 + 30) * 7 + int(y * 0.9) * 5 + int(z * 0.9 + 30) * 3) % 17 == 0:
        return tone(p["spot"], face), None
    return skin(P, "yellow", dark="yellow_dark")(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 17.0, y - 19.6, 1.0, "eye")
        if c is not None:
            return c, None
    return hidef(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("tortamon")
    mats = {"skin": hidef, "belly": skin(P, "yellow", dark="yellow_dark"), "neck": hidef, "head": headf, "leg": hidef,
            "paw": hidef, "claw": solid(P, "spike"), "tail": hidef}
    a = quadruped(m, mats, "tortamon", length=24.0, body_y=11.0, body_rx=7.0, body_ry=6.0, chest_bulk=1.1,
                  neck=((0, 14, -12), (0, 17, -14)), head_len=10.0, head_w=4.6, head_h=5.4, snout=0.4, mouth_open=16,
                  teeth=0, tail=((0, 11, 12), (0, 8, 17), (0, 5, 21)), tail_r=(2.4, 1.6, 1.0), toes=3, claws=True)
    bd, hd = a["body"], a["head"]
    ball(m, bd, (0, 15.0, 1.0), 8.6, armour(P, "yellow", "yellow_dark", panel=(3.0, 3.0)), layers=4, squash=0.7)
    for i in range(18):                                                                # tall shell spikes
        ang = i * 2.4
        r = 2.0 + (i % 6) * 1.2
        x, z = r * math.cos(ang), 1.0 + r * math.sin(ang)
        h = math.sqrt(max(0.0, 74.0 - r * r)) * 0.7
        spike(m, bd, (x, 15.0 + h * 0.6, z), (x * 0.12, 1, (z - 1.0) * 0.12), 2.0, 7.0 - r * 0.3, solid(P, "spike"),
              tip=0.8)
    for sx in (-1, 1):                                                                 # shield bosses
        m.round_box(bd, sx * 8.6, 2.0, 0.8, 3.6, 9.0, 16.0, armour(P, "boss", "boss_dark"), cut=0)
        spike(m, bd, (sx * 9.2, 12.4, 2.0), (sx, 0, 0), 1.6, 2.0, solid(P, "spike"), tip=0.8)
    for j in range(3):
        spike(m, bd, (0, 9.0 - j * 1.4, 14.0 + j * 3.0), (0, 1, 0.3), 1.0, 2.0, solid(P, "spike"), tip=0.8)
    return m
