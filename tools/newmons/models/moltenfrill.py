"""Molten Frill (Fire/Dark), the ancient paradox Moltres, built from boxes after the art the user shared (the art's
own name; artist not named).

An upright crested theropod: a crimson head with a twin ridged crest of gold, a gaping mouth and a yellow eye, and
round its neck a huge frill of glowing orange, streaked from the neck outwards and edged in wavy flame-yellow. Its
body and thighs are a warm cream striped with crimson flame marks, a crimson stripe runs down its throat and belly,
its little arms and long legs are crimson with white claws, and its long tail sweeps back and up under a jagged crest
of flame.

Shiny: blue-violet fire and a deep blue head.

Front is -z, y is up. 46 units tall; about 2.2 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digidetail import scales, solid as dsolid
from _pgen1 import CLEAR, ribbon, smooth_path, tri
from _regi import ellipsoid
from _route import mix, pal, tone

HEIGHT = 46
SCALE = round(2.2 * 16 / HEIGHT, 3)
HITBOX = [1.6, HEIGHT / 16]
KIND = "biped"
K = 3
LOOK = ("an upright crested theropod with a crimson gaping head, a huge glowing orange neck frill edged in flame, a "
        "cream body with crimson flame stripes and a long tail under a crest of fire")

BASE = {"cream": (238, 196, 118), "cream_dark": (206, 156, 86), "crimson": (204, 30, 72), "crimson_dark": (150, 18,
                                                                                                          50),
        "frill": (244, 122, 82), "frill_dark": (210, 82, 58), "frill_light": (252, 176, 112), "flame": (254, 214, 120),
        "stripe": (214, 40, 66), "white": (244, 244, 246), "mouth": (96, 32, 44), "tongue": (232, 132, 146),
        "eye": (250, 230, 90), "pupil": (40, 20, 20), "crest": (246, 190, 84), "crest_dark": (214, 140, 50)}
SHINY = {"cream": (226, 218, 242), "cream_dark": (184, 172, 214), "crimson": (44, 62, 176), "crimson_dark": (26, 38,
                                                                                                           122),
         "frill": (150, 96, 232), "frill_dark": (108, 62, 190), "frill_light": (196, 150, 250), "flame": (176, 226, 255),
         "stripe": (70, 90, 210), "crest": (120, 200, 250), "crest_dark": (70, 140, 210)}
NECK = (0, 33.0, -3.2)


def P(v):
    return pal(BASE, SHINY, v)


LEGS = scales(P, "crimson", "crimson_dark", size=1.0, rim_mix=0.45)


def solid(key):
    def s(x, y, z, face, variant, **k):
        return tone(P(variant)[key], face), None
    return s


def creamf(x, y, z, face, variant, **k):
    """Cream with crimson flame stripes on the sides and a crimson stripe down the front."""
    p = P(variant)
    if face == "north" and abs(x) < 1.7 and y > 17:
        return tone(p["crimson"], face), None
    if face in ("east", "west", "up"):
        ph = (y * 0.55 + z * 0.35) % 3.0
        if ph < 0.35 and (int(y * 0.7 + z * 0.2) % 3) != 0:
            return tone(p["stripe"], face), None
    if face == "north" and abs(x) < 2.6 and y > 17:
        return tone(mix(p["cream"], p["crimson"], 0.2), face), None
    return tone(p["cream"] if face != "down" else p["cream_dark"], face), None


def neckf(x, y, z, face, variant, **k):
    """The neck rods (upright: their "down" face looks forward): cream, a crimson stripe down the throat."""
    p = P(variant)
    if face == "down":
        return tone(p["crimson"] if abs(x) < 1.3 else p["cream"], "north"), None
    return tone(p["cream"], face if face != "up" else "south"), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        r = math.hypot(z - (-5.0), y - 38.7)
        if r < 0.35:
            return p["pupil"], None
        if r < 0.7:
            return p["eye"], None
    return tone(p["crimson"], face), None


def crestf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and (z % 1.1) < 0.35:
        return tone(p["crest_dark"], face), None
    return tone(p["crest"], face), None


def frillf(side, cx, cy):
    """One half of the frill, a fan beside the neck: radial streaks, a lighter base and a wavy flame-yellow edge."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        dx, dy = side * (x - cx), y - cy
        if dx < -0.5:
            return CLEAR
        a = math.atan2(dy, max(dx, 0.01))                       # -pi/2 (down) .. pi/2 (up)
        if a < -1.45 or a > 1.55:
            return CLEAR
        R = 11.0 * (0.9 + 0.1 * math.cos(a * 1.2)) + 0.7 * math.sin(a * 16)
        r = math.hypot(dx, dy)
        if r > R:
            return CLEAR
        if R - r < 1.1:
            return p["flame"], p["flame"]
        streak = abs(math.sin(a * 9)) < 0.22 and r > 5.0
        if r < 3.6:
            c = p["frill_light"]
        else:
            c = p["frill_dark"] if streak else p["frill"]
        return c, c
    return s


def tailcrest(pts):
    """A jagged crest of flame standing on the tail (a zy plane): tongues rising from the tail's top line."""
    def top_at(z):
        for (z0, y0), (z1, y1) in zip(pts, pts[1:]):
            if z0 <= z <= z1:
                return y0 + (y1 - y0) * (z - z0) / max(z1 - z0, 0.01)
        return None

    def s(x, y, z, face, variant, **k):
        p = P(variant)
        b = top_at(z)
        if b is None:
            return CLEAR
        h = 3.6 * (0.35 + 0.65 * tri(z / 2.6)) * max(0.0, min(1.0, (z - pts[0][0]) / 6.0))
        if y < b - 0.5 or y > b + h:
            return CLEAR
        f = (y - b) / max(h, 0.01)
        c = p["frill"] if f < 0.45 else p["flame"]
        return c, c
    return s


