"""Kyukimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
sickle weasel: a lithe pink weasel-beast traced with red tribal lines, a wild mane of dark blue hair that sweeps back
into a great curling blue tail, a curved tusk-horn on its snout, a long silver sickle blade on its tail and small
clawed paws. 25 blocks long.

Front is -z, y is up. 36 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "quadruped"
K = 3
LOOK = "a lithe pink weasel-beast with red tribal lines, a wild dark blue mane sweeping into a curling tail and a silver sickle blade"
BASE = {"pink": (240, 170, 190), "pink_dark": (190, 110, 130), "red": (210, 40, 50), "blue": (50, 70, 150),
        "blue_dark": (20, 26, 80), "steel": (220, 224, 234), "steel_dark": (110, 114, 126), "tusk": (240, 220, 180),
        "eye": (250, 220, 60), "mouth": (160, 40, 50), "tooth": (250, 250, 246), "claw": (240, 240, 240)}
SHINY = {"pink": (200, 220, 250), "pink_dark": (130, 150, 200), "blue": (60, 130, 60), "blue_dark": (20, 70, 20)}


def P(v):
    return pal(BASE, SHINY, v)


def hidef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and abs(math.sin(z * 0.6 + y * 0.3)) > 0.95:
        return tone(p["red"], face), None
    return skin(P, "pink", dark="pink_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("kyukimon")
    mats = {"skin": hidef, "belly": hidef, "neck": hidef, "head": hidef, "snout": hidef, "jaw": hidef,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": hidef, "leg_lower": hidef,
            "paw": hidef, "claw": solid(P, "claw"), "tail": strands(P, "blue", "blue_dark")}
    a = quadruped(m, mats, "kyukimon", length=24.0, body_y=14.0, body_rx=4.2, body_ry=4.6, chest_bulk=1.3,
                  neck=((0, 18, -10), (0, 22, -13)), head_len=8.0, head_w=3.0, head_h=3.4, snout=0.8, mouth_open=8,
                  teeth=2, leg_bulk=0.9, toes=3, tail=((0, 18, 12), (0, 24, 18), (0, 30, 16)), tail_r=(2.4, 2.0, 1.6))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.3, ez - 0.7, max(sx * ex, sx * (ex + 0.3)), ey + 0.3, ez + 0.7,
              solid(P, "eye"))
    sn = (0, a["mouth_y"] + 1.6, a["snout_front"] + 1.0)
    pts = [sn, (2.0, sn[1] + 1.6, sn[2] - 2.0), (3.0, sn[1] + 3.6, sn[2] - 1.0)]       # curved tusk-horn
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, hd, p0, p1, 1, solid(P, "tusk"), extend=0.2, t2=1)
    MANE = strands(P, "blue", "blue_dark")
    for i in range(10):                                                              # wild blue mane
        spike(m, bd if i > 3 else a["neck"], (0, 19.6 if i > 3 else 23.0, -12.0 + i * 2.6), (0, 0.8, 1), 2.4, 6.0, MANE,
              tip=0.8)
    tb = a["tail"]
    pts = [(0, 30.0, 16.0), (0, 34.0, 10.0), (0, 32.0, 6.0), (0, 28.0, 8.0)]          # curling tail end
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 2, MANE, extend=0.4)
    for j in range(4):                                                               # sickle blade
        rod(m, tb, (0, 18.0 - j * 1.6, 18.0 + j * 4.0), (0, 16.4 - j * 1.6, 22.0 + j * 4.0), 1,
            metal(P, "steel", dark="steel_dark"), extend=0.2, t2=3)
    return m
