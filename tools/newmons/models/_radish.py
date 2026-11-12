"""Shaders shared by the radish rat line (Raddent, Rattlebunch): magenta radish skin with fine green veins and a pale
root tip, a tan rat face patch, dark eyes and nose, white buck teeth, whiskers and leafy green tops.

Shiny: a white daikon radish with its leaves a little bluer.
"""
from __future__ import annotations

import math

from _boxmodel import mix
from _route import dot_eye, pal, tone

BASE = {"skin": (214, 96, 150), "skin_dark": (168, 60, 112), "vein": (110, 150, 60), "face": (206, 170, 130),
        "eye": (60, 60, 90), "nose": (40, 36, 50), "tooth": (252, 250, 240), "leaf": (110, 180, 80),
        "leaf_dark": (60, 124, 50), "root": (240, 220, 226), "whisker": (60, 54, 60), "twine": (176, 140, 90)}
SHINY = {"skin": (244, 240, 230), "skin_dark": (210, 204, 190), "leaf": (100, 190, 140), "leaf_dark": (50, 130, 100),
         "face": (230, 200, 170)}


def P(variant):
    return pal(BASE, SHINY, variant)


def radish(facing, cx, cy, cz, face_w=2.6):
    """A radish body facing `facing` ("north", "east", "west", "south") with its centre at (cx, cy, cz): magenta skin,
    fine green veins, a tan face patch with two dark eyes on the side it faces, and a pale root tip at the back."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == facing:
            h = {"north": x - cx, "south": cx - x, "west": z - cz, "east": cz - z}[facing]
            v = y - cy
            for sx in (-1, 1):
                e = dot_eye(h - sx * face_w * 0.7, v - 1.0, 0.45, 0.55, p["eye"])
                if e:
                    return e
            if (h / face_w) ** 2 + ((v + 0.6) / 2.0) ** 2 < 1:
                return tone(p["face"], face), None
        w = abs(math.sin(x * 1.1 + z * 0.9) * math.cos(y * 0.7 - z * 0.4))
        if w < 0.03:
            return p["vein"], None
        c = p["skin"] if face != "down" else p["skin_dark"]
        return tone(c, face), None
    return s


def snout(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["skin"], face), None


def nose(x, y, z, face, variant, **k):
    return P(variant)["nose"], None


def tooth(x, y, z, face, variant, **k):
    return P(variant)["tooth"], None


def whisker(x, y, z, face, variant, **k):
    return P(variant)["whisker"], None


def foot(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["skin_dark"], face), None


def twine(x, y, z, face, variant, **k):
    p = P(variant)
    return (p["twine"] if int((y + x + z) * 3) % 2 else mix(p["twine"], (0, 0, 0), 0.2)), None


def stem(x, y, z, face, variant, **k):
    return tone(P(variant)["leaf_dark"], face), None


def light(v):
    return P(v)["leaf"]


def dark(v):
    return P(v)["leaf_dark"]
