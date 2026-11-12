"""Shared helpers for the kickboxing apes (Tikimp, Tikilla): black fur, white skull-like face and bone stripes, gold
teeth, fingers and joints, red-ringed eyes, and white tiki-mask fists with red carved markings.

Shiny: bone-white fur with black markings and jade instead of gold.
"""
from __future__ import annotations

import math

from _boxmodel import mix
from _route import pal, tone

BASE = {"black": (44, 38, 40), "black_light": (74, 66, 68), "white": (240, 238, 234), "gold": (240, 190, 40),
        "gold_dark": (190, 140, 20), "red": (210, 40, 50), "eye": (255, 200, 40), "mane": (246, 246, 248),
        "mane_shade": (210, 210, 216)}
SHINY = {"black": (226, 218, 206), "black_light": (246, 240, 230), "white": (54, 48, 52), "gold": (60, 190, 140),
         "gold_dark": (30, 130, 90), "eye": (120, 240, 200), "mane": (70, 66, 70), "mane_shade": (50, 46, 50)}


def P(v):
    return pal(BASE, SHINY, v)


def solid(key):
    def s(x, y, z, face, variant, **k):
        return tone(P(variant)[key], face), None
    return s


def skull_face(face_y, eye_dx, eye_r, mouth_w, red_ring=True):
    """A head shader: black, with a white skull-like face on the front (eye sockets ringed red with yellow eyes, a
    nose notch and a wide golden grin of teeth)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                d = math.hypot(x - sx * eye_dx, (y - face_y) * 1.15)
                if d < eye_r:
                    if d < eye_r * 0.55:
                        return p["eye"], None
                    return (p["red"] if red_ring else p["black"]), None
            dy = y - face_y
            if -eye_r * 2.6 < dy < -eye_r * 1.1 and abs(x) < mouth_w:          # the golden grin
                if abs((x * 2.2) % 1.0 - 0.5) < 0.09:
                    return p["gold_dark"], None
                return p["gold"], None
            if abs(x) < eye_dx + eye_r * 1.2 and -eye_r * 2.7 < dy < eye_r * 1.3:
                if abs(x) < 0.3 and -eye_r * 1.1 < dy < -eye_r * 0.4:
                    return p["black"], None                                 # the nose notch
                return p["white"], None
        return tone(p["black"], face), None
    return s


def ribs(x, y, z, face, variant, y0=None, y1=None, **k):
    """Black torso with white bone stripes (ribs and a breastbone) on the front."""
    p = P(variant)
    if face == "north" and y0 is not None and y0 < y < y1:
        if abs(x) < 0.5:
            return p["white"], None
        if int((y - y0) * 1.1) % 2 == 0 and abs(x) < 2.6:
            return p["white"], None
    return tone(p["black"], face), None


def banded(key_a="black", key_b="white"):
    """A limb banded in two colours along its length (rods run along -z before rotating)."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        t = (box.lo[2] + box.size[2] - z) / max(box.size[2], 1e-6) if box is not None else 0
        return tone(p[key_a] if int(t * 4) % 2 == 0 else p[key_b], face), None
    return s


def tiki_fist(cx, cy, cz, facing="north", tiki=True):
    """A big white oval fist: on its front a red carved tiki face (a ring with a bar through it and two prongs)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == facing and tiki:
            u, v = x - cx, y - cy
            r = math.hypot(u * 1.2, v + 0.6)
            if abs(r - 1.3) < 0.32 or (abs(u) < 0.3 and v > -0.6 and v < 1.8):
                return p["red"], None
            if abs(abs(u) - 1.2) < 0.3 and 0.8 < v < 2.2:
                return p["red"], None
        return tone(p["white"], face), None
    return s
