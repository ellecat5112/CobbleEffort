"""Chibickmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a tiny cream baby shaped like a soft rounded star, with two little pointed side points, big black
eyes, a happy pink mouth and two stubby feet. Baby I. make(sword=True): Chibick Sword, the long serrated bone-white
blade it turns into in the manga, studded with knobs along its spine, with a grip at its base.

Front is -z, y is up. 18 units tall (the sword: 40, a Child-sized weapon Digimon).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, skin, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.35, HEIGHT, 0.45)
KIND = "floater"
K = 4
LOOK = "a tiny cream baby shaped like a soft rounded star with big black eyes and a happy pink mouth"
BASE = {"cream": (252, 240, 170), "cream_dark": (220, 196, 110), "eye": (20, 20, 24), "white": (255, 255, 255),
        "mouth": (240, 90, 120), "foot": (140, 120, 60), "bone": (236, 232, 220), "bone_dark": (170, 164, 150),
        "grip": (90, 70, 50)}
SHINY = {"cream": (200, 230, 255), "cream_dark": (140, 180, 230), "bone": (230, 210, 240), "bone_dark": (170, 140, 190)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.6, y - 7.6)
            if d < 1.3:
                return tone(p["white"] if math.hypot(x - sx * 2.6 + 0.4, y - 8.0) < 0.4 else p["eye"], face), None
        if 4.6 < y < 6.0 and abs(x) < 1.0 - (6.0 - y) * 0.4:
            return tone(p["mouth"], face), None
    return skin(P, "cream", dark="cream_dark", var=0.03)(x, y, z, face, variant, box=box, **k)


def make(name, sword=False):
    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 6, 0))
        if sword:
            BONE = metal(P, "bone", dark="bone_dark")
            m.box(bd, -1.4, 0.0, -1.4, 1.4, 7.0, 1.4, solid(P, "grip"))                 # grip
            m.box(bd, -4.0, 7.0, -1.8, 4.0, 9.0, 1.8, BONE)                            # guard
            for i in range(10):                                                       # serrated blade
                y0 = 9.0 + i * 3.2
                w = 2.6 - i * 0.18
                m.box(bd, -w, y0, -1.0, w, y0 + 3.4, 1.0, BONE)
                for sx in (-1, 1):
                    spike(m, bd, (sx * w, y0 + 1.6, 0), (sx, 0.5, 0), 1.2, 1.8, BONE, tip=0.4)
                m.box(bd, -0.8, y0 + 1.0, -1.6, 0.8, y0 + 2.4, -1.0, solid(P, "bone_dark"))   # knob
            spike(m, bd, (0, 41.0, 0), (0, 1, 0), 1.6, 3.0, BONE, tip=0.3)
            return m
        for r, y0, y1 in ((5.0, 1.0, 3.0), (6.4, 3.0, 9.0), (5.4, 9.0, 11.6), (3.4, 11.6, 13.4), (1.6, 13.4, 15.6)):
            m.round_box(bd, 0, 0, r, r * 0.8, y0, y1, bodyf, cut=max(1, round(r * 0.35)))
        for sx in (-1, 1):                                                           # little star points
            spike(m, bd, (sx * 6.0, 8.0, 0), (sx, 0.3, 0), 3.0, 4.0, bodyf, tip=0.6)
            m.box(bd, sx * 3.0 - 1.0, 0.0, -1.6, sx * 3.0 + 1.0, 1.2, 1.0, solid(P, "foot"))
        return m
    return build


build = make("chibickmon")
