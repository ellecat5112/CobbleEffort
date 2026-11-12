"""Shared helpers for the jerboa mice (Jerbolt, Mesmerboa): yellow fur, red-brown feet and ear rims, and the
hypnotic ring tail: an excessively long tail curled into a full circle round the floating mouse, banded yellow and
violet (the violet bands glow faintly), ending in a lightning-bolt tip. The ring sits on a `ring` bone, which the rig
turns round and round, so the bands and the bolt keep circling.

Shiny: lilac fur with a cyan-and-gold ring.
"""
from __future__ import annotations

import math

from _boxmodel import mix, rod
from _route import pal, tone

BASE = {"fur": (250, 212, 50), "fur_dark": (214, 170, 30), "belly": (250, 232, 170), "red": (196, 92, 80),
        "red_dark": (150, 64, 56), "pink": (244, 170, 170), "white": (250, 248, 244), "violet": (150, 90, 230),
        "outline": (90, 50, 40), "eye": (30, 26, 34), "nose": (110, 200, 210), "cheek": (255, 236, 140)}
SHINY = {"fur": (206, 170, 240), "fur_dark": (170, 130, 210), "belly": (236, 220, 250), "violet": (60, 210, 230),
         "cheek": (240, 210, 255)}


def P(variant):
    return pal(BASE, SHINY, variant)


def fur(belly_y=None):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if belly_y is not None and face == "north" and y < belly_y:
            return tone(p["belly"], face), None
        return tone(p["fur"], face), None
    return s


def red(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["red"] if face != "down" else p["red_dark"], face), None


def band(i):
    """A ring segment's shader: yellow and violet bands, two segments each; the violet glows; dark edges."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        violet = (i // 2) % 2 == 1
        c = p["violet"] if violet else p["fur"]
        if face in ("east", "west") or (box is not None and min(abs(z - box.lo[2]), abs(box.lo[2] + box.size[2] - z)) < 0.2):
            c = mix(c, p["outline"], 0.3)
        return tone(c, face), (c if violet else None)
    return s


def ring(m, bone, cx, cy, cz, radius, width, thick, n=20):
    """A full circle of rod segments round (cx, cy) in the x-y plane at depth cz."""
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        p0 = (cx + radius * math.cos(a0), cy + radius * math.sin(a0), cz)
        p1 = (cx + radius * math.cos(a1), cy + radius * math.sin(a1), cz)
        rod(m, bone, p0, p1, width, band(i), extend=0.6, t2=thick)


def bolt_shader(points):
    """A lightning-bolt plane (x-y), cut to the polygon `points`, yellow with a darker outline."""
    def inside(x, y):
        c = False
        for (x0, y0), (x1, y1) in zip(points, points[1:] + points[:1]):
            if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
                c = not c
        return c

    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if not inside(x, y):
            return (0, 0, 0, 0), None
        edge = not all(inside(x + dx, y + dy) for dx, dy in ((0.35, 0), (-0.35, 0), (0, 0.35), (0, -0.35)))
        return (p["outline"] if edge else p["fur"]), None
    return s


def bolt_points(x0, y0, s):
    """A zigzag bolt shape (Pikachu-like tail flag) starting at (x0, y0), scaled by s, rising up and out."""
    pts = [(0, 0), (1.2, 0.2), (0.8, 1.6), (2.6, 1.4), (2.0, 3.2), (4.4, 3.0), (4.0, 6.6), (2.0, 4.4), (2.4, 4.4),
           (0.8, 2.6), (1.2, 2.6), (-0.4, 0.8)]
    return [(x0 + px * s, y0 + py * s) for px, py in pts]
