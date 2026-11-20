"""Iron Deluge (Water/Electric), the future paradox Kyogre, built from boxes after the art the user shared (signed but
the artist not named, no name given; our name).

A robot Kyogre of deep navy traced with glowing pink circuit rings: two pink-ringed ports glow on its front, its
great pectoral fins carry pink rings with three lines running to their white, black-banded tips, and a translucent
blue bubble swells beneath it around a pink core. From its back rises a black mechanical neck, ribbed in segments,
that curls forward to a black ball of a head with a pink pixel eye and an orange collar ring, crackling with pink
and blue lightning from its crown.

Shiny: white plating with cyan circuits.

Front is -z, y is up. 31 units tall (to the lightning); about 3.0 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _kyogre import CY, FIN_LEN, FIN_W, body, dorsal, fin_box, fluke
from _pgen1 import CLEAR, smooth_path, stars
from _regi import ellipsoid, lit
from _rotomform import bolt_shape
from _route import mix, pal, tone

HEIGHT = 31
SCALE = round(3.0 * 16 / HEIGHT, 3)
HITBOX = [3.2, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = ("a navy robot Kyogre traced with glowing pink circuit rings, white-tipped fins, a translucent bubble belly and "
        "a black mechanical neck curling up to a ball head with a pink pixel eye and crackling lightning")

BASE = {"navy": (30, 52, 116), "navy_light": (60, 92, 168), "navy_dark": (18, 30, 72), "pink": (246, 90, 160),
        "pink_light": (255, 190, 220), "white": (236, 238, 244), "black": (30, 30, 36), "black_light": (66, 66, 74),
        "bubble": (196, 230, 250, 150), "orange": (240, 150, 50), "blue_bolt": (150, 210, 255), "star": (255, 255, 255)}
SHINY = {"navy": (214, 220, 232), "navy_light": (240, 244, 250), "navy_dark": (160, 168, 186), "pink": (60, 220, 250),
         "pink_light": (190, 246, 255)}


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def hullf(x, y, z, face, variant, **k):
    """Deep navy; two pink-ringed ports on its front and pink circuit lines along its back."""
    p = P(variant)
    if face == "north" and z < -6:
        for sx in (-1, 1):
            r = math.hypot(x - sx * 3.4, y - (CY + 1.6))
            if r < 1.0:
                return p["pink"], p["pink"]
            if r < 1.6:
                return p["pink_light"], p["pink_light"]
    if face == "up" and abs(abs(x) - 2.6) < 0.35:
        return p["pink"], p["pink"]
    return lit(p["navy"], face, y, CY, 6), None


def finf(sx):
    """A pectoral fin: navy with a glowing pink ring and three lines to its white tip, banded black at the tip."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u = sx * (x - sx * 6.0)
        w = z - (box.lo[2] + box.size[2] / 2)
        if u > FIN_LEN - 2.6:
            if abs(w) % 3.0 < 0.4:
                return tone(p["black"], face), None
            return tone(p["white"], face), None
        if face in ("up", "down"):
            r = math.hypot(u - 4.6, w)
            if abs(r - 2.4) < 0.4:
                return p["pink"], p["pink"]
            if r > 2.4 and u > 4.6 and min(abs(w), abs(w - (u - 4.6) * 0.9), abs(w + (u - 4.6) * 0.9)) < 0.35:
                return p["pink"], p["pink"]
        return tone(p["navy"] if face != "down" else p["navy_dark"], face), None
    return s


def bubblef(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and math.hypot(x - 1.2, y - 4.0) < 2.6:
        return p["pink"], p["pink"]
    if stars(x, y, z, face, cell=1.6, r=0.25, prob=0.25):
        return p["star"] + (200,), p["star"]
    return p["bubble"], None


def neckf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    d = box.lo[2] + box.size[2] - z
    if (d % 2.4) < 0.4:
        return tone(p["black"], face), None
    return tone(p["black_light"] if face == "up" else p["black"], face), None


def headf(x, y, z, face, variant, **k):
    """A black ball with a pink pixel eye ringed in darker pink on each side."""
    p = P(variant)
    if face in ("east", "west", "north"):
        a = z if face != "north" else x
        r = math.hypot(a - (-1.0 if face != "north" else 0.0), y - 24.6)
        if face != "north" and r < 1.6:
            if ((y * 3) % 1.0 < 0.5) ^ ((a * 3) % 1.0 < 0.5):
                return p["pink"], p["pink"]
            return p["pink_light"], p["pink_light"]
    return lit(p["black"], face, y, 24, 2.4), None


def boltf(w, h, x0, y0, flip=False):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        u, v = (x - x0) / w, (y - y0) / h
        if flip:
            u = 1 - u
        if not (0 <= u <= 1 and 0 <= v <= 1) or not bolt_shape(u, v):
            return CLEAR
        c = mix(p["pink"], p["blue_bolt"], v)
        return c, c
    return s


def build() -> Model:
    m = Model("irondeluge")
    top = m.bone("irondeluge", None, (0, 0, 0))
    bd = m.bone("body", top, (0, CY, 0))
    body(m, bd, hullf)
    dorsal(m, bd, solid("navy_dark"))
    ellipsoid(m, bd, 0, 4.4, -2.0, 4.6, 3.4, 5.0, bubblef, step=1)                  # translucent bubble belly
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):
        fn = m.bone(nm, bd, (sx * 6.0, 8.0, -1.0))
        fin_box(m, fn, sx, finf(sx), thick=2.4)
    tl = m.bone("tail", bd, (0, CY, 11.0))
    fluke(m, tl, solid("navy_dark"))
    nk = m.bone("neck", bd, (0, CY + 5.0, 5.0))                                     # the black mechanical neck
    path = smooth_path([(0, CY + 5.0, 6.0), (0, CY + 10.0, 7.0), (0, CY + 14.0, 4.0), (0, CY + 15.0, 0.0)], 8)
    for a, b in zip(path, path[1:]):
        rod(m, nk, a, b, 3.0, neckf, extend=0.6)
    hd = m.bone("head", nk, (0, 24.0, -1.0))
    ellipsoid(m, hd, 0, 24.4, -1.0, 2.8, 2.8, 2.8, headf, step=1)                   # black ball head
    m.round_box(hd, 0, -3.2, 1.8, 1.0, 22.6, 23.8, solid("orange"), cut=0.5)       # orange collar ring / beak
    for x0, fl in ((-7.0, False), (-1.0, True)):                                   # lightning from its crown
        m.box(hd, x0, 26.6, -1.0, x0 + 8.0, 31.0, -1.0, boltf(8.0, 4.4, x0, 26.6, fl))
    return m
