"""Shaders shared by the knife dragonfly line (Shivnymph, Sheathalis, Cutlassfly): steel blades, handles, wood, and the
dragonfly's teal-and-brown body with orange eyes.

Shiny: crimson body and gilded blades.
"""
from __future__ import annotations

from _boxmodel import mix
from _route import pal, round_eye, tone

BASE = {"teal": (58, 150, 160), "teal_dark": (34, 92, 112), "teal_light": (120, 200, 200), "brown": (120, 80, 56),
        "brown_dark": (80, 52, 36), "iris": (255, 140, 40), "steel": (196, 202, 212), "steel_light": (238, 242, 248),
        "steel_dark": (130, 136, 150), "handle": (40, 34, 36), "rivet": (210, 200, 180), "wood": (170, 120, 70),
        "wood_dark": (126, 84, 46), "tip": (240, 110, 40)}
SHINY = {"teal": (190, 50, 70), "teal_dark": (120, 26, 44), "teal_light": (240, 120, 130), "steel": (232, 196, 100),
         "steel_light": (255, 236, 170), "steel_dark": (170, 130, 50), "iris": (120, 230, 120)}


def P(variant):
    return pal(BASE, SHINY, variant)


def body(x, y, z, face, variant, **k):
    """Teal on top, brown underneath, like a dragonfly nymph."""
    p = P(variant)
    if face == "down" or y < k.get("belly", -99):
        return tone(p["brown"], face), None
    return tone(p["teal"], face), None


def blade_plane(spine_v, edge_v, tip_u, base_u, axes="xz", sign=1):
    """A flat knife blade in a plane: from base_u to tip_u along the first axis, a straight spine at spine_v and a
    cutting edge at edge_v curving up to meet the spine at the point. Shiny bevel along the edge, a darker fuller line,
    cut away outside the blade. `sign` mirrors the first axis (left/right wings)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        a1, a2 = {"xz": (x, z), "xy": (x, y), "zy": (z, y)}[axes]
        u = (a1 * sign - base_u) / (tip_u - base_u)
        if not 0 <= u <= 1:
            return (0, 0, 0, 0), None
        edge = edge_v + (spine_v - edge_v) * max(0.0, (u - 0.55) / 0.45) ** 1.6
        lo, hi = sorted((spine_v, edge))
        if not lo <= a2 <= hi:
            return (0, 0, 0, 0), None
        w = hi - lo
        d_edge = abs(a2 - edge)
        if d_edge < 0.35 + 0.1 * w:
            return p["steel_light"], None
        if abs(a2 - (spine_v + (edge - spine_v) * 0.3)) < 0.18:
            return p["steel_dark"], None
        return p["steel"], None
    return s


def steel(x, y, z, face, variant, **k):
    p = P(variant)
    return (p["steel_light"] if face == "up" else p["steel"]), None


def handle(x, y, z, face, variant, **k):
    p = P(variant)
    if abs((y * 3 + z * 3) % 3.2 - 1.6) < 0.25 and face in ("east", "west"):
        return p["rivet"], None
    return tone(p["handle"], face), None


def eyes(cx, cy, r, sx_off):
    """Two big orange dragonfly eyes on the front face, either side of cx, at height cy."""
    def f(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                e = round_eye(x - cx - sx * sx_off, y - cy, r, p["iris"])
                if e:
                    return e
        return body(x, y, z, face, variant)
    return f


def wood(x, y, z, face, variant, **k):
    p = P(variant)
    v = (x * 0.15 + z * 0.15 + 0.6 * ((y * 1.7) % 1.0)) if face == "up" else y + 0.25 * (x + z)
    c = p["wood"] if (v * 2.2) % 1.0 < 0.75 else p["wood_dark"]
    return tone(mix(c, p["wood_dark"], 0.15 if face == "down" else 0), face), None
