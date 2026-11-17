"""Catch Mamemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the crane-game Mamemon. A little round grey Mamemon head with a happy face and a red joystick on
top, riding a dark teal UFO ring of coloured lights with slot-machine sevens, two jointed steel arms hanging down to a
big red claw that clutches a pile of eggs and capsules, and a blue lamp underneath. 25 blocks tall.

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, eye, gem, local, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 2.0)
KIND = "floater"
K = 3
LOOK = ("a little round grey Mamemon head riding a teal UFO ring of lights, with two steel arms ending in a big red "
        "crane claw full of eggs and capsules")
BASE = {"grey": (180, 184, 196), "grey_dark": (110, 114, 126), "teal": (50, 100, 100), "teal_dark": (20, 50, 50),
        "red": (220, 30, 30), "red_dark": (130, 10, 10), "steel": (200, 204, 216), "steel_dark": (90, 94, 106),
        "blue": (80, 160, 250), "blue_light": (210, 240, 255), "yellow": (250, 220, 50), "green": (60, 200, 90),
        "white": (255, 255, 255), "pupil": (20, 20, 24), "eye": (30, 30, 40), "mouth": (200, 50, 60),
        "egg1": (250, 200, 210), "egg2": (160, 210, 250), "egg3": (250, 240, 170)}
SHINY = {"teal": (110, 50, 120), "teal_dark": (50, 20, 60), "red": (240, 200, 40), "red_dark": (170, 120, 10)}


def P(v):
    return pal(BASE, SHINY, v)


TEAL = armour(P, "teal", "teal_dark", rivets=True)
STEEL = metal(P, "steel", dark="steel_dark")
CLAW = armour(P, "red", "red_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            c = eye(p, x - sx * 1.4, y - 35.6, 0.8, "eye")
            if c is not None:
                return c, None
        if abs(y - 34.0 + 0.3 * x * x) < 0.25 and abs(x) < 1.2:
            return tone(p["mouth"], face), None
    return metal(P, "grey", dark="grey_dark")(x, y, z, face, variant, box=box, **k)


def ringf(x, y, z, face, variant, box=None, **k):
    """The UFO ring: coloured lights round its rim and three red sevens on the front."""
    p = P(variant)
    if face in ("north", "south", "east", "west"):
        u, v, W, H = local(x, y, z, face, box)
        if face == "north" and abs(v - H / 2) < 0.9 and abs(x) < 4.0 and (x + 4.0) % 2.8 < 1.8:
            return tone(p["white"], face), None
        if abs(v - H / 2) < 0.5 and u % 2.0 < 0.8:
            c = p[("yellow", "green", "red", "blue")[int(u / 2.0) % 4]]
            return c, c
    return TEAL(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("catchmamemon")
    top = m.bone("catchmamemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 28, 0))
    m.round_box(bd, 0, 0, 7.6, 7.0, 28.0, 31.4, ringf, cut=2)                          # the UFO ring
    m.round_box(bd, 0, 0, 3.0, 3.0, 26.0, 28.0, gem(P, "blue", "blue_light"), cut=1)    # blue lamp
    hd = m.bone("head", bd, (0, 31, 0))
    ball(m, hd, (0, 35.0, 0), 3.8, headf, layers=4)
    rod(m, hd, (1.0, 38.4, 0), (2.4, 41.0, 0), 1, STEEL, extend=0)                      # the joystick
    ball(m, hd, (2.6, 41.4, 0), 1.0, solid(P, "red"), layers=2)
    for sx in (-1, 1):                                                                  # jointed arms
        ab = m.bone("arm_left" if sx > 0 else "arm_right", bd, (sx * 5.0, 28.0, 0))
        pts = [(sx * 5.0, 28.0, 0), (sx * 7.0, 20.0, 0), (sx * 6.4, 12.0, 0), (sx * 4.4, 8.0, 0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 1, STEEL, extend=0.3, t2=2)
            m.round_box(ab, p1[0], p1[2], 0.9, 0.9, p1[1] - 0.9, p1[1] + 0.9, solid(P, "steel_dark"), cut=1)
        m.box(ab, min(sx * 1.0, sx * 6.0), 2.0, -3.2, max(sx * 1.0, sx * 6.0), 8.4, 3.2, CLAW,
              rotation=(0, 0, sx * 12), pivot=(sx * 4.0, 8.0, 0))                        # claw halves
    for i, (dx, dy, key) in enumerate(((-1.6, 4.0, "egg1"), (1.4, 4.4, "egg2"), (0, 6.6, "egg3"),
                                       (-0.4, 2.4, "egg2"), (1.8, 6.8, "egg1"))):
        ball(m, bd, (dx, dy, -1.0 + (i % 2) * 2.0), 1.4, solid(P, key), layers=2)
    return m
