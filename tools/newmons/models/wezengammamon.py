"""Wezen Gammamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): an armoured teal ceratopsian: a low four-legged body of teal plates with white
joints, an orange-and-teal spiked frill, a toothy beaked head, a tail tipped with a glowing thruster, and three long
black cannon barrels mounted on its back, angled forward over its head. 15 blocks.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digidetail import armour, eye, metal, solid
from _route import pal, tone

HEIGHT = 17
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "an armoured teal ceratopsian with a spiked orange-and-teal frill and three long black cannon barrels on its back"
BASE = {"teal": (60, 140, 130), "teal_dark": (20, 70, 70), "white": (236, 240, 244), "orange": (240, 150, 40),
        "black": (34, 34, 40), "black_dark": (12, 12, 14), "glow": (255, 220, 80), "eye": (250, 220, 60),
        "pupil": (20, 10, 10)}
SHINY = {"teal": (140, 90, 160), "teal_dark": (70, 40, 100)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "teal", "teal_dark", trim="white", panel=(3.0, 3.0))


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 15.4, y - 13.6, 0.8, "eye", slit=True)
        if c is not None:
            return c, None
    return ARM(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("wezengammamon")
    mats = {"skin": ARM, "belly": metal(P, "white"), "neck": ARM, "head": headf, "leg": ARM, "paw": metal(P, "white"),
            "claw": solid(P, "black"), "tail": ARM}
    a = quadruped(m, mats, "wezengammamon", length=20.0, body_y=9.0, body_rx=5.0, body_ry=4.6, chest_bulk=1.1,
                  neck=((0, 11, -10), (0, 12, -12)), head_len=8.0, head_w=3.0, head_h=3.6, snout=0.6, mouth_open=12,
                  teeth=4, tail=((0, 10, 10), (0, 9, 15), (0, 10, 19)), tail_r=(2.0, 1.4, 1.0), toes=0, claws=False)
    bd, hd = a["body"], a["head"]
    for i in range(5):                                                                 # frill
        ang = (i - 2) * 0.45
        spike(m, hd, (math.sin(ang) * 2.4, 15.0, -10.0), (math.sin(ang), 0.8, 0.6), 1.8, 4.0,
              solid(P, "orange" if i % 2 else "teal"), tip=0.8)
    for j in range(3):                                                                 # three cannon barrels
        x = (j - 1) * 2.4
        rod(m, bd, (x, 14.0 + (1 - abs(j - 1)) * 1.6, 4.0), (x * 1.2, 22.0 + (1 - abs(j - 1)) * 1.6, -22.0), 1,
            metal(P, "black", dark="black_dark"), extend=0.0)
        m.round_box(bd, x, 4.0, 1.6, 2.0, 12.6, 15.6, metal(P, "black", dark="black_dark"), cut=1)
    ball(m, bd, (0, 10.0, 20.0), 1.2, solid(P, "glow", glow=True), layers=1)
    return m
