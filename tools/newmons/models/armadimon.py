"""Armadimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a cheerful yellow armadillo. A domed orange shell banded in a grid of plates, a yellow face with big
green eyes under an armoured brow with a red gem plate and spiked crest, a violet belly, a thick tail and big claws
on its stubby legs. 1 block tall.

Front is -z, y is up. 26 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped, slab_z
from _digidetail import armour, eye, metal, skin, solid
from _route import pal, tone

HEIGHT = 26
SCALE, HITBOX = sized(1.0, HEIGHT, 0.9)
KIND = "quadruped"
K = 4
ANIM = {"leg_amp": 16}
LOOK = ("a cheerful yellow armadillo with a domed orange grid-plated shell, big green eyes under an armoured brow with "
        "a red gem plate, a violet belly and big claws")
BASE = {"yellow": (250, 214, 60), "yellow_dark": (200, 150, 30), "orange": (240, 160, 40), "orange_dark": (180, 100, 20),
        "orange_light": (255, 210, 120), "violet": (130, 100, 190), "violet_dark": (80, 60, 140), "red": (220, 40, 40),
        "claw": (240, 240, 244), "claw_dark": (170, 170, 186), "eye": (90, 200, 120), "pupil": (16, 30, 20),
        "white": (250, 250, 250), "mouth": (180, 60, 60), "tooth": (250, 250, 250)}
SHINY = {"yellow": (200, 200, 214), "yellow_dark": (140, 140, 160), "orange": (90, 140, 220), "orange_dark": (40, 80, 160),
         "orange_light": (170, 210, 255)}


def P(v):
    return pal(BASE, SHINY, v)


SHELL = armour(P, "orange", "orange_dark", light="orange_light", panel=(1.8, 1.6))
HIDE = skin(P, "yellow", dark="yellow_dark", var=0.04)
CLAW = metal(P, "claw", dark="claw_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west", "north"):
        dz = z + 13.0 if face != "north" else abs(x) - 2.0
        c = eye(p, dz, y - 10.6, 1.4, "eye")
        if c is not None:
            return c, None
    return HIDE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("armadimon")
    mats = {"skin": HIDE, "belly": skin(P, "violet", dark="violet_dark"), "neck": HIDE, "head": headf, "snout": HIDE,
            "jaw": HIDE, "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": SHELL, "leg_lower": HIDE,
            "paw": HIDE, "claw": CLAW, "tail": SHELL}
    a = quadruped(m, mats, "armadimon", length=18.0, body_y=8.0, body_rx=5.6, body_ry=4.4, chest_bulk=1.0,
                  neck=((0, 9, -9), (0, 10, -11)), head_len=7.0, head_w=3.6, head_h=4.4, snout=0.3, mouth_open=6,
                  teeth=0, leg_bulk=1.3, toes=3, tail=((0, 9, 12), (0, 8, 16), (0, 7, 19)), tail_r=(1.8, 1.4, 1.0))
    bd = a["body"]
    for i in range(5):                                           # the domed shell bands
        z0 = -9 + i * 3.8
        slab_z(m, bd, 0, 10.0, z0, z0 + 3.6, 7.0 - abs(i - 2) * 0.5, 5.4 - abs(i - 2) * 0.4, SHELL)
    hd = a["head"]
    m.box(hd, -3.8, 12.4, -14.6, 3.8, 14.4, -9.0, SHELL)                                  # armoured brow
    m.box(hd, -1.4, 12.8, -15.0, 1.4, 14.0, -14.4, solid(P, "red"))                      # red gem plate
    for sx in (-1, 0, 1):
        spike(m, hd, (sx * 2.0, 14.4, -12.0), (sx * 0.4, 1, 0.3), 1.2, 3.0 - abs(sx), solid(P, "yellow"))
    return m
