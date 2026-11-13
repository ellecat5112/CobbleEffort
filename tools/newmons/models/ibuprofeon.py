"""Ibuprofeon, the Recovery Pokémon (Poison/Normal), a new Eevee evolution after the art by psychedelic-lemur that the
user shared (the art's own name): an Eeveelution that pulled through. A white coat patched with tan bandages (two
across its back, bands round its legs), a pale blue-grey cone of shame round its neck, one red eye and the other
covered by a round eye patch, tall ears with dark red insides, white cheek tufts, and a tail like a blister pack of
pills.

Shiny: a cream coat with a mint cone, pale blue bandages and orange-coated pills.

Front is -z, y is up. 22 units tall to the ear tips; baseScale 0.65 (0.9 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _route import pal, tone

SCALE = 0.65
HITBOX = [1.3, 1.4]
KIND = "quadruped"
K = 5
HEIGHT = 22
LOOK = ("a white Eeveelution with tan bandages, a blue-grey cone of shame, one red eye and an eye patch, dark red ear "
        "insides and a tail like a blister pack of pills")

BASE = {"coat": (246, 244, 240), "coat_shade": (222, 220, 218), "bandage": (226, 196, 160), "bandage_gap": (250, 236, 214),
        "cone": (196, 206, 222), "cone_dark": (150, 162, 184), "inner": (150, 50, 60), "eye": (220, 30, 36),
        "eye_dark": (110, 10, 16), "patch": (252, 252, 252), "patch_line": (110, 110, 120), "nose": (40, 36, 40),
        "blister": (170, 182, 202), "blister_dark": (124, 136, 160), "pill": (214, 224, 240)}
SHINY = {"coat": (250, 240, 218), "coat_shade": (228, 216, 192), "bandage": (170, 206, 236), "bandage_gap": (220, 236, 250),
         "cone": (176, 232, 206), "cone_dark": (120, 190, 160), "pill": (242, 140, 60), "blister": (196, 206, 214),
         "blister_dark": (150, 160, 172)}


def P(v):
    return pal(BASE, SHINY, v)


def coatf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["coat"] if face != "down" else p["coat_shade"], face), None


def bodyf(x, y, z, face, variant, **k):
    """The white coat with two tan bandage patches across its back."""
    p = P(variant)
    if face in ("up", "east", "west") and y > 9.4:
        for z0, z1 in ((-2.6, -0.4), (0.4, 3.0)):
            if z0 < z < z1:
                return tone(p["bandage"], face), None
        if -0.4 <= z <= 0.4:
            return tone(p["bandage_gap"], face), None
    return coatf(x, y, z, face, variant)


def legf(band_y):
    """A leg with a tan bandage band round it at band_y (None for none)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if band_y is not None and abs(y - band_y) < 0.9 and face not in ("up", "down"):
            return tone(p["bandage"], face), None
        return coatf(x, y, z, face, variant)
    return s


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        dx, dy = x - 1.4, y - 14.0                                               # its one red eye
        if (dx / 0.95) ** 2 + (dy / 0.75) ** 2 < 1:
            if dy > 0.3 - 0.35 * dx:
                return p["eye_dark"], None                                       # a tired, half-lidded look
            return (p["eye_dark"] if math.hypot(dx - 0.1, dy + 0.1) < 0.32 else p["eye"]), None
        d = math.hypot(x + 1.4, y - 14.0)                                        # the round eye patch
        if d < 1.3:
            if d > 1.08 or (abs(y - 14.0) < 0.14 and abs(x + 1.4) < 0.75):
                return p["patch_line"], None                                     # its rim and the closed eye
            return p["patch"], None
        if abs(x) < 0.32 and 12.3 < y < 12.8:
            return p["nose"], None
    return coatf(x, y, z, face, variant)


