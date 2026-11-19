"""Salamandamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Armor Digimon of courage: a long low salamander of molten rust-red hide patterned with swirling
golden flame marks, its whole outline licked by orange fire, a broad flat head with narrow eyes, stubby round-toed legs
and a long curling tail. 15 blocks.

Front is -z, y is up. 20 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import cutout, flame_inside, solid
from _route import pal, tone

HEIGHT = 20
SCALE, HITBOX = sized(15, HEIGHT, 8.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a long low molten rust-red salamander swirled with golden flame marks, licked all over by orange fire, with a long curling tail"
BASE = {"rust": (190, 70, 40), "rust_dark": (120, 30, 14), "gold": (250, 200, 60), "fire": (250, 140, 30, 220),
        "eye": (30, 20, 10)}
SHINY = {"rust": (60, 80, 180), "rust_dark": (20, 30, 110), "fire": (120, 190, 255, 220)}


def P(v):
    return pal(BASE, SHINY, v)


def hidef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("up", "east", "west") and abs(math.sin(z * 0.6 + abs(x) * 0.8) + math.cos(z * 0.3 - y)) > 1.5:
        return tone(p["gold"], face), p["gold"]
    return tone(p["rust"] if (x * 3 + y * 5 + z * 7) % 11 > 2 else p["rust_dark"], face), None


FIRE = cutout(flame_inside(tongues=3), solid(P, "fire", glow=True))


def build():
    m = Model("salamandamon")
    mats = {"skin": hidef, "head": hidef, "snout": hidef, "jaw": hidef, "claw": hidef}
    a = quadruped(m, mats, "salamandamon", length=30.0, body_y=8.0, body_rx=6.0, body_ry=3.6, neck=((0, 9, -16),
                  (0, 9, -19)), head_len=10.0, head_w=4.6, head_h=3.0, snout=0.2, mouth_open=2,
                  leg_len=5.0, tail=((0, 8, 15), (6, 7, 22), (10, 7, 18), (12, 7, 12)), tail_r=(3.0, 2.2, 1.4, 1.0))
    hd = a["head"]
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 4.4, sx * 4.7))
        m.box(hd, x0, 9.6, -24.0, x1, 10.2, -22.0, solid(P, "eye"))
    fb = m.bone("fire", a["body"], (0, 10, 0))                                            # flame outline
    for j in range(8):
        z = -14.0 + j * 4.0
        for sx in (-1, 1):
            m.box(fb, min(sx * 6.0, sx * 6.2), 6.0, z - 2.0, max(sx * 6.0, sx * 6.2), 16.0, z + 2.0, FIRE,
                  rotation=(0, 0, sx * -15), pivot=(sx * 6.0, 10.0, z))
        m.box(fb, -2.0, 11.0, z, 2.0, 17.0, z, FIRE)
    return m
