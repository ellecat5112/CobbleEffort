"""Sangloupmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a vampire wolf: a lean violet beast with a shaggy silver-white mane and chest, a bat-winged violet
blade-crest on its head, sabre fangs, red flame marks on its tail and flanks, a ruby-ringed ear, black-violet armoured
paws with long silver blade-claws, and a bushy violet tail. 15 blocks.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, fur, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a lean violet vampire wolf with a silver mane, a bat-winged blade crest, sabre fangs, red flame marks and silver blade-claws"
BASE = {"violet": (100, 70, 170), "violet_dark": (40, 24, 90), "silver": (220, 220, 236), "silver_dark": (150, 150, 176),
        "red": (220, 60, 50), "steel": (220, 224, 236), "steel_dark": (110, 114, 130), "eye": (240, 60, 60),
        "tooth": (250, 250, 240)}
SHINY = {"violet": (60, 60, 70), "violet_dark": (20, 20, 26), "red": (90, 200, 240)}


def P(v):
    return pal(BASE, SHINY, v)


def furf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west", "up") and abs(math.sin(z * 0.8 + y * 0.6)) > 0.93 and z > -4.0:
        return tone(p["red"], face), None
    if z < -8.0 or face == "down":
        return fur(P, "silver", "silver_dark", length=1.6)(x, y, z, face, variant, box=box, **k)
    return fur(P, "violet", "violet_dark", length=1.4)(x, y, z, face, variant, box=box, **k)


STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("sangloupmon")
    mats = {"skin": furf, "head": furf, "paw": armour(P, "violet_dark", "violet_dark"), "claw": STEEL,
            "tooth": solid(P, "tooth")}
    a = quadruped(m, mats, "sangloupmon", length=26.0, body_y=18.0, body_rx=6.0, body_ry=6.4, chest_bulk=1.25,
                  neck=((0, 26, -14), (0, 30, -18)), head_len=10.0, head_w=4.0, head_h=4.4, teeth=4, mouth_open=12,
                  tail=((0, 20, 14), (0, 24, 20), (0, 30, 24)), tail_r=(3.0, 3.4, 2.6))
    hd = a["head"]
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.6, 28.0, -25.0), (0, -1, -0.1), 0.9, 4.0, solid(P, "tooth"), tip=0.8)   # sabre fangs
        x0, x1 = sorted((sx * 3.9, sx * 4.2))
        m.box(hd, x0, 31.0, -24.0, x1, 31.8, -22.6, solid(P, "eye", glow=True))
        for j in range(3):                                                               # bat-winged crest
            spike(m, hd, (sx * 2.0, 33.0, -18.0 + j * 1.4), (sx * (1.0 - j * 0.2), 0.6 + j * 0.2, 0.4), 1.2,
                  6.0 - j, armour(P, "violet", "violet_dark"), tip=0.8)
    spike(m, hd, (0, 33.0, -19.0), (0, 1, 0.3), 1.6, 6.0, armour(P, "violet", "violet_dark"), tip=0.8)
    for sx in (-1, 1):                                                                   # silver blade-claws
        for zz in (-8.0, 8.0):
            for f in range(3):
                spike(m, a["body"], (sx * 4.6 + (f - 1) * 1.0, 1.0, zz - 3.0), (0, -0.1, -1), 0.9, 5.0, STEEL, tip=0.8)
    return m
