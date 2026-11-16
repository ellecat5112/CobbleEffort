"""Shared palette and shaders for the Algomon line (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): glossy lime-green and violet "algorithm" creatures with big ringed eyes, yellow-and-red tipped horns,
green tentacles and, at the last stages, black armour with green vine trim.

Shiny: crimson and teal (the green turns crimson, the violet teal)."""
from __future__ import annotations

import math

from _digidetail import eye, local, metal, mix, mul, plane, skin, solid
from _route import pal, tone

BASE = {"green": (120, 210, 40), "green_dark": (40, 110, 20), "green_light": (220, 250, 140),
        "violet": (100, 50, 150), "violet_dark": (44, 18, 74), "violet_light": (170, 120, 220),
        "eye_y": (250, 226, 40), "eye_r": (220, 30, 60), "iris": (230, 40, 120), "pupil": (40, 10, 40),
        "white": (250, 250, 250), "pink": (240, 50, 140), "pink_light": (255, 160, 210),
        "horn_y": (250, 210, 40), "horn_r": (220, 40, 40), "steel": (200, 204, 214), "steel_dark": (110, 114, 126),
        "black": (34, 34, 42), "black_light": (90, 92, 110), "navy": (30, 34, 70), "navy_light": (80, 90, 150),
        "claw": (210, 30, 40), "lamp": (255, 250, 200), "feather": (170, 210, 60), "feather_dark": (70, 120, 30),
        "drop": (120, 200, 250)}
SHINY = {"green": (210, 40, 70), "green_dark": (120, 10, 30), "green_light": (255, 150, 170),
         "violet": (30, 140, 150), "violet_dark": (10, 70, 80), "violet_light": (110, 210, 220),
         "feather": (230, 80, 100), "feather_dark": (130, 20, 40), "navy": (60, 30, 70), "navy_light": (140, 90, 160)}


def P(v):
    return pal(BASE, SHINY, v)


def glossy(key, dark, light):
    """A glossy, wet-looking hide: smooth gradient lit from the top, a soft white specular streak."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        t = v / max(H, 1e-6) if face not in ("up", "down") else (1.0 if face == "up" else 0.0)
        col = mix(p[dark], p[key], min(1.0, 0.35 + t))
        a, b = plane(x, y, z, face)
        g = math.sin(a * 0.5 + b * 0.35)
        if g > 0.93:
            col = mix(col, p[light], 0.75)
        elif g > 0.8:
            col = mix(col, p[light], 0.3)
        return tone(col, face), None
    return s


GREEN = glossy("green", "green_dark", "green_light")
VIOLET = glossy("violet", "violet_dark", "violet_light")
STEEL = metal(P, "steel", dark="steel_dark", light="white")
BLACK = skin(P, "black", light="black_light", var=0.03)
CLAW = solid(P, "claw")


def hornf(x, y, z, face, variant, box=None, **k):
    """A violet horn whose tip is banded yellow then red."""
    p = P(variant)
    t = (box.lo[2] + box.size[2] - z) / max(box.size[2], 1e-6)          # 0 at the root
    col = p["violet"] if t < 0.55 else p["horn_y"] if t < 0.8 else p["horn_r"]
    return tone(col, face), None


def ringed_eye(cx, cy, r, face_want="north", outer="eye_y", ring="violet", iris="iris"):
    """The Algomon eye: a yellow almond with a violet rim, a pink iris ring and a dark pupil (a function (du, dv) ->
    colour or None for the face `face_want`)."""
    def f(x, y, z, face, p):
        if face != face_want:
            return None
        a, b = plane(x, y, z, face)
        du, dv = a - cx, b - cy
        d = math.hypot(du / 1.25, dv)
        if d > r:
            return None
        if d > r * 0.86:
            return p[ring]
        if d < r * 0.5:
            c = eye(p, du, dv, r * 0.5, iris)
            if c is not None:
                return c
        return p[outer]
    return f


def tentaclef(key="green", dark="green_dark"):
    """A tentacle: lengthwise ridges and a lighter underside."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        ridge = abs(((u / max(W, 1e-6)) * 3) % 1 - 0.5) < 0.12
        col = p[dark] if ridge else p[key]
        if face == "down":
            col = mix(col, p["green_light"], 0.3)
        return tone(col, face), None
    return s
