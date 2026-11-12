"""Shaders shared by the mummy line (Mumpillar, Sarcoon, Pharantis): bandages, nemes stripes, gold, black visors and
glowing eyes.

Shaders return (colour, glow): glow an RGB for the emissive layer or None.

Shiny: turquoise and rose gold, with cyan eyes.
"""
from __future__ import annotations

import math

from _boxmodel import mix

BASE = {"wrap": (240, 242, 248), "wrap_line": (196, 202, 218), "blue": (72, 130, 220), "blue_pale": (186, 208, 240),
        "gold": (244, 192, 44), "gold_dark": (186, 132, 22), "black": (34, 34, 46), "eye": (255, 214, 60),
        "eye_ring": (250, 250, 240), "eye_orange": (255, 150, 40), "silver": (210, 214, 224), "mouth": (60, 130, 230)}
SHINY = {"blue": (40, 186, 176), "blue_pale": (170, 236, 228), "gold": (232, 150, 132), "gold_dark": (176, 96, 86),
         "eye": (120, 240, 255), "eye_orange": (90, 230, 255), "mouth": (40, 190, 180)}


def P(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def hashf(x, y, z):
    n = math.sin(math.floor(x) * 12.9898 + math.floor(y) * 78.233 + math.floor(z) * 37.719) * 43758.5453
    return n - math.floor(n)


def bandage(x, y, z, face, variant, patches=True, **k):
    """White bandage wrapped round and round: slanted grey lines where the strips overlap, and a few blue patches."""
    pal = P(variant)
    if face not in ("up", "down"):
        u = x if face in ("north", "south") else z
        if abs((y + 0.45 * u) % 1.6 - 0.8) < 0.13:
            return pal["wrap_line"], None
    if patches and hashf(x * 0.4 + 2, y * 0.4, z * 0.4) > 0.86:
        return mix(pal["blue"], pal["blue_pale"], 0.35), None
    return (pal["wrap"] if face != "down" else mix(pal["wrap"], (0, 0, 0), 0.15)), None


def nemes(x, y, z, face, variant, axis="y", period=1.6, **k):
    """A pharaoh's striped headcloth: alternating blue and pale blue bands."""
    pal = P(variant)
    v = {"y": y, "x": x, "z": z}[axis]
    return (pal["blue"] if (v % (2 * period)) < period else pal["blue_pale"]), None


def gold(x, y, z, face, variant, **k):
    pal = P(variant)
    if face == "up":
        return mix(pal["gold"], (255, 255, 255), 0.2), None
    if face == "down":
        return pal["gold_dark"], None
    return pal["gold"], None


def gold_bands(x, y, z, face, variant, period=1.4, **k):
    pal = P(variant)
    return (pal["gold"] if (y % (2 * period)) < period * 1.3 else pal["gold_dark"]), None


def black(x, y, z, face, variant, **k):
    return P(variant)["black"], None


def ring_eye(dx, dy, r, variant, orange=False):
    """A round glowing eye: a pale ring round a glowing yellow (or orange) centre -> (colour, glow) or None."""
    pal = P(variant)
    d = math.hypot(dx, dy)
    if d > r:
        return None
    if d > r * 0.62:
        return pal["eye_ring"], pal["eye_ring"]
    c = pal["eye_orange" if orange else "eye"]
    if dx < -0.15 * r and dy > 0.15 * r and d < 0.4 * r:
        return (255, 255, 255), (255, 255, 255)
    return c, c


def visor(dx, dy, rx, ry):
    """True inside a rounded black visor (an ellipse with radii rx, ry)."""
    return (dx / rx) ** 2 + (dy / ry) ** 2 <= 1
