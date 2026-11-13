"""Shared colours, shaders and parts for the CobbleEffort Foongus line, Grass/Steel mushrooms that look like Phillips
head screws, after the art the user shared (artist not named): a steel dome cap with a cross slot on top, notched
sides and a ring of rivets, a round white body with swirly eyes and a cheery mouth, and arms that are threaded screw
shafts, on little copper feet.

Shiny: a brass screw.
"""
from __future__ import annotations

import math

from _boxmodel import rod
from _route import pal, tone

BASE = {"steel": (178, 182, 190), "steel_light": (214, 218, 226), "steel_dark": (110, 114, 124),
        "slot": (52, 54, 62), "white": (246, 246, 244), "white_shade": (214, 214, 218), "swirl": (150, 120, 100),
        "swirl_dark": (90, 80, 80), "mouth": (70, 40, 44), "tongue": (232, 120, 120), "blush": (250, 196, 200),
        "copper": (214, 128, 72), "hair": (160, 164, 172)}
SHINY = {"steel": (214, 176, 84), "steel_light": (244, 214, 130), "steel_dark": (150, 112, 44), "slot": (90, 62, 30),
         "hair": (200, 164, 90), "swirl": (110, 140, 200), "swirl_dark": (60, 80, 140)}


def P(v):
    return pal(BASE, SHINY, v)


def capf(cx, cz, rim_y, top_y, slot_w, notches=4):
    """The screw-head cap: steel, a dark Phillips cross slot on top, notches cut into its sides at the slot ends, and a
    ring of rivets round the rim (at rim_y)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        dx, dz = x - cx, z - cz
        if face == "up":
            if (abs(dx) < slot_w or abs(dz) < slot_w) and math.hypot(dx, dz) < (top_y - rim_y) * 1.6 + 1.2:
                return p["slot"], None                                     # the cross slot
            return p["steel_light"], None
        if face == "down":
            return p["steel_dark"], None
        if y > rim_y + 0.8 and (abs(dx) < slot_w * 0.9 or abs(dz) < slot_w * 0.9):
            return p["slot"], None                                         # notches at the slot ends
        if abs(y - rim_y) < 0.35:
            a = math.atan2(dz, dx)
            if (a * 14 / math.pi) % 2 < 0.55:
                return p["slot"], None                                     # rivets round the rim
        return tone(p["steel"], face), None
    return s


def threadf(pitch=1.1):
    """A threaded screw shaft (rods: z runs along it): slanted light and dark thread bands."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face in ("north", "south"):
            return p["steel_dark"], None
        t = (z + (x + y) * 0.45) % pitch
        return tone(p["steel_light"] if t < pitch * 0.5 else p["steel_dark"], face), None
    return s


def steelf(x, y, z, face, variant, **k):
    return tone(P(variant)["steel"], face), None


def copperf(x, y, z, face, variant, **k):
    return tone(P(variant)["copper"], face), None


def hairf(x, y, z, face, variant, **k):
    return tone(P(variant)["hair"], face), None


def facef(ex, ey, er, mouth_y, mouth_w, front_z):
    """The white body with a face on its front: two swirly eyes at (+-ex, ey) of radius er, a cheery open mouth."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                dx, dy = x - sx * ex, y - ey
                d = math.hypot(dx, dy)
                if d < er:
                    a = math.atan2(dy, dx) * sx
                    if (d / er * 3.2 - a / math.pi) % 1.0 < 0.42:
                        return (p["swirl_dark"] if sx < 0 else p["swirl"]), None   # spiral eyes
                    return p["white"], None
                if abs(dx) < er * 0.9 and -er * 1.9 < dy < -er * 1.25:
                    return p["blush"], None
            if abs(x) < mouth_w and mouth_y - mouth_w * 0.9 < y < mouth_y and \
                    (y - (mouth_y - mouth_w * 0.9)) > (abs(x) / mouth_w) ** 2 * mouth_w * 0.9 - 0.05:
                return (p["tongue"] if y < mouth_y - mouth_w * 0.55 else p["mouth"]), None
        return tone(p["white"] if face in ("north", "up", "east", "west") else p["white_shade"], face), None
    return s


def screw(m, bone, base, d, length, t, pitch=1.1):
    """A threaded screw shaft from base along d, tapering to a point."""
    n = math.sqrt(sum(v * v for v in d))
    u = tuple(v / n for v in d)
    at = lambda f: tuple(b + c * length * f for b, c in zip(base, u))
    rod(m, bone, at(0), at(0.45), t, threadf(pitch), extend=0.1)
    rod(m, bone, at(0.43), at(0.75), t * 0.72, threadf(pitch), extend=0.1)
    rod(m, bone, at(0.73), at(1.0), max(0.5, t * 0.38), threadf(pitch), extend=0.0)
