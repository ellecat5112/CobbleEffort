"""Bitmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a pink armoured mouse-cat. A round pink-and-white armoured body, a pointed pink helm with a grey visor
and a green eye, a blue scarf, two long curling ribbon-ears banded black and pink sweeping back over its body, and
four stubby armoured legs with claws. 15 blocks tall.

Front is -z, y is up. 32 units tall; Adult stage (Armor).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digidetail import armour, eye, fabric, local, metal, solid
from _route import pal, tone

HEIGHT = 32
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 14}
LOOK = ("a pink armoured mouse-cat: a round pink-and-white armoured body, a pointed helm with a visor and green eye, a "
        "blue scarf and two long curling ribbon-ears banded black and pink")
BASE = {"pink": (240, 120, 180), "pink_dark": (180, 60, 120), "pink_light": (255, 200, 230), "white": (246, 244, 248),
        "white_dark": (190, 186, 196), "black": (34, 32, 40), "grey": (150, 152, 164), "blue": (60, 90, 200),
        "blue_dark": (24, 40, 120), "eye": (90, 200, 120), "pupil": (16, 30, 20), "claw": (240, 240, 244)}
SHINY = {"pink": (120, 190, 240), "pink_dark": (60, 120, 190), "pink_light": (200, 230, 255), "blue": (240, 140, 40),
         "blue_dark": (170, 80, 16)}


def P(v):
    return pal(BASE, SHINY, v)


PINK = armour(P, "pink", "pink_dark", light="pink_light")
WHITE = armour(P, "white", "white_dark")


def ribbonf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = (box.lo[2] + box.size[2] - z) if box else 0
    return tone(p["black"] if (t % 4.0) < 1.4 else p["pink"], face), None


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        c = eye(p, x - 0.0, y - 16.0, 1.2, "eye")
        if c is not None:
            return c, None
        if abs(y - 16.0) < 1.8 and abs(x) < 2.6:
            return tone(p["grey"], face), None
    return PINK(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("bitmon")
    mats = {"skin": WHITE, "belly": PINK, "neck": PINK, "head": headf, "snout": PINK, "jaw": WHITE,
            "mouth": solid(P, "black"), "tooth": solid(P, "white"), "leg_upper": PINK, "leg_lower": WHITE, "paw": PINK,
            "claw": solid(P, "claw"), "tail": PINK}
    a = quadruped(m, mats, "bitmon", length=20.0, body_y=11.0, body_rx=6.4, body_ry=6.0, chest_bulk=1.1,
                  neck=((0, 13, -10), (0, 14, -12)), head_len=8.0, head_w=4.0, head_h=4.4, snout=0.4, mouth_open=4,
                  teeth=0, leg_bulk=1.3, toes=3, tail=((0, 12, 11), (0, 11, 13)), tail_r=(1.0, 0.8))
    hd = a["head"]
    spike(m, hd, (0, 18.0, -12.0), (0, 0.6, -1), 1.6, 3.0, PINK)                       # pointed helm tip
    m.round_box(a["neck"], 0, -10.0, 4.2, 3.0, 11.0, 13.4, fabric(P, "blue", "blue_dark"), cut=1)   # scarf
    for sx in (-1, 1):                                           # long curling ribbon-ears
        ear = m.bone("ear_left" if sx > 0 else "ear_right", hd, (sx * 3.0, 18.0, -10.0))
        pts = [(sx * 3.0, 18.0, -10.0), (sx * 5.0, 22.0, -6.0), (sx * 6.0, 23.0, 2.0), (sx * 6.0, 20.0, 9.0),
               (sx * 5.0, 14.0, 13.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ear, p0, p1, 3, ribbonf, extend=0.4, t2=1)
    return m
