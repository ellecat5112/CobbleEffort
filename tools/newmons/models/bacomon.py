"""Bacomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a cardboard-box Digimon. A box head with open flaps on top, one red eye peering out and a torn
second eye-hole, a box body with a tape strip and a little label, box arms (one holding a roll of tape) and box legs.
1 block tall.

Front is -z, y is up. 32 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _digi import sized
from _digidetail import eye, local, mix, plane, solid
from _route import pal, tone

HEIGHT = 32
SCALE, HITBOX = sized(1.0, HEIGHT, 0.8)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 18}
LOOK = ("a cardboard-box Digimon: a box head with open flaps, one red eye and a torn eye-hole, a taped box body, box "
        "arms and legs and a roll of tape")
BASE = {"card": (220, 180, 100), "card_dark": (160, 120, 60), "card_light": (240, 210, 140), "tape": (200, 170, 110),
        "eye": (230, 50, 50), "pupil": (20, 10, 10), "white": (250, 250, 250), "hole": (40, 30, 20),
        "label": (240, 240, 236), "red": (200, 40, 40)}
SHINY = {"card": (150, 160, 170), "card_dark": (90, 100, 110), "card_light": (200, 210, 220), "eye": (60, 180, 255)}


def P(v):
    return pal(BASE, SHINY, v)


def cardf(x, y, z, face, variant, box=None, **k):
    """Corrugated cardboard: faint flute lines, darker folded edges."""
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if min(u, W - u, v, H - v) < 0.3:
        return tone(p["card_dark"], face), None
    a, b = plane(x, y, z, face)
    c = p["card_light"] if (a * 2.0) % 1.0 < 0.15 else p["card"]
    return tone(c, face), None


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        c = eye(p, x + 2.0, y - 23.0, 1.6, "eye")
        if c is not None:
            return c, None
        if math.hypot(x - 2.2, y - 22.6) < 1.6 + 0.3 * math.sin(math.atan2(y - 22.6, x - 2.2) * 5):
            return p["hole"], None
    return cardf(x, y, z, face, variant, box=box, **k)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if abs(x) < 0.8:
            return tone(p["tape"], face), None
        if 1.4 < x < 3.4 and 12.0 < y < 13.6:
            return p["label"] if y > 12.4 else p["red"], None
    return cardf(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("bacomon")
    top = m.bone("bacomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.box(bd, -4.0, 8.0, -3.4, 4.0, 17.0, 3.4, bodyf)
    hd = m.bone("head", bd, (0, 17, 0))
    m.box(hd, -5.6, 17.0, -5.0, 5.6, 27.0, 5.0, headf)
    for sx in (-1, 1):                                           # open flaps on top
        m.box(hd, min(sx * 5.6, sx * 9.0), 27.0, -5.0, max(sx * 5.6, sx * 9.0), 27.0, 5.0, cardf,
              rotation=(0, 0, sx * 35), pivot=(sx * 5.6, 27.0, 0))
    m.box(hd, -5.6, 27.0, -5.0, 5.6, 27.0, -8.0, cardf, rotation=(-40, 0, 0), pivot=(0, 27.0, -5.0))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.0, 15.0, 0))
        m.box(ab, min(sx * 4.0, sx * 11.0), 13.6, -1.4, max(sx * 4.0, sx * 11.0), 16.0, 1.4, cardf)
        m.box(ab, min(sx * 10.0, sx * 11.6), 12.0, -1.6, max(sx * 10.0, sx * 11.6), 17.6, 1.6, cardf)
    for i in range(8):                                           # roll of tape in its right hand
        ang = math.radians(i * 45)
        c = (-13.0, 15.0 + 2.0 * math.sin(ang), 2.0 * math.cos(ang))
        m.box("arm_right", c[0] - 1.0, c[1] - 0.6, c[2] - 0.6, c[0] + 1.0, c[1] + 0.6, c[2] + 0.6, solid(P, "tape"),
              rotation=(i * 45, 0, 0), pivot=c)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.0, 8.0, 0))
        m.box(lg, sx * 2.2 - 1.6, 2.0, -1.6, sx * 2.2 + 1.6, 8.0, 1.6, cardf)
        m.box(lg, sx * 2.2 - 2.2, 0.0, -3.0, sx * 2.2 + 2.2, 2.4, 2.0, cardf)
    return m
