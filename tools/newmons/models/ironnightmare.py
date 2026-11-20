"""Iron Nightmare (Dark/Electric), the future paradox Darkrai, built from boxes after the art the user shared (artist
and name not given; our name).

A robot Darkrai of black metal: a bell-shaped lower body seamed in grey, a slim waist, a chest set with a collar of red
points tipped in yellow, and round black shoulder joints sprouting antennae that end in balls. Its long thin arms are
jointed with red lights and end in long hooked claws. Its head is a white helmet in a red hood with one yellow eye, and
yellow lightning crackles over it: a great bolt above its head, sparks at its hands and a burst beneath it.

Shiny: white metal with a blue hood and blue lightning.

Front is -z, y is up. 48 units tall (to the bolt); about 2.6 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _pgen1 import CLEAR
from _regi import ellipsoid, lit
from _rotomform import bolt_shape
from _route import mix, pal, tone

HEIGHT = 48
SCALE = round(2.6 * 16 / HEIGHT, 3)
HITBOX = [1.4, 34 / 16]
KIND = "floater"
K = 3
LOOK = ("a black robot Darkrai with a bell-shaped body, ball-tipped shoulder antennae, long clawed arms with red joint "
        "lights, a white helmet in a red hood and yellow lightning crackling over it")

BASE = {"black": (36, 34, 42), "black_light": (70, 68, 80), "seam": (100, 98, 110), "red": (196, 46, 40),
        "yellow": (250, 214, 60), "white": (238, 238, 244), "white_dark": (190, 190, 204), "eye": (240, 220, 80),
        "bolt": (255, 224, 70), "bolt_light": (255, 250, 190)}
SHINY = {"black": (210, 212, 222), "black_light": (240, 242, 248), "seam": (150, 152, 166), "red": (60, 110, 220),
         "bolt": (110, 200, 255), "bolt_light": (220, 244, 255)}


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def metalf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up":
        return p["black_light"], None
    return lit(p["black"], face, y, 18, 10), None


def skirtf(x, y, z, face, variant, **k):
    """The bell: black, seamed in grey from top to bottom."""
    p = P(variant)
    a = math.degrees(math.atan2(z, x)) % 45
    if face != "up" and face != "down" and a < 4:
        return p["seam"], None
    return metalf(x, y, z, face, variant)


def chestf(x, y, z, face, variant, **k):
    """The chest: a collar of red points tipped in yellow on its front."""
    p = P(variant)
    if face == "north" and 15.0 < y < 20.0:
        u = (x + 6.0) % 2.4 - 1.2
        v = y - 15.0
        if v > abs(u) * 3.0:
            return (p["yellow"] if v < 1.4 else p["red"]), None
    return metalf(x, y, z, face, variant)


def helmetf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and math.hypot(x + 0.8, y - 26.0) < 0.8:
        return p["eye"], p["eye"]
    return lit(p["white"], face, y, 28, 4), None


def boltf(x0, y0, w, h, flip=False):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        u, v = (x - x0) / w, (y - y0) / h
        if flip:
            u = 1 - u
        if not (0 <= u <= 1 and 0 <= v <= 1) or not bolt_shape(u, v):
            return CLEAR
        c = mix(p["bolt"], p["bolt_light"], abs(u - 0.5))
        return c, c
    return s


def burstf(x, y, z, face, variant, **k):
    """A jagged burst of lightning beneath it (an xy plane)."""
    p = P(variant)
    a = math.atan2(-(y - 4.0), x)
    r = math.hypot(x, y - 4.0)
    if y > 4.0:
        return CLEAR
    n = 9
    f = (a / math.pi * n) % 1.0
    R = 3.0 + 5.0 * (1 - abs(2 * f - 1)) ** 2
    if r < R:
        c = p["bolt_light"] if r < R * 0.5 else p["bolt"]
        return c, c
    return CLEAR


def build() -> Model:
    m = Model("ironnightmare")
    top = m.bone("ironnightmare", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14.0, 0))
    for i, (y0, r) in enumerate(((4.0, 5.6), (6.0, 5.2), (8.0, 4.6), (10.0, 3.8), (12.0, 2.8))):
        m.round_box(bd, 0, 0.0, r, r, y0, y0 + 2.0, skirtf, cut=max(1, round(r * 0.35)))   # the bell
    m.round_box(bd, 0, 0.0, 1.8, 1.8, 13.6, 15.0, solid("seam"), cut=0.5)            # slim waist
    ellipsoid(m, bd, 0, 18.4, 0.0, 5.4, 4.4, 3.8, chestf, step=1)                     # chest
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):
        ellipsoid(m, bd, sx * 7.0, 20.0, 0.0, 3.6, 3.6, 3.6, metalf, step=1)          # round shoulder joints
        rod(m, bd, (sx * 8.6, 22.6, 0.0), (sx * 13.0, 27.4, 0.0), 1.2, metalf, extend=0.3)   # antennae
        ellipsoid(m, bd, sx * 13.4, 27.8, 0.0, 1.8, 1.8, 1.8, metalf, step=1)
        ar = m.bone(nm, bd, (sx * 6.0, 18.0, 0.0))
        sh, el, hand = (sx * 7.6, 17.0, 0.0), (sx * 10.4, 10.6, -2.0), (sx * 11.4, 5.0, -4.0)
        rod(m, ar, sh, el, 2.0, metalf, extend=0.4)
        ellipsoid(m, ar, el[0], el[1], el[2], 1.2, 1.2, 1.2, solid("red", True), step=1)
        rod(m, ar, el, hand, 1.4, metalf, extend=0.4)
        for c in (-1, 0, 1):                                                     # long hooked claws
            a = (hand[0] + c * 0.6, hand[1], hand[2])
            b = (hand[0] + c * 1.0 + sx * 0.6, hand[1] - 3.4, hand[2] - 1.4)
            e = (hand[0] + c * 1.2 + sx * 0.2, hand[1] - 5.6, hand[2] + 0.4)
            rod(m, ar, a, b, 0.8, metalf, extend=0.3)
            rod(m, ar, b, e, 0.7, metalf, extend=0.3)
        x0 = sx * 11.4 - 3.0
        m.box(ar, x0, 6.0, -4.6, x0 + 6.0, 12.0, -4.6, boltf(x0, 6.0, 6.0, 6.0, sx < 0))   # sparks at its hands
    hd = m.bone("head", bd, (0, 22.0, 0.0))
    m.round_box(hd, 0, 1.0, 3.6, 3.0, 22.0, 31.0, solid("red"), cut=1)                # the red hood
    m.round_box(hd, 0, -0.6, 2.6, 2.6, 22.6, 31.6, helmetf, cut=1)                   # the white helmet
    spike(m, hd, (0, 30.4, -1.4), (0, 0.5, -1), 3.4, 5.0, helmetf, tip=1.6)           # the helmet's forward point
    m.box(hd, -6.0, 31.0, 1.4, 4.0, 48.0, 1.4, boltf(-6.0, 31.0, 10.0, 17.0))        # the great bolt above
    m.box(bd, -8.0, 0.0, 0.0, 8.0, 4.0, 0.0, burstf)                                # the burst beneath
    return m
