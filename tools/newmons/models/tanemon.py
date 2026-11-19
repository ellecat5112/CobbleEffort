"""Tanemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a round green bulb with a cream face, big glossy red eyes and pink cheeks, a cat mouth, two
ragged leaves sprouting from its top and little root feet. 0.5 blocks.

Front is -z, y is up. Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _digi import sized
from _digibeast import ball
from _digidetail import cutout, eye, plane, skin, solid
from _route import pal, tone

HEIGHT = 22
SCALE, HITBOX = sized(0.5, HEIGHT, 1.0)
KIND = "biped"
K = 4
LOOK = "a round green bulb with a cream face, big red eyes, two ragged leaves on top and little root feet"
BASE = {"green": (120, 190, 60), "green_dark": (60, 120, 30), "cream": (250, 244, 220), "eye": (150, 20, 20),
        "pupil": (40, 6, 6), "white": (255, 255, 255), "pink": (250, 170, 180), "leaf": (90, 170, 50),
        "leaf_dark": (30, 90, 20), "root": (230, 200, 140), "black": (30, 30, 30)}
SHINY = {"green": (230, 190, 60), "green_dark": (170, 120, 20), "leaf": (230, 140, 40), "leaf_dark": (150, 70, 10)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    # cream face: the lower front half
    if z < -1.0 and y < 9.0 - 0.15 * x * x / 4:
        if face == "north":
            a, b = plane(x, y, z, face)
            for sx in (-1, 1):
                c = eye(p, a - sx * 2.6, b - 6.4, 1.6, "eye")
                if c is not None:
                    return c, None
                if math.hypot(a - sx * 4.4, b - 4.4) < 0.9:
                    return p["pink"], None
            if abs(b - 4.0) < 0.3 and abs(a) < 1.0:
                return p["black"], None
        return tone(p["cream"], face), None
    return skin(P, "green", dark="green_dark")(x, y, z, face, variant, box=box, **k)


def leaf_in(x, y, z, face, box):
    if box is None:
        return True
    t = (y - box.lo[1]) / max(box.size[1], 1e-6)
    w = math.sin(min(1.0, t) * math.pi) * 0.5 + 0.08
    u = (x - box.lo[0]) / max(box.size[0], 1e-6) - 0.5
    rag = 0.06 * math.sin(t * 22.0)
    return abs(u) < w + rag


def build():
    m = Model("tanemon")
    top = m.bone("tanemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 7.0, 0), 6.4, bodyf, layers=6, squash=0.9)
    rod(m, bd, (0, 12.4, 0), (0, 15.0, 0), 2, skin(P, "green", dark="green_dark"), extend=0.3)
    lv = m.bone("leaves", bd, (0, 15, 0))
    for sx in (-1, 1):
        m.box(lv, sx * 1.0 - 2.6, 14.6, -0.2, sx * 1.0 + 2.6, 22.0, 0.2,
              cutout(leaf_in, skin(P, "leaf", dark="leaf_dark")), rotation=(0, 0, -sx * 40), pivot=(0, 14.6, 0))
    for i in range(4):
        ang = i * math.pi / 2 + math.pi / 4
        m.box(bd, 3.6 * math.cos(ang) - 0.8, 0.0, 3.6 * math.sin(ang) - 0.8, 3.6 * math.cos(ang) + 0.8, 1.4,
              3.6 * math.sin(ang) + 0.8, solid(P, "root"))
    return m
