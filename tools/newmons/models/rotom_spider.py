"""Spider Rotom (Electric/Bug), after the user's Rotom doodle sheet (artist not named): Rotom inside a robot spider.
A round orange body with two big teal lens eyes like goggles and a little open mouth, eight long black legs banded in
grey, and a web of glowing green wire spun behind it.

Front is -z, y is up. 16 units tall; about 0.8 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _rotomform import ball, face_on, palette, solid

P = palette({"aura": (90, 210, 110), "aura_light": (200, 255, 210), "iris": (90, 220, 210)})
HEIGHT = 16
SCALE = round(0.8 * 16 / HEIGHT, 3)
HITBOX = [1.0, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "a round orange robot spider with big teal goggle eyes, eight banded legs and a glowing green wire web"


def leg(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone_band(p, z, box), None


def tone_band(p, z, box):
    from _route import tone as _t
    t = (box.lo[2] + box.size[2] - z) / max(1, box.size[2])
    return p["grey"] if int(t * 4) % 2 else p["black"]


def web(x, y, z, face, variant, **k):
    p = P(variant)
    a = math.atan2(y - 9, x)
    d = math.hypot(x, y - 9)
    spoke = abs(math.sin(a * 4)) < 0.08 * (8 / max(d, 1))
    ring = abs((d % 2.4) - 1.2) < 0.18
    if d < 9 and (spoke or ring):
        return p["aura"], p["aura"]
    return (0, 0, 0, 0)


def build() -> Model:
    m = Model("rotom_spider")
    top = m.bone("rotom_spider", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.box(bd, -9, 0, 3, 9, 18, 3, web)                                               # the glowing wire web
    hd = m.bone("head", bd, (0, 8, 0))
    ball(m, hd, 0, 8, 0, 4.4, face_on(P, (0, 8, -4.4), eyes=[(-1.7, 0.6, 1.6), (1.7, 0.6, 1.6)],
                                       mouth=(0, -2.0, 1.4, 1.0, 2)))               # the round body (its face)
    for sx in (-1, 1):
        for i, zz in enumerate((-2.5, -0.8, 0.8, 2.5)):                              # eight banded legs
            knee = (6.5 * sx, 11 - abs(i - 1.5) * 0.6, zz * 1.6)
            rod(m, bd, (3.5 * sx, 8, zz), knee, 0.9, leg, extend=0.3)
            rod(m, bd, knee, (9 * sx, 1, zz * 2.0), 0.9, leg, extend=0.3)
    return m