def build() -> Model:
    m = Model("moltenfrill")
    top = m.bone("moltenfrill", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 22, 1))
    ellipsoid(m, bd, 0, 23.0, 1.0, 4.2, 5.8, 5.4, creamf, step=1)                   # the cream body
    nk = m.bone("neck", bd, (0, 27.5, -2.4))
    neck = smooth_path([(0, 27.0, -2.0), (0, 30.5, -3.4), (0, 34.0, -3.6), (0, 36.0, -3.2)], 5)
    ribbon(m, nk, neck, [3.6, 3.4, 3.2, 3.0, 2.9, 2.8], neckf, extend=1.0)
    for sx in (-1, 1):                                                            # the great frill, two fans
        x0, x1 = sorted((sx * 1.2, sx * 14.0))
        m.box(nk, x0, 21.0, -1.8, x1, 45.0, -1.8, frillf(sx, sx * 1.4, NECK[1]),
              rotation=(0, -sx * 22, 0), pivot=(sx * 1.4, NECK[1], -1.8))
    hd = m.bone("head", nk, (0, 37, -3.4))
    m.round_box(hd, 0, -4.2, 2.3, 2.6, 36.2, 40.2, headf, cut=1)                    # crimson head
    m.box(hd, -1.7, 37.6, -9.8, 1.7, 39.6, -6.2, solid("crimson"))                   # upper jaw
    m.box(hd, -1.3, 37.2, -9.4, 1.3, 37.7, -6.4, solid("mouth"))
    jw = m.bone("jaw", hd, (0, 37.0, -5.8))
    m.box(jw, -1.4, 35.8, -9.0, 1.4, 37.0, -5.8, solid("crimson_dark"), rotation=(26, 0, 0), pivot=(0, 37.0, -5.8))
    m.box(jw, -0.9, 36.8, -8.4, 0.9, 37.2, -6.0, solid("tongue"), rotation=(26, 0, 0), pivot=(0, 37.0, -5.8))
    for sx in (-1, 1):                                                            # twin ridged crests
        x0, x1 = sorted((sx * 0.4, sx * 1.3))
        for z0, z1, h in ((-9.2, -7.0, 1.6), (-7.2, -4.8, 2.8), (-5.0, -2.6, 3.2), (-2.8, -1.0, 2.2)):
            m.box(hd, x0, 39.4, z0, x1, 39.6 + h, z1, crestf)
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):                           # little crimson arms
        ar = m.bone(nm, bd, (sx * 3.2, 26.4, -3.2))
        el, hand = (sx * 4.2, 23.4, -4.6), (sx * 3.6, 22.4, -6.8)
        rod(m, ar, (sx * 3.2, 26.4, -3.2), el, 1.8, LEGS, extend=0.5)
        rod(m, ar, el, hand, 1.5, LEGS, extend=0.4)
        for fx in (-0.5, 0.0, 0.5):
            spike(m, ar, (hand[0] + fx, hand[1], hand[2] - 0.4), (0, -0.6, -1), 0.6, 1.8, solid("white"))
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):
        lg = m.bone(nm, bd, (sx * 2.8, 19.5, 2.0))
        m.round_box(lg, sx * 2.8, 1.8, 2.2, 2.6, 13.6, 21.0, creamf, cut=1)         # striped cream thighs
        knee, ank = (sx * 2.9, 13.4, 0.2), (sx * 3.0, 6.2, 2.8)
        rod(m, lg, (sx * 2.8, 14.6, 1.4), knee, 2.0, LEGS, extend=0.5)
        rod(m, lg, knee, ank, 1.8, LEGS, extend=0.5)
        rod(m, lg, ank, (sx * 3.0, 1.2, 0.6), 1.6, LEGS, extend=0.5)
        m.box(lg, sx * 3.0 - 1.4, 0, -1.0, sx * 3.0 + 1.4, 1.8, 1.8, LEGS)
        for dxx in (-0.5, 0.0, 0.5):
            rod(m, lg, (sx * 3.0 + dxx * 0.8, 0.9, -0.8), (sx * 3.0 + dxx * 2.6, 0.9, -3.4), 1.0, LEGS, extend=0.3)
            spike(m, lg, (sx * 3.0 + dxx * 2.8, 1.0, -3.4), (dxx * 0.3, -0.5, -1), 0.9, 1.8, solid("white"),
                  tip=0.4)
        spike(m, lg, (sx * 3.0, 1.0, 1.8), (0, -0.3, 1), 0.8, 1.6, solid("white"))
    tl = m.bone("tail", bd, (0, 21.5, 6.0))                                       # the long tail, up and back
    path = smooth_path([(0, 21.5, 5.6), (0, 22.0, 12.0), (0, 24.0, 19.0), (0, 27.5, 26.0), (0, 31.5, 32.0),
                        (0, 35.0, 36.5)], 14)
    ribbon(m, tl, path, [4.6 - 3.6 * i / len(path) for i in range(len(path))], creamf, extend=1.0)
    line = [(q[2], q[1] + (4.6 - 3.6 * i / len(path)) / 2 - 0.3) for i, q in enumerate(path)]
    m.box(tl, 0, 20.0, 8.0, 0, 42.0, 37.0, tailcrest(line))
    return m
