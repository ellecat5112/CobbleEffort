"""Brachimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a long-necked sauropod. A golden-yellow brachiosaur striped with blue chevrons along its neck,
back, legs and tail, a pale belly, a small head with a grey horn on the snout and a row of teeth, and four columnar
legs with white claws. 25 blocks tall.

Front is -z, y is up. 56 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import lerp, quadruped
from _digidetail import eye, scales, skin, solid
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a golden-yellow long-necked sauropod striped with blue chevrons, a pale belly, a small horned head and four "
        "columnar clawed legs")
BASE = {"gold": (246, 190, 50), "gold_dark": (190, 120, 20), "gold_light": (255, 230, 140), "blue": (40, 140, 220),
        "blue_dark": (14, 70, 140), "belly": (250, 230, 170), "horn": (170, 170, 180), "claw": (240, 240, 244),
        "eye": (230, 60, 50), "pupil": (30, 10, 10), "white": (255, 255, 255), "mouth": (130, 30, 30),
        "tooth": (250, 250, 246)}
SHINY = {"gold": (120, 200, 110), "gold_dark": (50, 120, 50), "gold_light": (200, 250, 180), "blue": (210, 60, 160),
         "blue_dark": (120, 20, 90)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "gold", "gold_dark", size=1.6, light="gold_light", rim_mix=0.3)
BELLY = skin(P, "belly", var=0.03)


def striped(x, y, z, face, variant, box=None, **k):
    """Blue chevron stripes across the hide, every few units along the body."""
    p = P(variant)
    if face != "down" and face != "north":
        t = (y * 0.6 + z * 0.8 - abs(x) * 0.6) % 6.0
        if t < 1.0:
            return tone(p["blue_dark"] if t < 0.25 else p["blue"], face), None
    return HIDE(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 21.0, y - 53.0, 0.8, "eye")
        if c is not None:
            return c, None
    return HIDE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("brachimon")
    mats = {"skin": striped, "belly": BELLY, "neck": striped, "head": headf, "snout": HIDE, "jaw": HIDE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": striped, "leg_lower": striped,
            "paw": HIDE, "claw": solid(P, "claw"), "tail": striped}
    a = quadruped(m, mats, "brachimon", length=26.0, body_y=20.0, body_rx=7.4, body_ry=8.0, chest_bulk=1.15,
                  neck=((0, 30, -15), (0, 38, -18), (0, 46, -20), (0, 52, -20)), head_len=8.0, head_w=2.8,
                  head_h=3.0, snout=0.5, mouth_open=6, teeth=4, leg_bulk=1.7, toes=4,
                  tail=((0, 22, 18), (2, 16, 24), (5, 12, 29), (9, 12, 32)), tail_r=(3.4, 2.4, 1.4, 0.8))
    hd = a["head"]
    spike(m, hd, (0, 53.6, -22.6), (0, 1, -0.3), 1.8, 3.6, solid(P, "horn"), tip=0.5)      # snout horn
    for j in range(5):                                                                   # ridge nubs on the neck
        p = lerp((0, 31, -13), (0, 50, -18), j / 4)
        spike(m, a["neck"], (0, p[1] + 1.4, p[2] + 2.0), (0, 0.4, 1), 1.4, 1.6, HIDE)
    return m
