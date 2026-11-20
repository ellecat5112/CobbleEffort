"""Eternal Wings (Fairy/Psychic), the ancient paradox Latias, built from boxes after Glowing_Shark's art (the art's
own name).

A feathered Latias of deep violet and white. Two huge wings spread up and out from its shoulders, violet coverts in
scalloped rows giving way to long white flight feathers, each marked near its tip with a pale mint eye-spot; a
smaller fan of the same feathers sweeps down below it as a tail. Its head carries a glowing blue glass visor over an
amber eye, with white feathered ears swept back, and its body is violet above and white below, banded with violet
chevrons.

Shiny: rose and white with gold eye-spots.

Front is -z, y is up. 47 units tall (wings up); about 2.6 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _pgen1 import CLEAR
from _regi import ellipsoid, lit
from _route import mix, pal, tone

HEIGHT = 47
SCALE = round(2.6 * 16 / HEIGHT, 3)
HITBOX = [1.6, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = ("a feathered violet and white Latias with huge wings of scalloped violet coverts and white eye-spotted flight "
        "feathers, a feather fan of a tail and a glowing blue visor over its eye")

BASE = {"violet": (112, 62, 196), "violet_dark": (74, 36, 140), "violet_light": (150, 104, 224), "white": (236, 238, 246),
        "white_dark": (196, 200, 220), "mint": (196, 246, 224), "visor": (70, 180, 255), "visor_light": (180, 236, 255),
        "eye": (250, 176, 40), "pupil": (40, 20, 30), "line": (60, 40, 110)}
SHINY = {"violet": (220, 84, 120), "violet_dark": (160, 50, 84), "violet_light": (246, 140, 170), "mint": (250, 220, 120)}
CY = 20.0


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def bodyf(x, y, z, face, variant, **k):
    """Violet above, white below in front, banded with violet chevrons."""
    p = P(variant)
    if face == "north" or (face in ("east", "west") and z < -1.5):
        ch = (y + abs(x) * 0.7) % 3.0
        if y < 25.0 and ch > 0.5:
            return lit(p["white"], face, y, CY, 7), None
    return lit(p["violet"], face, y, CY, 7), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west", "north") and y > 30.4 and z < -2.0:
        return p["visor"], p["visor"]
    if face in ("east", "west") and math.hypot(z + 3.4, y - 29.6) < 0.6:
        return p["eye"], None
    if y < 29.0:
        return lit(p["white"], face, y, 30, 3), None
    return lit(p["violet"], face, y, 30, 3), None


def fanf(cx, cy, a0, a1, n, rmax, rmin=3.0, side=1):
    """A fan of n long feathers from (cx, cy) between angles a0..a1 (degrees from +x*side, counter-clockwise), on an xy
    plane: violet scalloped coverts near the root, long white flight feathers with mint eye-spots near their tips."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        dx, dy = side * (x - cx), y - cy
        r = math.hypot(dx, dy)
        if r < rmin * 0.5:
            return CLEAR
        a = math.degrees(math.atan2(dy, dx))
        if not (a0 - 4 <= a <= a1 + 4):
            return CLEAR
        f = (a - a0) / (a1 - a0) * n
        i = math.floor(f)
        off = f - i - 0.5                                                   # -0.5..0.5 across a feather
        R = rmax * (0.72 + 0.28 * math.sin(math.pi * min(1.0, max(0.0, (i + 0.5) / n)))) * (1 - 0.45 * off * off)
        if r > R:
            return CLEAR
        if abs(off) > 0.47:
            return p["line"], None                                          # the line between feathers
        t = r / R
        if t < 0.5:
            row = (r + abs(off) * 3.0) % 2.4
            return (p["violet_dark"] if row < 0.4 else p["violet"]), None      # scalloped coverts
        if abs(t - 0.82) < 0.08 and abs(off) < 0.22:
            return p["mint"], None                                          # eye-spot
        return mix(p["white"], p["white_dark"], max(0.0, t - 0.9) * 4), None
    return s


def build() -> Model:
    m = Model("eternalwings")
    top = m.bone("eternalwings", None, (0, 0, 0))
    bd = m.bone("body", top, (0, CY, 0))
    ellipsoid(m, bd, 0, CY, 0.4, 4.2, 7.0, 4.4, bodyf, step=1)                   # the body
    hd = m.bone("head", bd, (0, 27.0, -1.0))
    ellipsoid(m, hd, 0, 30.0, -1.6, 3.0, 3.0, 3.6, headf, step=1)                # head
    m.round_box(hd, 0, -5.0, 1.6, 1.6, 28.2, 30.6, solid("white"), cut=0.6)       # snout
    for sx in (-1, 1):                                                           # white feathered ears
        rod(m, hd, (sx * 2.0, 31.6, 0.0), (sx * 3.4, 33.8, 3.6), 1.6, solid("white"), extend=0.4, t2=1.0)
        spike(m, hd, (sx * 3.4, 33.6, 3.4), (sx * 0.3, 0.3, 1), 1.2, 2.4, solid("violet"), tip=0.5)
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):                          # small folded arms
        ar = m.bone(nm, bd, (sx * 3.6, 23.0, -2.0))
        rod(m, ar, (sx * 3.6, 23.0, -2.0), (sx * 4.2, 19.6, -4.0), 1.6, solid("white"), extend=0.4)
        rod(m, ar, (sx * 4.2, 19.6, -4.0), (sx * 2.6, 18.4, -5.0), 1.4, solid("white"), extend=0.3)
    for nm, sx in (("wing_left", 1), ("wing_right", -1)):                        # huge feathered wings
        wg = m.bone(nm, bd, (sx * 4.0, 24.0, 1.4))
        x0, x1 = sorted((sx * 2.5, sx * 30.0))
        m.box(wg, x0, 18.0, 1.6, x1, 47.0, 1.6, fanf(sx * 4.0, 24.0, 8, 98, 10, 23.0, side=sx))
        ellipsoid(m, wg, sx * 5.4, 25.0, 1.4, 2.0, 2.0, 1.6, solid("violet"), step=1)   # wing root
    tl = m.bone("tail", bd, (0, 14.0, 1.6))                                       # a feather fan of a tail
    m.box(tl, -14.0, 0.0, 2.6, 14.0, 15.0, 2.6, fanf(0.0, 14.5, -128, -52, 7, 14.0))
    return m
