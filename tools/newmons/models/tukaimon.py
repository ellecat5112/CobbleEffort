"""Tukaimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little bat familiar: a plump purple-backed body with a white belly, round yellow eyes set low on its
face, two enormous wing-ears with ragged lilac edges sweeping up and back, and stubby dark feet. 1 block.

Front is -z, y is up. Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import cutout, eye, plane, skin, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(1.0, HEIGHT, 2.0)
KIND = "floater"
K = 4
LOOK = "a little purple bat familiar with a white belly, round yellow eyes and two enormous ragged wing-ears"
BASE = {"purple": (110, 60, 150), "purple_dark": (60, 24, 100), "lilac": (190, 150, 220), "white": (246, 246, 250),
        "eye": (250, 220, 60), "pupil": (20, 20, 20), "foot": (60, 60, 70)}
SHINY = {"purple": (60, 110, 160), "purple_dark": (24, 60, 110), "lilac": (150, 200, 230)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if y < 6.4 + 0.25 * z:
        if face == "north":
            a, b = plane(x, y, z, face)
            for sx in (-1, 1):
                c = eye(p, a - sx * 2.6, b - 6.0, 1.1, "eye")
                if c is not None:
                    return c, None
        return tone(p["white"], face), None
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            c = eye(p, a - sx * 2.6, b - 6.0, 1.1, "eye")
            if c is not None:
                return c, None
    return skin(P, "purple", dark="purple_dark")(x, y, z, face, variant, box=box, **k)


def ear_in(x, y, z, face, box):
    if box is None:
        return True
    u = (y - box.lo[1]) / max(box.size[1], 1e-6)
    v = (abs(x) - min(abs(box.lo[0]), abs(box.lo[0] + box.size[0]))) / max(box.size[0], 1e-6)
    return v < 1.0 - u * 0.85 + 0.08 * math.sin(u * 18.0)


def earf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if box is not None and (y - box.lo[1]) / max(box.size[1], 1e-6) > 0.7:
        return tone(p["lilac"], face), None
    return skin(P, "purple", dark="purple_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("tukaimon")
    top = m.bone("tukaimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 7.0, 0), 5.6, bodyf, layers=5, squash=0.85, ry=5.0)
    for sx in (-1, 1):
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 2.0, 10.0, 0))
        x0, x1 = sorted((sx * 1.0, sx * 8.0))
        m.box(wb, x0, 10.0, -0.3, x1, 24.0, 0.3, cutout(ear_in, earf), rotation=(-15, 0, -sx * 28),
              pivot=(sx * 1.0, 10.0, 0))
    for sx in (-1, 1):
        m.round_box(top, sx * 2.4, -0.6, 0.9, 1.2, 0.0, 2.6, solid(P, "foot"), cut=0)
    return m