def earf(cx, y0, y1, w):
    """A tall ear on a plane (pre-rotation): cut to a pointed shape, dark red inside on its front."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        t = min(1.0, max(0.0, (y - y0) / (y1 - y0)))
        half = w / 2 * (1 - t) ** 0.7
        if abs(x - cx) > half:
            return (0, 0, 0, 0), None
        if face == "north" and abs(x - cx) < half * 0.62 and 0.06 < t < 0.88:
            return p["inner"], None
        return tone(p["coat"], face), None
    return s


def conef(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["cone"] if face in ("north", "up") else p["cone_dark"], face), None


def blisterf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["blister"] if face in ("up", "east", "west") else p["blister_dark"], face), None


def pillf(x, y, z, face, variant, **k):
    return tone(P(variant)["pill"], face), None


def build() -> Model:
    m = Model("ibuprofeon")
    top = m.bone("ibuprofeon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 9, 0))
    m.round_box(bd, 0, 0.6, 2.8, 5.8, 7.0, 11.6, bodyf, cut=1.2)                  # body with bandages on its back
    m.round_box(bd, 0, -4.4, 2.5, 2.0, 8.4, 12.6, coatf, cut=0.9)                 # chest and neck
    # the tail: a long flat blister pack of pills
    tl = m.bone("tail", bd, (0, 10.6, 6.2))
    pts = [(0, 10.6, 6.0), (0, 9.4, 9.4), (0, 7.8, 12.8), (0, 6.4, 16.0)]
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, a, b, 4.4 - i * 0.7, blisterf, extend=0.4, t2=1.0)          # the flat pack, tapering
        mid = tuple((u + v) / 2 for u, v in zip(a, b))
        rod(m, tl, (mid[0], mid[1] + 0.7, mid[2] - 0.8), (mid[0], mid[1] + 0.4, mid[2] + 0.8), 1.8 - i * 0.3, pillf,
            extend=0, t2=1.0)                                                    # a pill in its bubble
    hd = m.bone("head", bd, (0, 12.4, -4.8))
    m.round_box(hd, 0, -5.2, 2.9, 2.6, 11.0, 16.2, headf, cut=1.1)                # head
    m.round_box(hd, 0, -8.0, 1.3, 0.8, 11.4, 13.2, coatf, cut=0.4)                 # muzzle
    for sx in (-1, 1):
        cx = sx * 1.9                                                              # tall ears, dark red inside
        m.box(hd, cx - 1.9, 15.6, -4.2, cx + 1.9, 22.0, -4.2, earf(cx, 15.6, 22.0, 3.8),
              rotation=(-6, 0, sx * 30), pivot=(cx, 15.8, -4.2))
        for j in range(3):                                                         # white cheek tufts
            rod(m, hd, (sx * 2.6, 12.0 + j * 0.8, -4.6), (sx * 3.8, 11.4 + j * 0.9, -4.2), 1.0, coatf, extend=0.1)
    # the cone of shame: overlapping rings of plates, widening toward the front, round its neck
    for ring in range(6):
        rad = 3.2 + ring * 0.55
        z0 = -2.6 - ring * 0.62
        n = 14
        for i in range(n):
            a = 2 * math.pi * (i + 0.5) / n
            x, y = rad * math.sin(a), 13.0 + rad * math.cos(a)
            w = 2 * rad * math.sin(math.pi / n) + 0.5
            m.box(hd, x - w / 2, y - 0.5, z0 - 1.0, x + w / 2, y + 0.5, z0, conef,
                  rotation=(0, 0, math.degrees(a)), pivot=(x, y, z0 - 0.5))
    for nm, lx, lz, band in (("leg_front_left", -1.4, -4.4, 2.2), ("leg_front_right", 1.4, -4.4, None),
                             ("leg_back_left", -1.5, 4.6, None), ("leg_back_right", 1.5, 4.6, 2.6)):
        lg = m.bone(nm, top, (lx, 8, lz))
        rod(m, lg, (lx, 8.4, lz), (lx, 0.9, lz - 0.2), 1.7, legf(band), extend=0.3)  # legs, two bandaged
        m.round_box(lg, lx, lz - 0.5, 1.0, 1.2, 0, 1.2, coatf, cut=0.3)
    return m
