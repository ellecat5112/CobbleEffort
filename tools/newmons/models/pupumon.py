"""Pupumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a pale lilac-white blob with two big black eyes and a little zigzag mouth, and two big translucent
blue leaf-ears on top. 0.35 blocks.

Front is -z, y is up. 14 units tall; Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 14
SCALE, HITBOX = sized(0.35, HEIGHT, 1.6)
KIND = "floater"
K = 4
LOOK = "a pale lilac-white blob with big black eyes, a zigzag mouth and two big blue leaf-ears"
BASE = {"white": (236, 236, 250), "white_dark": (190, 190, 220), "black": (20, 20, 26), "glint": (255, 255, 255),
        "blue": (80, 140, 220, 220), "cream": (250, 240, 214)}
SHINY = {"white": (250, 230, 236), "white_dark": (220, 180, 196), "blue": (240, 120, 160, 220)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.2, (y - 5.4) * 0.8)
            if math.hypot(x - sx * 2.2 + 0.4, y - 5.9) < 0.35:
                return tone(p["glint"], face), None
            if d < 1.2:
                return tone(p["black"], face), None
        if abs(y - 3.4 - 0.3 * abs(math.sin(x * 2.4))) < 0.18 and abs(x) < 1.4:
            return tone(p["black"], face), None
    if y < 2.0:
        return tone(p["cream"], face), None
    return skin(P, "white", dark="white_dark", var=0.02)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("pupumon")
    top = m.bone("pupumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    ball(m, bd, (0, 4.6, 0), 4.8, bodyf, layers=4, ry=4.2, squash=0.9)
    for sx in (-1, 1):
        m.box(bd, min(sx * 1.6, sx * 6.0), 7.0, 0, max(sx * 1.6, sx * 6.0), 13.0, 0, solid(P, "blue"),
              rotation=(0, 0, -sx * 20), pivot=(sx * 1.6, 7.0, 0))
    return m
