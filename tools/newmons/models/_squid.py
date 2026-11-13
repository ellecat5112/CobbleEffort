"""Shared colours and shaders for the CobbleEffort Tentacool line, deep-sea squids after the art the user shared
(artist not named): a purple mantle dotted with glowing blue ring photophores, a yellow head and arms speckled blue,
big yellow eyes with black slit pupils, and two long tentacles ending in hooked ring clubs.

Shiny: a crimson mantle (like the red squids of the deep) with a pale peach head and arms.
"""
from __future__ import annotations

import math

from _boxmodel import rod
from _route import pal, tone

BASE = {"mantle": (150, 72, 190), "mantle_dark": (104, 44, 146), "mantle_light": (186, 120, 222),
        "ring": (150, 214, 255), "body": (240, 216, 84), "body_dark": (200, 168, 52), "dot": (100, 184, 240),
        "tip": (70, 120, 230), "eye": (250, 222, 64), "pupil": (20, 18, 24), "rim": (60, 40, 30), "hook": (40, 34, 44)}
SHINY = {"mantle": (182, 40, 62), "mantle_dark": (128, 24, 44), "mantle_light": (222, 92, 110), "body": (250, 204, 176),
         "body_dark": (214, 160, 134), "dot": (110, 220, 230), "tip": (70, 200, 220)}


def P(v):
    return pal(BASE, SHINY, v)


def mantlef(spots, top_dark=None):
    """The purple mantle with glowing ring photophores at the given (x, y, z, r) places (3D, on its surface)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        for sx, sy, sz, r in spots:
            d = math.sqrt((x - sx) ** 2 + (y - sy) ** 2 + (z - sz) ** 2)
            if d < r:
                if d > r * 0.58:
                    return p["ring"], p["ring"]                            # the glowing ring
                return p["mantle_light"], None
        if face == "down":
            return p["mantle_dark"], None
        if top_dark is not None and y > top_dark:
            return tone(p["mantle_dark"], face), None
        return tone(p["mantle"], face), None
    return s


def bodyf(x, y, z, face, variant, **k):
    """The yellow head, speckled blue."""
    p = P(variant)
    if face != "down" and math.sin(x * 2.3 + z * 1.7) * math.sin(y * 2.9 - z * 0.6) > 0.82:
        return p["dot"], None
    return tone(p["body"], face), None


def armf(tip_glow=False):
    """Yellow arms speckled blue (rods: z runs along them), blue toward the tip; the tip glows if tip_glow."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face in ("north", "south"):
            c = p["tip"]
            return c, (c if tip_glow else None)
        if math.sin(z * 2.1 + x * 0.9) > 0.86:
            return p["dot"], None
        return tone(p["body"], face), None
    return s


def tipf(glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)["tip"]
        return tone(c, face), (c if glow else None)
    return s


def hookf(x, y, z, face, variant, **k):
    return tone(P(variant)["hook"], face), None


def eye(face, x, y, z, ex, ey, ez, r, variant):
    """A big yellow eye with a black vertical slit pupil, centred at (ex, ey, ez) on the head's surface."""
    p = P(variant)
    d = math.sqrt((x - ex) ** 2 + (y - ey) ** 2 + (z - ez) ** 2)
    if d >= r:
        return None
    if d > r * 0.82:
        return p["rim"]
    horiz = math.hypot(x - ex, z - ez)
    if horiz < r * 0.18 and abs(y - ey) < r * 0.7:
        return p["pupil"]
    return p["eye"]


def ring_club(m, bone, cx, cy, cz, size, shader):
    """A hooked ring club at a tentacle's end: a little square ring of four bars in the xy plane."""
    h, t = size / 2, max(0.45, size * 0.24)
    m.box(bone, cx - h, cy + h - t, cz - t / 2, cx + h, cy + h, cz + t / 2, shader)
    m.box(bone, cx - h, cy - h, cz - t / 2, cx + h, cy - h + t, cz + t / 2, shader)
    m.box(bone, cx - h, cy - h, cz - t / 2, cx - h + t, cy + h, cz + t / 2, shader)
    m.box(bone, cx + h - t, cy - h, cz - t / 2, cx + h, cy + h, cz + t / 2, shader)


def tentacle(m, bone, pts, t0, t1, shader):
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        t = t0 + (t1 - t0) * i / max(1, len(pts) - 2)
        rod(m, bone, a, b, max(0.5, t), shader, extend=0.2)
