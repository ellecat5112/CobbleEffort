"""Shared helpers for the land shark line (Sharkindle, Forgnash, Magmalodon), CobbleEffort's pseudo-legendary:
black and dark-grey hide with red armour, glowing orange fins, flames and (Magmalodon) smoke.

Planes are cut to polygons (fins) or flame tongues; flames and fins glow (emissive layer); smoke is translucent (the
shell layer).

Shiny: steel-silver hide, cobalt armour and blue flames.
"""
from __future__ import annotations

import math

from _boxmodel import mix
from _route import pal, tone

BASE = {"black": (34, 32, 38), "grey": (74, 78, 90), "grey_light": (110, 116, 130), "red": (190, 40, 46),
        "red_dark": (130, 24, 30), "orange": (255, 150, 40), "yellow": (255, 210, 70), "eye": (255, 200, 50),
        "tooth": (248, 246, 240), "claw": (236, 236, 240), "smoke": (150, 148, 156), "flame_core": (255, 240, 170),
        "flame_mid": (255, 150, 40), "flame_edge": (220, 50, 20)}
SHINY = {"black": (150, 156, 170), "grey": (190, 196, 208), "grey_light": (225, 230, 238), "red": (40, 80, 200),
         "red_dark": (24, 50, 140), "orange": (60, 200, 255), "yellow": (150, 230, 255), "eye": (120, 230, 255),
         "smoke": (200, 210, 235), "flame_core": (220, 250, 255), "flame_mid": (60, 170, 255), "flame_edge": (30, 60, 220)}


def P(variant):
    return pal(BASE, SHINY, variant)


def solid(key):
    def s(x, y, z, face, variant, **k):
        return tone(P(variant)[key], face), None
    return s


def glow(key):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return c, c
    return s


def plane_coords(x, y, z, axes):
    return {"xy": (x, y), "zy": (z, y), "xz": (x, z)}[axes]


def inside_poly(u, v, pts):
    c = False
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        if (y0 > v) != (y1 > v) and u < x0 + (v - y0) * (x1 - x0) / (y1 - y0):
            c = not c
    return c


def fin(pts, axes="zy", key="orange", glow_it=True):
    """A plane cut to the polygon `pts` (in the plane's two axes): a fin, coloured `key` with a darker edge line."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        u, v = plane_coords(x, y, z, axes)
        if not inside_poly(u, v, pts):
            return (0, 0, 0, 0), None
        edge = not all(inside_poly(u + du, v + dv, pts) for du, dv in ((0.3, 0), (-0.3, 0), (0, 0.3), (0, -0.3)))
        c = mix(p[key], p["red_dark"], 0.5) if edge else p[key]
        return c, (c if glow_it else None)
    return s


def flame(axes, base_v, tongues, width):
    """A plane of flame tongues rising from height base_v: tongues = [(u centre, height), ...], each `width` wide at
    its base; white-hot in the core, orange, red at the edges; all glowing."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        u, v = plane_coords(x, y, z, axes)
        v -= base_v
        best = None
        for uc, hgt in tongues:
            if 0 <= v <= hgt:
                w = width * 0.5 * (1 - v / hgt) ** 0.7 * (1 + 0.15 * math.sin(v * 2.3 + uc))
                d = abs(u - uc) / max(w, 1e-6)
                if d <= 1:
                    t = max(d, v / hgt)
                    best = min(best, t) if best is not None else t
        if best is None:
            return (0, 0, 0, 0), None
        c = mix(p["flame_core"], p["flame_mid"], min(1, best * 1.6)) if best < 0.6 else mix(p["flame_mid"], p["flame_edge"], (best - 0.6) / 0.4)
        return c, c
    return s


def teeth_band(y0, y1, period=0.8):
    """True on a zigzag row of teeth between heights y0 (gum) and y1 (tips) along a horizontal coordinate."""
    def f(u, v):
        tri = abs((u / period) % 1.0 - 0.5) * 2               # 0 at a tooth's point, 1 between teeth
        tip = y1 + (y0 - y1) * tri
        lo, hi = sorted((y0, tip))
        return lo <= v <= hi
    return f


def smoke(x, y, z, face, variant, **k):
    """Translucent grey smoke (the shell layer)."""
    p = P(variant)
    a = 175 + int(35 * math.sin(y * 1.3 + x * 0.7))
    return p["smoke"] + (a,), None
