"""Stegomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Armor Digimon of purity: a green stegosaur with orange stripes and spots, rows of great silver
plates along its back, a steel-armoured beak-head, white claws and a tail tipped with silver spikes. 15 blocks.

Front is -z, y is up. 30 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, metal, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a green stegosaur with orange stripes and spots, rows of great silver back plates, a steel-armoured beak-head and a spiked tail"
BASE = {"green": (70, 150, 60), "green_dark": (24, 80, 20), "orange": (240, 120, 40), "steel": (190, 194, 206),
        "steel_dark": (90, 94, 108), "claw": (246, 246, 240), "belly": (200, 220, 120), "eye": (250, 200, 40)}
SHINY = {"green": (150, 90, 170), "green_dark": (80, 40, 100), "orange": (90, 200, 220)}


def P(v):
    return pal(BASE, SHINY, v)


def hidef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("up", "east", "west") and (abs(math.sin(z * 0.8)) > 0.93 or math.hypot((x % 3.0) - 1.5, (z % 3.0) - 1.5) < 0.4):
        return tone(p["orange"], face), None
    return skin(P, "green", dark="green_dark")(x, y, z, face, variant, box=box, **k)


STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("stegomon")
    mats = {"skin": hidef, "belly": skin(P, "belly", dark="green_dark"), "head": armour(P, "steel", "steel_dark"),
            "snout": armour(P, "steel", "steel_dark"), "jaw": hidef, "claw": solid(P, "claw")}
    a = quadruped(m, mats, "stegomon", length=28.0, body_y=12.0, body_rx=7.0, body_ry=6.0, neck=((0, 13, -14),
                  (0, 12, -18)), head_len=9.0, head_w=3.6, head_h=3.6, snout=0.6, leg_len=8.0,
                  tail=((0, 14, 14), (0, 13, 20), (0, 12, 26)), tail_r=(3.0, 2.0, 1.4))
    for j in range(7):                                                                   # great back plates
        z = -10.0 + j * 3.4
        h = 9.0 - abs(j - 3) * 1.4
        for sx in (-1, 1):
            spike(m, a["body"], (sx * 1.6, 17.0 - abs(j - 3) * 0.6, z), (sx * 0.3, 1, 0.1), 2.6, h, STEEL, tip=0.8)
    for sx in (-1, 1):
        spike(m, "tail", (0, 12.0, 26.0), (sx * 0.8, 0.3, 0.6), 1.2, 4.0, STEEL, tip=0.8)
        x0, x1 = sorted((sx * 3.5, sx * 3.8))
        m.box(a["head"], x0, 12.6, -23.0, x1, 13.4, -21.6, solid(P, "eye"))
    return m
