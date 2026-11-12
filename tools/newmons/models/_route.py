"""Shared helpers for the route-one Pokémon (seed spider, knife dragonfly, cardinal, rubber duck, radish rat lines).

Each model module keeps its own palette dict (BASE, SHINY); `pal(module_palettes, variant)` picks one. Shaders return
(colour, glow) like the other lines'. Helpers paint common features from model-space positions: round eyes with a
shine, soft vertical shading, leaf planes cut out to shape, and blades.
"""
from __future__ import annotations

import math

from _boxmodel import mix


def pal(base, shiny, variant):
    return base if variant != "shiny" else {**base, **shiny}


def tone(c, face):
    """Soft extra shading on top of the box painter's: tops a little lighter, undersides darker."""
    if face == "up":
        return mix(c, (255, 255, 255), 0.12)
    if face == "down":
        return mix(c, (0, 0, 0), 0.18)
    return c


def solid(base, shiny, key):
    """A shader painting one palette colour."""
    def s(x, y, z, face, variant, **k):
        return tone(pal(base, shiny, variant)[key], face), None
    return s


def round_eye(dx, dy, r, iris, pupil=(24, 22, 30), ring=None, glow=None):
    """A round eye: optional ring, a coloured iris, a dark pupil and a white shine -> (colour, glow) or None."""
    d = math.hypot(dx, dy)
    if d > r:
        return None
    if ring is not None and d > r * 0.8:
        return ring, None
    if dx < -0.2 * r and dy > 0.2 * r and d < 0.45 * r:
        return (255, 255, 255), None
    if d < r * 0.38:
        return pupil, None
    return iris, glow


def dot_eye(dx, dy, rx, ry, colour=(24, 22, 30)):
    """A small oval dark eye with a shine."""
    if (dx / rx) ** 2 + (dy / ry) ** 2 > 1:
        return None
    if dx < -0.15 * rx and dy > 0.25 * ry and (dx / rx) ** 2 + (dy / ry) ** 2 < 0.35:
        return (255, 255, 255), None
    return colour, None


def leaf_plane(origin, leaves, length, width, light, dark, axes="xz", serrate=0.0):
    """A flat plane of pointed leaves fanning from `origin` along angles (degrees) in the plane's two axes; darker
    midribs and veins; outside the leaves the plane is cut away. `axes`: "xz" (a horizontal plane, angle 0 = +z),
    "xy" (a vertical plane facing front, angle 0 = +y) or "zy" (a side plane, angle 0 = +y)."""
    ox, oz = origin

    def s(x, y, z, face, variant, **k):
        L, D = light(variant), dark(variant)
        a1, a2 = {"xz": (x, z), "xy": (x, y), "zy": (z, y)}[axes]
        for ang in leaves:
            a = math.radians(ang)
            dx, dz = a1 - ox, a2 - oz
            u = dx * math.sin(a) + dz * math.cos(a)
            v = dx * math.cos(a) - dz * math.sin(a)
            if 0 <= u <= length:
                w = width * math.sin(math.pi * u / length) ** 0.8
                if serrate:
                    w *= 1 - serrate * abs(math.sin(u * 2.2))
                if abs(v) <= w:
                    if abs(v) < 0.16 or (abs(v) > 0.3 and abs(abs(v) - (u * 0.35) % 1.4) < 0.08):
                        return D, None
                    return mix(L, D, 0.25 * u / length), None
        return (0, 0, 0, 0), None
    return s


def along(z, box):
    """How far a texel is along a rod box (0 at its start, 1 at its end): rods run along -z before rotating."""
    return (box.lo[2] + box.size[2] - z) / max(box.size[2], 1e-6)
